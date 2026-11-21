import json
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='collections/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1000&q=85'

    def __str__(self):
        return self.name


class Product(models.Model):
    TIER_CHOICES = [
        ('Everyday & Affordable', 'Everyday & Affordable Brands'),
        ('Enthusiast & Mid-Range', 'Enthusiast & Mid-Range Brands'),
        ('Luxury & High-End', 'Luxury & High-End Brands'),
        ('Iconic & Established Luxury', 'Iconic & Established Luxury'),
        ('Ultra-Luxury & Haute Horlogerie', 'Ultra-Luxury & Haute Horlogerie'),
        ('Old Money Heritage', 'Old Money Watches'),
    ]

    AUDIENCE_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
        ('Unisex', 'Unisex'),
    ]

    MOVEMENT_CHOICES = [
        ('Automatic', 'Swiss / Japanese Automatic'),
        ('Mechanical', 'Manual Mechanical'),
        ('Quartz', 'Precision Quartz / Solar Eco-Drive'),
        ('Chronograph', 'Calibre Chronograph'),
        ('Tourbillon', 'Flying Tourbillon / Grand Complication'),
        ('Spring Drive', 'Spring Drive'),
    ]

    STRAP_CHOICES = [
        ('Alligator Leather', 'Alligator Leather'),
        ('Oyster / Integrated Steel', 'Oyster / Integrated Steel'),
        ('Brushed Titanium', 'Brushed Titanium'),
        ('Resin / FKM Rubber', 'Resin / FKM Rubber'),
        ('Milanese Mesh', 'Milanese Mesh'),
        ('Nato / Canvas', 'Nato / Canvas'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    brand = models.CharField(max_length=120, default='Rolex')
    brand_tier = models.CharField(max_length=60, choices=TIER_CHOICES, default='Luxury & High-End')
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='Men')
    is_old_money = models.BooleanField(default=False)
    is_premium_vault = models.BooleanField(default=False)

    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    original_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=10)

    # Interactive Color & Strap/Dial Mapping (JSON string mapping Color Name -> Image URL & Hex)
    available_colours = models.CharField(max_length=240, default='Midnight Teal, Platinum, Warm Ivory, Deep Charcoal')
    color_variants_json = models.TextField(
        blank=True,
        default='[{"name":"Midnight Teal","hex":"#102B2A","img":"https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1000&q=85"},{"name":"Platinum","hex":"#B8C4C2","img":"https://images.unsplash.com/photo-1547996160-81dfa63595aa?auto=format&fit=crop&w=1000&q=85"},{"name":"Warm Ivory","hex":"#F3F0E8","img":"https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=1000&q=85"},{"name":"Deep Charcoal","hex":"#17201F","img":"https://images.unsplash.com/photo-1539874754764-5a96559165b0?auto=format&fit=crop&w=1000&q=85"}]'
    )
    dial_colour = models.CharField(max_length=80, default='Midnight Teal')
    dial_detail_note = models.CharField(max_length=160, default='Sunray Guilloché Dial with Applied Indices')
    strap_material = models.CharField(max_length=80, choices=STRAP_CHOICES, default='Oyster / Integrated Steel')
    strap_detail_note = models.CharField(max_length=160, default='Micro-Adjustable Deployant Clasp')
    case_material = models.CharField(max_length=100, default='904L Oystersteel / Titanium')
    movement_type = models.CharField(max_length=80, choices=MOVEMENT_CHOICES, default='Automatic')
    water_resistance = models.CharField(max_length=60, default='100m / 10 ATM')
    dial_size = models.CharField(max_length=40, default='40 mm')

    primary_image = models.ImageField(upload_to='watches/', blank=True, null=True)
    primary_image_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)

    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    popularity_score = models.PositiveIntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand}-{self.name}")
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        if self.primary_image:
            return self.primary_image.url
        return self.primary_image_url or 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=1000&q=85'

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(round(((self.original_price - self.price) / self.original_price) * 100))
        return 0

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 4.9
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    @property
    def colour_list(self):
        return [c.strip() for c in self.available_colours.split(',') if c.strip()]

    @property
    def parsed_variants(self):
        try:
            data = json.loads(self.color_variants_json)
            if isinstance(data, list) and data:
                return data
        except Exception:
            pass
        return [
            {'name': 'Midnight Teal', 'hex': '#102B2A', 'img': self.get_image},
            {'name': 'Platinum', 'hex': '#B8C4C2', 'img': 'https://images.unsplash.com/photo-1547996160-81dfa63595aa?auto=format&fit=crop&w=1000&q=85'},
            {'name': 'Warm Ivory', 'hex': '#F3F0E8', 'img': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=1000&q=85'},
            {'name': 'Deep Charcoal', 'hex': '#17201F', 'img': 'https://images.unsplash.com/photo-1539874754764-5a96559165b0?auto=format&fit=crop&w=1000&q=85'},
        ]

    def __str__(self):
        return f"{self.brand} — {self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='watches/gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    caption = models.CharField(max_length=120, blank=True, default='Dial & Strap Macro View')

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    updated_at = models.DateTimeField(auto_now=True)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')
        ordering = ['-added_at']


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def original_subtotal(self):
        total = Decimal('0.00')
        for item in self.items.select_related('product'):
            unit = item.product.original_price if (item.product.original_price and item.product.original_price > item.product.price) else item.product.price
            total += unit * item.quantity
        return total

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.select_related('product'))

    @property
    def total_discount(self):
        return max(Decimal('0.00'), self.original_subtotal - self.subtotal)

    @property
    def shipping_charge(self):
        if self.subtotal == 0 or self.subtotal >= Decimal('5000.00'):
            return Decimal('0.00')
        return Decimal('199.00')

    @property
    def final_total(self):
        return self.subtotal + self.shipping_charge


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    selected_colour = models.CharField(max_length=120, blank=True)
    custom_spec = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def line_total(self):
        return self.product.price * self.quantity


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    title = models.CharField(max_length=140, default='Masterpiece Craftsmanship')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
