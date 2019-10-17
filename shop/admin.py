from django.contrib import admin

from .models import Product, Category

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category','image','image_thumbnail','description','stock','price')
