import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('SIMULATED_CARD', 'AETHER Vault Instant Card / UPI (Simulated)'),
        ('COD', 'Cash on Delivery (Concierge Handover)'),
    ]

    order_number = models.CharField(max_length=24, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=25)
    delivery_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    offer_code = models.CharField(max_length=60, blank=True)
    offer_discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)

    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='SIMULATED_CARD')
    payment_status = models.CharField(max_length=50, default='Paid · AETHER Vault Settlement')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ATH-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    selected_colour = models.CharField(max_length=120, blank=True)
    custom_spec = models.TextField(blank=True)

    @property
    def line_total(self):
        return self.unit_price * self.quantity
