from .models import Cart, Wishlist, Category

def global_nav_counts(request):
    cart_count = 0
    wishlist_count = 0
    wishlist_product_ids = []
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        cart_count = cart.total_items
        wishlist_product_ids = list(wishlist.items.values_list('product_id', flat=True))
        wishlist_count = len(wishlist_product_ids)
    return {
        'nav_cart_count': cart_count,
        'nav_wishlist_count': wishlist_count,
        'wishlist_product_ids': wishlist_product_ids,
        'nav_collections': Category.objects.all(),
    }
