from django.urls import path
from . import views 


urlpatterns = [
    path('', views.product_list,
            name='products'),
    path('<int:category_id>/', views.product_list,
            name='product_list_by_category'),
]

