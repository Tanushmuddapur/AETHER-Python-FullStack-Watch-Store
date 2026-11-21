from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('watch/<slug:slug>/', views.product_detail, name='product_detail'),
    path('premium-vault/', views.premium_watches, name='premium_watches'),
    path('custom-mix/add/', views.add_custom_mix_to_cart, name='add_custom_mix_to_cart'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/move-to-cart/<int:item_id>/', views.move_wishlist_to_cart, name='move_wishlist_to_cart'),
    path('admin-console/', views.admin_console, name='admin_console'),
    path('admin-console/watch/save/', views.admin_save_watch, name='admin_save_watch'),
    path('admin-console/watch/delete/<int:product_id>/', views.admin_delete_watch, name='admin_delete_watch'),
    path('admin-console/order/status/<int:order_id>/', views.admin_update_order_status, name='admin_update_order_status'),
]
