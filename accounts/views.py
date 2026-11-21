from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, AddressForm
from .models import Address
from orders.models import Order
from store.models import Wishlist, Cart

def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            parts = cd['full_name'].strip().split(' ', 1)
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'], first_name=parts[0], last_name=parts[1] if len(parts)>1 else '')
            if cd.get('account_role') == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
            user.profile.full_name = cd['full_name']
            user.profile.phone_number = cd['phone_number']
            user.profile.save()
            login(request, user)
            messages.success(request, f'Welcome to AETHER, {cd["full_name"]}.')
            return redirect('store:admin_console' if user.is_staff else 'store:home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            ident = form.cleaned_data['identifier'].strip()
            pw = form.cleaned_data['password']
            uname = ident
            if '@' in ident:
                m = User.objects.filter(email__iexact=ident).first()
                if m: uname = m.username
            user = authenticate(request, username=uname, password=pw)
            if user:
                login(request, user)
                request.session.set_expiry(1209600 if form.cleaned_data.get('remember_me') else 0)
                messages.success(request, f'Welcome back, {user.profile.full_name or user.username}.')
                return redirect(request.GET.get('next') or ('store:admin_console' if user.is_staff else 'store:home'))
            messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Signed out securely.')
    return redirect('store:home')

@login_required
def dashboard_view(request):
    tab = request.GET.get('tab', 'overview')
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile, user=request.user)
    password_form = PasswordChangeForm(user=request.user)
    address_form = AddressForm()

    if request.method == 'POST':
        act = request.POST.get('action')
        if act == 'update_profile':
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
            if profile_form.is_valid():
                profile_form.save()
                request.user.email = profile_form.cleaned_data['email']
                request.user.save()
                messages.success(request, 'Profile updated.')
                return redirect('/accounts/dashboard/?tab=settings')
        elif act == 'change_password':
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                u = password_form.save()
                update_session_auth_hash(request, u)
                messages.success(request, 'Password updated.')
                return redirect('/accounts/dashboard/?tab=password')
        elif act == 'add_address':
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                a = address_form.save(commit=False)
                a.user = request.user
                a.save()
                messages.success(request, 'Address saved.')
                return redirect('/accounts/dashboard/?tab=addresses')

    return render(request, 'accounts/dashboard.html', {
        'tab': tab, 'orders': orders, 'wishlist_items': wishlist.items.select_related('product'),
        'cart': cart, 'addresses': addresses, 'profile_form': profile_form,
        'password_form': password_form, 'address_form': address_form,
    })

@login_required
@require_POST
def delete_address(request, address_id):
    get_object_or_404(Address, id=address_id, user=request.user).delete()
    return redirect('/accounts/dashboard/?tab=addresses')
