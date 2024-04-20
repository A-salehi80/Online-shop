from django.shortcuts import render
from rest_framework import generics, permissions
from main.models import Item
from .serializers import Item_Serializer
# Create your views here.


class ItemApi(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = Item_Serializer
    permission_classes = (permissions.IsAuthenticated,)
