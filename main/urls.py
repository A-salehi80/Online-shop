from django.urls import path, include
from .views import index
from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='index')
]
