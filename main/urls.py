from django.urls import path, include
from .views import Shopview,item_list
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:product_id>', views.product_detail, name='product'),
    path('users/Cart/', views.cart_view, name='Cart'),
    path('decrease_cart_item_quantity/<cart_item_id>/<decrease_amount>/', views.decrease_cart_item_quantity, name='decrease'),
    path('increase_cart_item_quantity/<cart_item_id>/<increase_amount>/', views.increase_cart_item_quantity, name='increase'),
    path('delete_cart_item/<cart_item_id>/', views.delete_item, name='delete'),
    path('add_to_cart/<product_id>/<selectedColor>/', views.add_to_cart, name='add'),
    path('childcategory/<child_id>/', views.childcategory_finder, name='childfinder'),
    path('category/<category_id>/', views.categoryfinder, name='categoryfinder'),
    path('blog_detail/<blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/', views.blog, name='blog'),
    path('item_list/', views.item_list, name='item_list')
]
