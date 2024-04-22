from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Address  # Stelle sicher, dass Address importiert wird


class EigeneUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form'})
        self.fields['username'].label = 'Benutzername'
        self.fields['first_name'].widget.attrs.update({'class': 'form'})
        self.fields['first_name'].label = 'Vorname'
        self.fields['last_name'].widget.attrs.update({'class': 'form'})
        self.fields['last_name'].label = 'Nachname'
        self.fields['password1'].widget.attrs.update({'class': 'form'})
        self.fields['password1'].label = 'Passwort'
        self.fields['password2'].widget.attrs.update({'class': 'form'})
        self.fields['password2'].label = 'Passwort wiederholen'
        self.fields['email'].widget.attrs.update({'class': 'form'})
        self.fields['email'].label = 'Email'


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['postcode', 'city', 'street', 'house_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['postcode'].widget.attrs.update({'class': 'form'})
        self.fields['postcode'].label = 'PLZ'
        self.fields['city'].widget.attrs.update({'class': 'form'})
        self.fields['city'].label = 'Stadt'
        self.fields['street'].widget.attrs.update({'class': 'form'})
        self.fields['street'].label = 'Straße'
        self.fields['house_number'].widget.attrs.update({'class': 'form'})
        self.fields['house_number'].label = 'Hausnummer'
