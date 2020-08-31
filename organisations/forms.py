from django import forms

from organisations.models import Feedback, FeedbackType


class FeedbackForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Betreff'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Nachricht'}))
    type = forms.ModelChoiceField(queryset=FeedbackType.objects.filter(for_users=True).order_by('name'), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kategorie'}), label="Kategorie" )

    class Meta:
        model = Feedback
        fields= ('type', 'title', 'message')