from django import forms
from django.contrib.auth.models import User
from .models import Profile, Address

class RegistrationForm(forms.Form):
    ROLE_CHOICES = [('collector', 'Collector Account'), ('admin', 'Atelier Admin')]
    account_role = forms.ChoiceField(choices=ROLE_CHOICES, initial='collector', widget=forms.RadioSelect)
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Julian Mercer'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'julian_mercer'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'julian@aether.ch'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '+91 98765 43210'}))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'placeholder': 'Minimum 6 characters', 'id': 'reg-password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password', 'id': 'reg-confirm-password'}))

    def clean_username(self):
        u = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=u).exists():
            raise forms.ValidationError('Username already taken.')
        return u

    def clean_email(self):
        e = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=e).exists():
            raise forms.ValidationError('Email already registered.')
        return e

    def clean(self):
        cd = super().clean()
        if cd.get('password') != cd.get('confirm_password'):
            self.add_error('confirm_password', 'Passwords do not match.')
        return cd

class LoginForm(forms.Form):
    identifier = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'login-password'}))
    remember_me = forms.BooleanField(required=False)

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'avatar', 'bio']
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['label', 'recipient_name', 'phone_number', 'street_address', 'city', 'state', 'postal_code', 'country', 'is_default']
