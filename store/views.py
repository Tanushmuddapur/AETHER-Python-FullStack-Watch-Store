from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.views.decorators.http import require_POST

from .models import (
    Category, Product, Wishlist, WishlistItem,
    Cart, CartItem, Review, NewsletterSubscriber
)
from orders.models import Order
from .forms import ReviewForm, ContactForm, NewsletterForm
from .seed import seed_aether_catalog


def home(request):
    seed_aether_catalog()
    collections = Category.objects.all()
    best_sellers = Product.objects.filter(is_best_seller=True)[:4]
    old_money_watches = Product.objects.filter(is_old_money=True)[:4]
    men_watches = Product.objects.filter(audience='Men')[:4]
    women_watches = Product.objects.filter(audience='Women')[:4]
    kids_watches = Product.objects.filter(audience='Kids')[:4]
    hero_watch = Product.objects.filter(brand='Rolex').first() or Product.objects.first()

    return render(request, 'home.html', {
        'collections': collections,
        'best_sellers': best_sellers,
        'old_money_watches': old_money_watches,
        'men_watches': men_watches,
        'women_watches': women_watches,
        'kids_watches': kids_watches,
        'hero_watch': hero_watch,
    })


def shop(request):
    seed_aether_catalog()
    products = Product.objects.select_related('category').all()

    q = request.GET.get('q', '').strip()
    collection_slug = request.GET.get('collection', '').strip()
    tier = request.GET.get('tier', '').strip()
    brand = request.GET.get('brand', '').strip()
    audience = request.GET.get('audience', '').strip()
    strap = request.GET.get('strap', '').strip()
    movement = request.GET.get('movement', '').strip()
    old_money = request.GET.get('old_money', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    sort = request.GET.get('sort', 'popularity').strip()

    # If collection == 'all' or empty, show all watches across all collections!
    if collection_slug and collection_slug != 'all':
        products = products.filter(category__slug=collection_slug)
    if tier and tier != 'all':
        products = products.filter(brand_tier__iexact=tier)
    if brand:
        products = products.filter(brand__iexact=brand)
    if audience and audience != 'all':
        products = products.filter(audience__iexact=audience)
    if old_money == '1':
        products = products.filter(is_old_money=True)
    if q:
        products = products.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q))
    if strap:
        products = products.filter(strap_material__iexact=strap)
    if movement:
        products = products.filter(movement_type__iexact=movement)
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-popularity_score', '-created_at')

    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'shop.html', {
        'page_obj': page_obj,
        'collections': Category.objects.all(),
        'tier_choices': Product.TIER_CHOICES,
        'audience_choices': Product.AUDIENCE_CHOICES,
        'brands': Product.objects.values_list('brand', flat=True).distinct().order_by('brand'),
        'strap_choices': Product.STRAP_CHOICES,
        'movement_choices': Product.MOVEMENT_CHOICES,
        'filters': {
            'q': q, 'collection': collection_slug or 'all', 'tier': tier,
            'brand': brand, 'audience': audience, 'old_money': old_money,
            'strap': strap, 'movement': movement,
            'min_price': min_price, 'max_price': max_price, 'sort': sort,
        },
    })


def product_detail(request, slug):
    seed_aether_catalog()
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)
    reviews = product.reviews.select_related('user').all()
    related_products = Product.objects.filter(Q(category=product.category) | Q(brand=product.brand)).exclude(id=product.id)[:4]

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please sign in to submit a collector review.')
            return redirect('accounts:login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.product = product
            rev.user = request.user
            rev.save()
            messages.success(request, 'Your collector review has been published.')
            return redirect('store:product_detail', slug=product.slug)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': form,
    })


# ==============================================================================
# ULTRA-LUXURY PREMIUM WATCHES VAULT (Segmented by Tiers + Old Money + Mix Studio)
# ==============================================================================
@login_required
def premium_watches(request):
    seed_aether_catalog()
    luxury_high_end = Product.objects.filter(brand_tier='Luxury & High-End').order_by('-price')
    iconic_luxury = Product.objects.filter(brand_tier='Iconic & Established Luxury').order_by('-price')
    ultra_luxury = Product.objects.filter(brand_tier='Ultra-Luxury & Haute Horlogerie').order_by('-price')
    old_money = Product.objects.filter(is_old_money=True).order_by('-price')
    all_watches = Product.objects.all().order_by('-price')

    return render(request, 'premium_watches.html', {
        'luxury_high_end': luxury_high_end,
        'iconic_luxury': iconic_luxury,
        'ultra_luxury': ultra_luxury,
        'old_money': old_money,
        'all_watches': all_watches,
    })


@login_required
@require_POST
def add_custom_mix_to_cart(request):
    seed_aether_catalog()
    base_watch_id = request.POST.get('base_watch_id')
    base_product = Product.objects.filter(id=base_watch_id).first() or Product.objects.filter(is_premium_vault=True).first() or Product.objects.first()

    theme_name = request.POST.get('theme_name', 'Midnight Teal')
    case_brand = request.POST.get('case_brand', 'Rolex 904L Oystersteel Case')
    dial_brand = request.POST.get('dial_brand', 'Grand Seiko Zaratsu Sunray Dial')
    calibre_brand = request.POST.get('calibre_brand', 'Patek Philippe Gyromax Calibre')
    strap_brand = request.POST.get('strap_brand', 'Cartier QuickSwitch Alligator Strap')
    engraving = request.POST.get('engraving', 'AETHER · 2026').strip() or 'AETHER · 2026'

    spec_summary = f"Theme: {theme_name} | Case: {case_brand} | Dial: {dial_brand} | Calibre: {calibre_brand} | Strap: {strap_brand} | Engraving: '{engraving}'"

    cart, _ = Cart.objects.get_or_create(user=request.user)
    CartItem.objects.create(
        cart=cart,
        product=base_product,
        quantity=1,
        selected_colour=f"Bespoke Brand Mix ({theme_name})",
        custom_spec=spec_summary,
    )
    messages.success(request, f'Custom mixed watch ({theme_name}) added to your Shopping Bag!')
    return redirect('store:cart')


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been received by the AETHER Concierge Desk.')
            return redirect('store:contact')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'full_name': getattr(request.user.profile, 'full_name', request.user.username),
                'email': request.user.email,
            }
        form = ContactForm(initial=initial)
    return render(request, 'contact.html', {'form': form})


@require_POST
def subscribe_newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email'].lower()
        _, created = NewsletterSubscriber.objects.get_or_create(email=email)
        messages.success(request, 'Welcome to the AETHER Private Circle.' if created else 'You are already subscribed.')
    else:
        messages.error(request, 'Please provide a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'store:home'))


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product', 'product__category').all()
    return render(request, 'cart.html', {'cart': cart, 'items': items})


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock < 1:
        messages.error(request, f'{product.name} is currently out of stock.')
        return redirect(request.META.get('HTTP_REFERER', 'store:shop'))

    qty = max(1, min(int(request.POST.get('quantity', 1)), product.stock))
    colour = request.POST.get('selected_colour', '') or product.dial_colour
    custom_spec = request.POST.get('custom_spec', '')
    buy_now = request.POST.get('buy_now') == '1'

    cart, _ = Cart.objects.get_or_create(user=request.user)
    existing = CartItem.objects.filter(cart=cart, product=product, selected_colour=colour, custom_spec=custom_spec).first()
    if existing:
        existing.quantity = min(product.stock, existing.quantity + qty)
        existing.save()
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=qty, selected_colour=colour, custom_spec=custom_spec)

    if buy_now:
        return redirect('orders:checkout')

    messages.success(request, f'Added "{product.brand} {product.name}" to your Shopping Bag.')
    return redirect(request.META.get('HTTP_REFERER', 'store:cart'))


@login_required
@require_POST
def update_cart_quantity(request, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    action = request.POST.get('action')
    if action == 'increase' and item.quantity < item.product.stock:
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    return redirect('store:cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    get_object_or_404(CartItem, id=item_id, cart=cart).delete()
    messages.info(request, 'Item removed from Shopping Bag.')
    return redirect('store:cart')


@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product', 'product__category').all()
    return render(request, 'wishlist.html', {'wishlist': wishlist, 'items': items})


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    existing = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if existing:
        existing.delete()
        messages.info(request, f'Removed "{product.name}" from Wishlist.')
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f'Saved "{product.name}" to Wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'store:wishlist'))


@login_required
@require_POST
def move_wishlist_to_cart(request, item_id):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    w_item = get_object_or_404(WishlistItem, id=item_id, wishlist=wishlist)
    product = w_item.product
    if product.stock < 1:
        messages.error(request, f'{product.name} is out of stock.')
        return redirect('store:wishlist')
    cart, _ = Cart.objects.get_or_create(user=request.user)
    CartItem.objects.create(cart=cart, product=product, quantity=1, selected_colour=product.dial_colour)
    w_item.delete()
    messages.success(request, f'Moved "{product.name}" to your Shopping Bag.')
    return redirect('store:cart')


def is_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_console(request):
    seed_aether_catalog()
    products = Product.objects.select_related('category').all().order_by('-created_at')
    orders = Order.objects.select_related('user').prefetch_related('items').all().order_by('-created_at')
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    categories = Category.objects.all()
    total_revenue = orders.aggregate(total=Sum('final_amount'))['total'] or Decimal('0.00')

    return render(request, 'admin_console.html', {
        'products': products,
        'orders': orders,
        'users': users,
        'categories': categories,
        'tier_choices': Product.TIER_CHOICES,
        'audience_choices': Product.AUDIENCE_CHOICES,
        'total_revenue': total_revenue,
    })


@login_required
@user_passes_test(is_admin)
@require_POST
def admin_save_watch(request):
    watch_id = request.POST.get('watch_id', '').strip()
    cat = get_object_or_404(Category, id=request.POST.get('category_id'))

    prod = get_object_or_404(Product, id=watch_id) if watch_id else Product()
    prod.category = cat
    prod.name = request.POST.get('name')
    prod.brand = request.POST.get('brand', 'AETHER Genève')
    prod.brand_tier = request.POST.get('brand_tier', 'Luxury & High-End')
    prod.audience = request.POST.get('audience', 'Men')
    prod.price = Decimal(request.POST.get('price', '125000'))
    orig = request.POST.get('original_price', '').strip()
    prod.original_price = Decimal(orig) if orig else None
    prod.stock = int(request.POST.get('stock', 5))
    prod.dial_colour = request.POST.get('dial_colour', 'Midnight Teal')
    prod.case_material = request.POST.get('case_material', 'Grade-5 Titanium')
    prod.primary_image_url = request.POST.get('primary_image_url', '')
    prod.video_url = request.POST.get('video_url', '')
    prod.description = request.POST.get('description', '')
    prod.is_premium_vault = request.POST.get('is_premium_vault') == '1'
    prod.is_old_money = request.POST.get('is_old_money') == '1'
    if request.FILES.get('primary_image'):
        prod.primary_image = request.FILES['primary_image']
    prod.save()

    messages.success(request, f'Timepiece "{prod.brand} {prod.name}" saved!')
    return redirect('store:admin_console')


@login_required
@user_passes_test(is_admin)
@require_POST
def admin_delete_watch(request, product_id):
    prod = get_object_or_404(Product, id=product_id)
    name = prod.name
    prod.delete()
    messages.info(request, f'Deleted "{name}" from catalog.')
    return redirect('store:admin_console')


@login_required
@user_passes_test(is_admin)
@require_POST
def admin_update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = request.POST.get('status', order.status)
    order.save()
    messages.success(request, f'Order {order.order_number} updated to {order.status}.')
    return redirect('store:admin_console')


def not_found(request, exception):
    return render(request, '404.html', status=404)
