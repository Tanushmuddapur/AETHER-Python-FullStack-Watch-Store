from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.http import require_POST
from store.models import Cart, Product
from accounts.models import Address
from .models import Order, OrderItem
from .forms import CheckoutForm

OFFER_CATALOG = {
    'AETHER10': {'label': '10% Instant Privilege Card Offer', 'pct': Decimal('0.10'), 'max': Decimal('25000.00')},
    'HDFC15': {'label': 'HDFC / ICICI Infinite Card 15% Off', 'pct': Decimal('0.15'), 'max': Decimal('40000.00')},
    'FIRST5000': {'label': 'First Collector Flat ₹5,000 Off', 'flat': Decimal('5000.00')},
}

def compute_offer_discount(subtotal, code):
    code = (code or '').strip().upper()
    if code not in OFFER_CATALOG or subtotal <= 0:
        return '', Decimal('0.00')
    rule = OFFER_CATALOG[code]
    disc = min(subtotal, rule['flat']) if 'flat' in rule else min(subtotal * rule['pct'], rule['max'])
    return code, disc.quantize(Decimal('0.01'))

@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    if not items.exists():
        return redirect('store:shop')
    default_addr = Address.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            with transaction.atomic():
                locked = []
                for c_item in items:
                    prod = Product.objects.select_for_update().get(pk=c_item.product.pk)
                    locked.append((c_item, prod))
                code, disc = compute_offer_discount(cart.subtotal, cd.get('offer_code'))
                final_amt = max(Decimal('0.00'), cart.subtotal - disc + cart.shipping_charge)
                order = Order.objects.create(
                    user=request.user, full_name=cd['full_name'], email=cd['email'],
                    phone_number=cd['phone_number'], delivery_address=cd['delivery_address'],
                    city=cd['city'], state=cd['state'], postal_code=cd['postal_code'],
                    subtotal=cart.subtotal, discount_amount=cart.total_discount,
                    offer_code=code, offer_discount=disc, shipping_charge=cart.shipping_charge,
                    final_amount=final_amt, payment_method=cd['payment_method'],
                    payment_status='Paid · AETHER Vault Settlement' if cd['payment_method']=='SIMULATED_CARD' else 'Cash on Delivery',
                    status='Confirmed'
                )
                for c_item, prod in locked:
                    OrderItem.objects.create(order=order, product=prod, product_name=prod.name, quantity=c_item.quantity, unit_price=prod.price, selected_colour=c_item.selected_colour, custom_spec=c_item.custom_spec)
                    prod.stock = max(0, prod.stock - c_item.quantity)
                    prod.save()
                cart.items.all().delete()
            messages.success(request, f'Order {order.order_number} confirmed!')
            return redirect('orders:order_confirmation', order_number=order.order_number)
    else:
        form = CheckoutForm(initial={
            'full_name': default_addr.recipient_name if default_addr else (request.user.profile.full_name or request.user.username),
            'email': request.user.email,
            'phone_number': default_addr.phone_number if default_addr else request.user.profile.phone_number,
            'delivery_address': default_addr.street_address if default_addr else '',
            'city': default_addr.city if default_addr else 'Hubballi',
            'state': default_addr.state if default_addr else 'Karnataka',
            'postal_code': default_addr.postal_code if default_addr else '580020',
            'payment_method': 'SIMULATED_CARD',
        })
    return render(request, 'checkout.html', {'cart': cart, 'items': items, 'form': form})

@login_required
def order_confirmation(request, order_number):
    return render(request, 'orders/confirmation.html', {'order': get_object_or_404(Order, order_number=order_number, user=request.user)})

@login_required
def order_detail(request, order_number):
    return render(request, 'orders/order_detail.html', {'order': get_object_or_404(Order, order_number=order_number, user=request.user)})

@login_required
@require_POST
def cancel_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.status in ['Pending', 'Confirmed']:
        order.status = 'Cancelled'
        order.save()
    return redirect('orders:order_detail', order_number=order.order_number)


def track_order_view(request):
    query_order = request.GET.get('order_number', '').strip().upper()
    tracked_order = None
    user_orders = []
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')

    if query_order:
        if request.user.is_authenticated:
            tracked_order = Order.objects.filter(order_number__iexact=query_order, user=request.user).prefetch_related('items').first()
        else:
            tracked_order = Order.objects.filter(order_number__iexact=query_order).prefetch_related('items').first()
        if not tracked_order:
            messages.error(request, f'No order found matching "{query_order}".')

    stages = ['Pending', 'Confirmed', 'Processing', 'Shipped', 'Delivered']
    current_stage_idx = 1
    if tracked_order:
        if tracked_order.status in stages:
            current_stage_idx = stages.index(tracked_order.status)
        elif tracked_order.status == 'Cancelled':
            current_stage_idx = -1

    return render(request, 'orders/track_order.html', {
        'query_order': query_order,
        'tracked_order': tracked_order,
        'user_orders': user_orders,
        'stages': stages,
        'current_stage_idx': current_stage_idx,
    })
