from rest_framework import serializers
from usermanager.models import Profile, User
from main.models import Blog, Item, CartItem, Cart, Colors, Category, ChildCategory, SubCategory

class Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'price', 'category', 'detail', 'brand',
                  'image1', 'image2', 'image3', 'image4', 'ID_NO', 'model', 'tags')
