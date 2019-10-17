from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order
from cart.models import Cart, CartItem
from cart.views import _cart_id
from shop.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.contrib import messages

@login_required()
def order_create(request, total=0, cart_items = None):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.create(emailAddress = email)
        order_details.save()
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for order_item in cart_items:
            oi = OrderItem.objects.create(
                    product = order_item.product.name,
                    quantity = order_item.quantity,
                    price = order_item.product.price,
                    order = order_details)
            total += (order_item.quantity * order_item.product.price)
            oi.save()
        
            '''Reduce stock when order is placed or saved'''
            products = Product.objects.get(id=order_item.product.id)
            if products.stock > 0:
                products.stock = int(order_item.product.stock - order_item.quantity)
            products.save()
            order_item.delete()
    except ObjectDoesNotExist:
        pass
    return render(request, 'order.html', dict(cart_items = cart_items, total=total))

@login_required()
def order_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(emailAddress=email)
    return render(request, 'orders_list.html', {'order_details':order_details})

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_date = order.created
    current_date = datetime.now(timezone.utc)
    date_diff = current_date - order_date
    minutes_diff = date_diff.total_seconds() / 60.0
    if minutes_diff <= 30:      
        order.adjust_stock(order_id)
        order.delete()
        messages.add_message(request, messages.INFO, 
					'Order is now cancelled')
    else:
        messages.add_message(request, messages.INFO, 
					'Sorry, it is too late to cancel this order')
    return redirect('order_history')


