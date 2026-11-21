from django.contrib import admin
from .models import Category, Product, ProductImage, Wishlist, WishlistItem, Cart, CartItem, Review, ContactMessage, NewsletterSubscriber
admin.site.register([Category, Product, ProductImage, Wishlist, WishlistItem, Cart, CartItem, Review, ContactMessage, NewsletterSubscriber])
