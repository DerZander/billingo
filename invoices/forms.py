from datetime import date

from django import forms

from recipients.models import Recipient
from invoices.models import Invoice

MONTHS = [(0,'Alle'),(1,'Januar'),(2,'Februar'),(3,'März'),(4,'April'),(5,'Mai'), (6,'Juni'), (7,'Juli'), (8,'August'),(9,'September'), (10,'Oktober'), (11,'November'), (12,'Dezember')]



class InvoiceForm(forms.ModelForm):
    invoice_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechnungsnummer'}))
    invoice_doctor = forms.ModelChoiceField(queryset=Recipient.objects.all().order_by('name'), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Arzt'}), label="Arzt")
    invoice_date = forms.DateField(initial=date.today(), widget=forms.SelectDateWidget(attrs={'class': 'form-control', 'placeholder': 'Rechnungsdatum'}))
    invoice_amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Betrag'}))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Beschreibung'}))

    class Meta:
        model = Invoice
        fields = ('invoice_number', 'invoice_doctor', 'invoice_date', 'invoice_amount', 'description')

class InvoiceSearchForm(forms.ModelForm):
    invoice_data = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechungsdaten'}))
    invoice_doctor = forms.ModelChoiceField(required=False, queryset=Recipient.objects.all().order_by('name'), widget=forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2', 'id': 'inlineFormCustomSelectPref', 'placeholder': 'Arzt'}), label="Arzt", )
    paid = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'custom-control-input','id':'customSwitch1'}))
    month = forms.ChoiceField(required=False, choices=MONTHS, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Rechnungsdatum'}))

    class Meta:
        model = Invoice
        fields = ('invoice_data','invoice_doctor','paid', 'month')