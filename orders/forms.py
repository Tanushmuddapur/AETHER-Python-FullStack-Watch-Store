from django import forms
from .models import Order

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=25)
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    offer_code = forms.CharField(max_length=60, required=False)
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_CHOICES, widget=forms.RadioSelect)
    save_address = forms.BooleanField(required=False, initial=True)
