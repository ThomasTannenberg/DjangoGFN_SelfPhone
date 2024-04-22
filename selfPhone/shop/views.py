from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Costumer
# from asgiref.sync import sync_to_async
from . forms import EigeneUserCreationForm, AddressForm

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


# def register_user(request):
#     seite = 'register'
#     form = EigeneUserCreationForm
#     messages.success(request, "register_user geladen.")

#     if request.method == 'POST':
#         form = EigeneUserCreationForm(request.POST)
#         if form.is_valid():
#             benutzer = form.save(commit=False)
#             benutzer.save()

#             customer = Costumer(
#                 first_name=request.POST['first_name'],
#                 last_name=request.POST['last_name'],
#                 email=request.POST['email'],
#                 customer=benutzer)
#             customer.save()

#             login(request, benutzer)
#             messages.success(request, "Benutzerkonto wurde erstellt.")
#             return redirect('shop')
#         else:
#             messages.error(
#                 request, "Fehler beim Erstellen des Benutzerkontos.")

#     return render(request, 'shop/register.html', {'seite': seite, 'form': form})
