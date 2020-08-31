from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(datetime.today().year-110,datetime.today().year+1),attrs={'class': 'form-control', 'placeholder': 'Geburtsdatum'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Straße'}))
    housenumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hausnummer'}))
    postcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PLZ'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ort'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vorname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nachname'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'birthday', 'street', 'housenumber', 'postcode', 'city', 'first_name', 'last_name')


class UserSignInForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email','password1', 'password2')

class CustomUserShowForm(UserChangeForm):
    email = forms.EmailField(disabled=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    birthday = forms.DateField(disabled=True, widget=forms.SelectDateWidget(years=range(datetime.today().year-110,datetime.today().year+1),attrs={'class': 'form-control', 'placeholder': 'Geburtsdatum'}))
    street = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Straße'}))
    housenumber = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hausnummer'}))
    postcode = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PLZ'}))
    city = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ort'}))
    first_name = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vorname'}))
    last_name = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nachname'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'birthday', 'street', 'housenumber', 'postcode', 'city', 'first_name', 'last_name')