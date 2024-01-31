from django.db import models
from jalali_date import date2jalali


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

    def __str__(self):
        return self.title

    @property
    def jdate(self):
        return date2jalali(self.create_date)


class Category(models.Model):
    name = models.CharField(max_length=125, unique=True)
    image = models.FileField(upload_to='img/category')


class Item(models.Model):
    name = models.CharField(max_length=125)
    price = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    detail = models.TextField()

