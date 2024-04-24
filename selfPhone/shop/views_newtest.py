from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import EigeneUserCreationForm, AddressForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# F() Expression ermöglicht es, die Datenbank direkt zu aktualisieren
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.


def shop(request):
    return render(request, 'shop/start.html')


def start(request):
    return render(request, 'shop/start.html')


def apple(request):
    return redirect('product_gallery', manufacturer='Apple')


def samsung(request):
    return redirect('product_gallery', manufacturer='Samsung')


def huawei(request):
    return redirect('product_gallery', manufacturer='Huawei')


def xiaomi(request):
    return redirect('product_gallery', manufacturer='Xiaomi')


def sony(request):
    return redirect('product_gallery', manufacturer='Sony')


def google(request):
    return redirect('product_gallery', manufacturer='Google')


def product_gallery(request, manufacturer):
    smartphones_list = Smartphone.objects.filter(manufacturer=manufacturer)
    grouped_smartphones = {}

    for phone in smartphones_list:
        key = (phone.model, phone.memory_size, phone.storage_size)
        if key not in grouped_smartphones:
            grouped_smartphones[key] = []
        grouped_smartphones[key].append(phone)

    return render(request, 'shop/product_gallery.html', {
        'grouped_smartphones': grouped_smartphones,
        'manufacturer': manufacturer
    })


def product_details(request, smartphone_id):
    smartphone = get_object_or_404(Smartphone, pk=smartphone_id)

    color_variations = Smartphone.objects.filter(
        manufacturer=smartphone.manufacturer,
        model=smartphone.model
    ).exclude(pk=smartphone.pk).values('color', 'id')

    storage_variations = Smartphone.objects.filter(
        manufacturer=smartphone.manufacturer,
        model=smartphone.model
    ).exclude(pk=smartphone.pk).values('storage_size', 'id')

    memory_variations = Smartphone.objects.filter(
        manufacturer=smartphone.manufacturer,
        model=smartphone.model
    ).exclude(pk=smartphone.pk).values('memory_size', 'id')

    color_variations = {v['color']: v for v in color_variations}.values()
    storage_variations = {v['storage_size']
        : v for v in storage_variations}.values()
    memory_variations = {v['memory_size']
        : v for v in memory_variations}.values()

    return render(request, 'shop/product_details.html', {
        'smartphone': smartphone,
        'color_variations': color_variations,
        'storage_variations': storage_variations,
        'memory_variations': memory_variations
    })


def basket(request):
    return render(request, 'shop/basket.html')


@login_required
def checkout(request):
    try:
        customer = Costumer.objects.get(customer=request.user)
        address = Address.objects.filter(customer=customer).first()
        cart_items = CartItem.objects.filter(
            product__smartphone__customer=customer, is_ordered=False)
        if not cart_items:
            messages.info(request, "Ihr Warenkorb ist leer.")
            return render(request, 'shop/checkout.html', {
                'customer': customer,
                'address': address,
                'cart_items': cart_items
            })
        return render(request, 'shop/checkout.html', {
            'customer': customer,
            'address': address,
            'cart_items': cart_items
        })
    except Costumer.DoesNotExist:
        messages.error(request, "Kundeninformationen nicht gefunden.")
        return redirect('login')
    except Exception as e:
        # Für andere unerwartete Ausnahmen
        messages.error(request, f"Ein Fehler ist aufgetreten: {str(e)}")
        return redirect('home')


def test(request):
    return render(request, 'shop/test.html')


def login_user(request):
    seite = 'login'
    messages.success(request, "methode geladen.")
    if request.method == 'POST':
        benutzername = request.POST['benutzername']
        passwort = request.POST['passwort']

        messages.success(request, "POST WAR ERFOLGREICH.")

        benutzer = authenticate(
            request, username=benutzername, password=passwort)

        if benutzer is not None:
            login(request, benutzer)
            # server message
            messages.success(request, "Erfolgreich eingeloggt.")
            return redirect('shop')
        else:
            messages.error(
                request, "Benutzername oder Passwort nicht korrekt.")

    return render(request, 'shop/login.html', {'seite': seite})


def logout_user(request):
    logout(request)
    messages.success(request, "Erfolgreich ausgeloggt.")
    return render(request, 'shop/logout.html')


def register_user(request):
    seite = 'register'
    user_form = EigeneUserCreationForm()
    address_form = AddressForm()
    if request.method == 'POST':
        user_form = EigeneUserCreationForm(request.POST)
        address_form = AddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            benutzer = user_form.save()
            if Costumer.objects.filter(customer=benutzer).exists():
                messages.error(request, "Benutzerkonto bereits vorhanden.")
                return render(request, 'shop/register.html', {'seite': seite, 'user_form': user_form, 'address_form': address_form})

            customer = Costumer(
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
                email=user_form.cleaned_data['email'],
                customer=benutzer)
            customer.save()

            address = address_form.save(commit=False)
            address.customer = customer  # Verknüpfung der Adresse mit dem Customer
            address.save()

            login(request, benutzer)
            messages.success(request, "Benutzerkonto wurde erstellt.")
            return redirect('shop')
        else:
            messages.error(
                request, "Fehler beim Erstellen des Benutzerkontos.")

    return render(request, 'shop/register.html', {'seite': seite, 'user_form': user_form, 'address_form': address_form})


@require_POST  # Stellt sicher, dass diese View nur POST-Anfragen akzeptiert
def shopBackend(request):
    try:
        data = json.loads(request.body)
        action = data.get('action')
        if action == 'add_to_cart':
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.update_or_create(
                product=product,
                defaults={'quantity': F('quantity') + quantity}
            )
            return JsonResponse({'message': 'Produkt erfolgreich zum Warenkorb hinzugefügt',
                                 'cart_quantity': cart_item.quantity}, status=200)
        elif action == 'update_cart':
            cart_item_id = data.get('cart_item_id')
            quantity = data.get('quantity')
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'message': 'Warenkorb erfolgreich aktualisiert'}, status=200)
        elif action == 'remove_from_cart':
            cart_item_id = data.get('cart_item_id')
            CartItem.objects.filter(id=cart_item_id).delete()
            return JsonResponse({'message': 'Artikel erfolgreich aus dem Warenkorb entfernt'},
                                status=200)
        elif action == 'create_order':
            customer = Costumer.objects.get(user=request.user)

            address = Address.objects.filter(customer=customer).first()
            order = Order.objects.create(customer=customer, address=address)

            cart_items = CartItem.objects.filter(
                product__smartphone__customer=customer, is_ordered=False)
            for item in cart_items:
                item.is_ordered = True
                item.save()
            order.products.set(cart_items)
            order.save()
            return JsonResponse({'message': 'Bestellung erfolgreich erstellt',
                                 'order_id': order.id}, status=200)
        else:
            return JsonResponse({'error': 'Unbekannte Aktion'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produkt nicht gefunden'}, status=404)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Warenkorb-Element nicht gefunden'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
