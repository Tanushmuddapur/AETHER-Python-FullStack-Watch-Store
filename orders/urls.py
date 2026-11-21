from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('track/', views.track_order_view, name='track_order'),
    path('confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('detail/<str:order_number>/', views.order_detail, name='order_detail'),
    path('cancel/<str:order_number>/', views.cancel_order, name='cancel_order'),
]
