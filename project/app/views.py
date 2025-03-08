from django.shortcuts import render, redirect, get_object_or_404
from .models import Users, Product, Cart, Order, OrderItem
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import Payment, Order
# ✅ User Authentication
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Users.objects.get(email=email)
            if check_password(password, user.password):
                auth_login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid password'})
        except Users.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email does not exist'})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        hashed_password = make_password(password)
        user = Users(fname=fname, lname=lname, email=email, password=hashed_password)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

def home(request):
    products = Product.objects.all()  # Fetch all products for the homepage
    return render(request, 'home.html', {'products': products})

# ✅ Product Pages
def women(request):
    products = Product.objects.filter(category="Women")
    return render(request, 'women.html', {'products': products})

def men(request):
    products = Product.objects.filter(category="Men")
    return render(request, 'men.html', {'products': products})

def kids(request):
    products = Product.objects.filter(category="Kids")
    return render(request, 'kids.html', {'products': products})

def sale(request):
    products = Product.objects.filter(category="Sale")
    return render(request, 'sale.html', {'products': products})

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# ✅ Contact Page
def contact(request):
    return render(request, 'contact.html')

# ✅ Cart Functionality

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

# ✅ Checkout & Payment


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        # Create an order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Add cart items to order
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        
        # Clear the cart after checkout
        cart_items.delete()

        # Redirect to payment
        return redirect('payment', order_id=order.id)

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def payment(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        transaction_id = get_random_string(12)  # Generate a random transaction ID

        # Create a payment record
        payment = Payment.objects.create(
            user=request.user,
            order=order,
            method=payment_method,
            transaction_id=transaction_id,
            amount_paid=order.total_price,
            success=True,  # Assuming payment is successful for now
        )

        # Update order status to Paid
        order.payment_status = True
        order.status = "Shipped"
        order.save()

        return redirect('home')

    return render(request, 'payment.html', {'order': order})