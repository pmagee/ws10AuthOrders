from django.db import models
from shop.models import Product
from django.shortcuts import get_object_or_404
from decimal import Decimal

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    emailAddress = models.EmailField(max_length=250, blank=True)
    
    class Meta:
        db_table = 'Order'
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_items(self):
        return OrderItem.objects.filter(order=self)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

