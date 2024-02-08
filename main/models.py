import string
from usermanager.models import User
from django.db import models
from jalali_date import date2jalali
import random


class Tag(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=225)
    subtitle = models.CharField(max_length=225, blank=True, null=True)
    image = models.FileField(upload_to='img/blog/', null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    ID_NO = models.CharField(max_length=225, blank=True, null=True, unique=True)

    def __str__(self):
        return self.title

    @property
    def jdate(self):
        return date2jalali(self.create_date)

    def save(self, *args, **kwargs):
        if not self.ID_NO:
            self.ID_NO = self.generate_random_code()
            super(Blog, self).save(*args, **kwargs)

    def generate_random_code(self):
        return 'BLG'+''.join(random.choices(string.digits, k=8))


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    image = models.FileField(upload_to='img/category')


class Item(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=128, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    ID_NO = models.CharField(max_length=225, blank=True, null=True, unique=True)
    image = models.FileField(upload_to='img/items', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.ID_NO:
            self.ID_NO = self.generate_random_code()
            super(Item, self).save(*args, **kwargs)


    def generate_random_code(self):
        return 'ITM'+''.join(random.choices(string.digits, k=8))


class Cart(models.Model):
    items = models.ManyToManyField(Item, through='CartItem')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    is_checked = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
