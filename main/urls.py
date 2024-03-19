from django.urls import path, include
from .views import index
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:product_id>', views.product_detail, name='index'),
    path('users/Cart/', views.Cart_view, name='Cart')
]
