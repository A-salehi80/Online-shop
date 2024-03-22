import string

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
        super(Blog, self).save(*args, **kwargs)
    def generate_random_code(self):
        return 'BLG'+''.join(random.choices(string.digits, k=8))


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    image = models.FileField(upload_to='img/category')

    def __str__(self):
        return self.name


class Colors(models.Model):
    color_fa = models.CharField(max_length=40)
    color_en = models.CharField(max_length=40)
    color_tag = models.CharField(max_length=9)

    def __str__(self):
        return self.color_fa


class Item(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=128, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    ID_NO = models.CharField(max_length=225, blank=True, null=True, unique=True)
    image1 = models.FileField(upload_to='img/items')
    image2 = models.FileField(upload_to='img/items', blank=True, null=True)
    image3 = models.FileField(upload_to='img/items', blank=True, null=True)
    image4 = models.FileField(upload_to='img/items', blank=True, null=True)
    color = models.ManyToManyField(Colors)

    def save(self, *args, **kwargs):
        if not self.ID_NO:
            self.ID_NO = self.generate_random_code()
            super(Item, self).save(*args, **kwargs)

        super(Item, self).save(*args, **kwargs)

    def generate_random_code(self):
        return 'ITM'+''.join(random.choices(string.digits, k=8))

    def __str__(self):
        return self.name


class Cart(models.Model):
    items = models.ManyToManyField(Item, through='CartItem')
    address = models.TextField(blank=True, null=True)
    is_checked = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)

    def __str__(self):
        user = str(self.profile.user)+'s Cart'
        return user


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE,blank=True, null=True)

    def save(self,*args, **kwargs):
        color = Colors.objects.filter(item=self.item).first()
        existing_cart_item = CartItem.objects.filter(item=self.item, cart=self.cart,color=self.color).first()
        if existing_cart_item:
            existing_cart_item.quantity = self.quantity+existing_cart_item.quantity
            super(CartItem, existing_cart_item).save(*args, **kwargs)
        else:
            super(CartItem, self).save()

        if color.id == self.color.id:

            super(CartItem, self).save(*args, **kwargs)

        else:
            raise ValueError('رنگ مورد نظر با رنگ های محصول همخوانی ندارد')

    def __str__(self):

        a=self.item.name
        return a


class Main_Page(models.Model):
    main_banner = models.FileField(upload_to='img/mainpage')
    main_banner_link = models.CharField(max_length=125, blank=True, null=True)
    main_gif = models.FileField(upload_to='img/mainpage')
    main_gif_link = models.CharField(max_length=125, blank=True, null=True)
    X_link = models.CharField(max_length=125, blank=True, null=True)
    Aparat_link = models.CharField(max_length=125, blank=True, null=True)
    IG_link = models.CharField(max_length=125, blank=True, null=True)
    Phone_no = models.CharField(max_length=125, blank=True, null=True)
    ad_1_link = models.CharField(max_length=125, blank=True, null=True)
    ad_1 = models.FileField(upload_to='img/mainpage', blank=True, null=True)
    ad_2_link = models.CharField(max_length=125, blank=True, null=True)
    ad_2 = models.FileField(upload_to='img/mainpage', blank=True, null=True)


class Large_banner(models.Model):
    banner = models.FileField(upload_to='img/mainpage')
    link = models.CharField(max_length=125, blank=True, null=True)




