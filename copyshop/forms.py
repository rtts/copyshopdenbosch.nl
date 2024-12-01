from urllib.parse import quote
from django import forms
from django.conf import settings
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'email', 'phone', 'address', 'notes']

class CreateOrderForm(forms.ModelForm):
    def clean_total(self):
        total = self.cleaned_data['total']
        if total < 0.35:
            raise forms.ValidationError('Het minimumbedrag is €0,35')
        return total

    class Meta:
        model = Order
        fields = ['total', 'assignee']

class ContactForm(forms.Form):
    """
    Spam-resistant contact form.
    """

    body = forms.CharField(label="Uw bericht", widget=forms.Textarea(), required=False)

    def save(self):
        """
        Return a mailto: link.
        """

        subject = quote(settings.CONTACT_FORM_EMAIL_SUBJECT, safe="")
        body = quote(self.cleaned_data.get("body"), safe="")
        return f"mailto:{settings.CONTACT_FORM_EMAIL_ADDRESS}?subject={subject}&body={body}"
