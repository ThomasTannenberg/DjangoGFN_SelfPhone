
from .models import Smartphone
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import EigeneUserCreationForm, AddressForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import random

# Create your views here.

COLOR_MAP = {
    'Schwarz': '#000000',
    'Weiß': '#f1f1f1',
    'Rot': '#FF0000',
    'Blau': '#0000FF',
    'Grün': '#00FF00',
    'Gelb': '#FFFF00',
    'Grau': '#808080',
    'Silber': '#C0C0C0',
    'Gold': '#FFD700',
    # Füge weitere Farben hinzu, wie benötigt
}


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
    # Smartphones nach Hersteller filtern und nach Modell und ID sortieren
    smartphones = Smartphone.objects.filter(
        manufacturer=manufacturer).order_by('model', 'id')

    representatives = {}
    model_color_groups = {}

    # Smartphones nach Modell und Farbe gruppieren
    for phone in smartphones:
        model_color_key = (phone.model, phone.color)
        if model_color_key not in model_color_groups:
            model_color_groups[model_color_key] = []
        model_color_groups[model_color_key].append(phone)

    # Repräsentatives Smartphone für jede Modell- und Farbkombination wählen
    for model_color, phones in model_color_groups.items():
        representative = random.choice(phones)
        representatives[model_color] = representative.id

    # Bestimmen, ob ein Smartphone der Repräsentant seiner Modell- und Farbkombination ist
    for phone in smartphones:
        phone.is_representative = (
            phone.id == representatives[(phone.model, phone.color)])

    return render(request, 'shop/product_gallery.html', {
        'smartphones': smartphones,
        'manufacturer': manufacturer,
        'representatives': list(representatives.values())
    })


def product_details(request, smartphone_id):
    smartphone = get_object_or_404(Smartphone, pk=smartphone_id)

    color_results = Smartphone.objects.filter(
        manufacturer=smartphone.manufacturer,
        model=smartphone.model
    ).exclude(pk=smartphone.pk).values('color', 'id')

    storage_results = Smartphone.objects.filter(
        manufacturer=smartphone.manufacturer,
        model=smartphone.model
    ).exclude(pk=smartphone.pk).values('storage_size', 'id')

    memory_results = Smartphone.objects.filter(
        manufacturer=smartphone.manufacturer,
        model=smartphone.model
    ).exclude(pk=smartphone.pk).values('memory_size', 'id')

    # Entfernt Duplikate da SQLite kein distinct kennt
    color_variations = {v['color']: v for v in color_results}.values()
    storage_variations = {v['storage_size']
        : v for v in storage_results}.values()
    memory_variations = {v['memory_size']: v for v in memory_results}.values()

    # Anpassen der Farbcodes mit COLOR_MAP, von ganz oben
    color_variations = [{
        'color': color_variation['color'],
        'id': color_variation['id'],
        'color_code': COLOR_MAP.get(color_variation['color'], '#000000')
    } for color_variation in color_variations]

    return render(request, 'shop/product_details.html', {
        'smartphone': smartphone,
        'color_variations': list(color_variations),
        'storage_variations': list(storage_variations),
        'memory_variations': list(memory_variations)
    })


def basket(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        if product_id is not None:
            smartphone = get_object_or_404(Smartphone, pk=product_id)
            product, created = Product.objects.get_or_create(
                smartphone=smartphone)

            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            # Leiten Sie nach dem Hinzufügen zum Warenkorb zur Warenkorb-Seite oder einer Bestätigungsseite weiter
            return redirect('basket')

    # Anzeigen des aktuellen Warenkorbinhalts für den Benutzer
    # Filtern nach Benutzer, wenn Benutzeranmeldung implementiert ist
    cart_items = CartItem.objects.filter(is_ordered=False)
    total_price = sum(item.get_total_price for item in cart_items)
    return render(request, 'shop/basket.html', {'cart_items': cart_items, 'total_price': total_price})


@require_POST
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = request.POST.get('quantity')
    if quantity and quantity.isdigit():
        cart_item.quantity = int(quantity)
        cart_item.save()
    return redirect('basket')


@require_POST
def remove_from_basket(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('basket')


@ login_required
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
    if request.method == 'POST':
        if 'logout' in request.POST:  # Check for logout action
            logout(request)
            messages.success(request, "Erfolgreich ausgeloggt.")
            return redirect('login')

        benutzername = request.POST.get('benutzername')
        passwort = request.POST.get('passwort')

        if benutzername and passwort:
            benutzer = authenticate(
                request, username=benutzername, password=passwort)
            if benutzer is not None:
                login(request, benutzer)
                messages.success(request, "Erfolgreich eingeloggt.")
                return redirect('shop')
            else:
                messages.error(
                    request, "Benutzername oder Passwort nicht korrekt.")
                return render(request, 'shop/login.html', {'seite': seite})
        else:
            messages.error(
                request, "Bitte Benutzername und Passwort eingeben.")
            return render(request, 'shop/login.html', {'seite': seite})

    return render(request, 'shop/login.html', {'seite': seite})


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
