from .models import Product, CartItem, Order
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Costumer
# from asgiref.sync import sync_to_async
from . forms import EigeneUserCreationForm, AddressForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.


def shop(request):
    return render(request, 'shop/start.html')


def start(request):
    return render(request, 'shop/start.html')


def apple(request):
    return render(request, 'shop/apple.html')


def samsung(request):
    return render(request, 'shop/samsung.html')


def huawei(request):
    return render(request, 'shop/huawei.html')


def xiaomi(request):
    return render(request, 'shop/xiaomi.html')


def sony(request):
    return render(request, 'shop/sony.html')


def google(request):
    return render(request, 'shop/google.html')


def product_gallery(request):
    return render(request, 'shop/product_gallery.html')


def product_details(request):
    return render(request, 'shop/product_details.html')


def basket(request):
    return render(request, 'shop/basket.html')


def checkout(request):
    return render(request, 'shop/checkout.html')


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


@require_POST  # Stellt sicher, dass diese View nur POST-Anfragen akzeptiert... fliegt vielleicht raus
def shopBackend(request):
    try:
        data = json.loads(request.body)
        action = data.get('action')
        if action == 'add_to_cart':
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += int(quantity)
                cart_item.save()
            return JsonResponse({'message': 'Produkt erfolgreich zum Warenkorb hinzugefügt', 'cart_quantity': cart_item.quantity}, status=200)
        elif action == 'create_order':
            # Logik zur Erstellung einer Bestellung?????
            # Kann ich one DB schlecht testen
            pass
        else:
            return JsonResponse({'error': 'Unbekannte Aktion'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produkt nicht gefunden'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
