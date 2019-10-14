from django.shortcuts import render
from .models import OrderItem, Order
from cart.models import Cart, CartItem
from cart.views import _cart_id
from shop.models import Product
from django.core.exceptions import ObjectDoesNotExist

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
