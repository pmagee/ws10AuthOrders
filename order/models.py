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
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_items(self):
        return OrderItem.objects.filter(order=self)
    
    def adjust_stock(self, order_id):
        print('Order Id:',order_id)
        order_items = OrderItem.objects.filter(id=order_id) 
        print('Size',order_items.count())
        for oi in order_items:
            print('In here')
            product = Product.get(name = oi.product)
            product.quantity = p.quantity + oi.quantity
            product.save

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

