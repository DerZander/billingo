from django import forms
from django.core.exceptions import ValidationError

from .models import Recipient, RecipientType, RecipientFavorit


class RecipientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Arzt'}))
    description = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Beschreibung'}))
    recipient_type = forms.ModelChoiceField(queryset=RecipientType.objects.all().order_by('name'), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kategorie'}), label="Kategorie", )
    iban = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IBAN'}))
    street = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Straße'}))
    housenumber = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hausnummer'}))
    postcode = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PLZ'}))
    city = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ort'}))

    class Meta:
        model = Recipient
        fields = ('name', 'description', 'recipient_type', 'iban', 'street', 'housenumber', 'postcode', 'city')


class RecipientTypeForm(forms.ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'forms-control', 'placeholder': 'Typname'}))
    description = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Beschreibung'}))

    class Meta:
        model = RecipientType
        fields = ('name', 'description')


class RecipientSearchForm(forms.ModelForm):
    recipient_type = forms.ModelChoiceField(required=False, queryset=RecipientType.objects.all().order_by('name'), widget=forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2', 'id': 'inlineFormCustomSelectPref', 'placeholder': 'Kategorie'}), label="Kategorie", )
    favorit = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'custom-control-input','id':'customSwitch1'}))
    recipient_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Arzt'}))

    class Meta:
        model = RecipientType
        fields = ('recipient_type', 'favorit')

class RecipientTypeForm(forms.ModelForm):
    file = forms.FileField()#widget=forms.FileInput(attrs={'class':'custom-control-input', 'placeholder': 'Spezifikationsdatei'}))
    class Meta:
        model = RecipientType
        fields = ('file',)