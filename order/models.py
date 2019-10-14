from django.db import models
from shop.models import Product

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    emailAddress = models.EmailField(max_length=250, blank=True)
    
    class Meta:
        db_table = 'Order'
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

