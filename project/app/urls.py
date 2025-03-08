from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    
    # Main Pages
    path('home/', views.home, name='home'),
    path('women/', views.women, name='women'),
    path('men/', views.men, name='men'),
    path('kids/', views.kids, name='kids'),
    path('sale/', views.sale, name='sale'),
    path('contact/', views.contact, name='contact'),

    # Cart Functionality
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout & Payment
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    
]