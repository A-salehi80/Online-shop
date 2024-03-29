from django.contrib import admin
from .models import Blog, Tag, Category, Item, Cart, CartItem, Main_Page, Large_banner, Colors, SubCategory,ChildCategory
from tiny.widgets import TinyMCE
from django.db import models


class Cartinline(admin.TabularInline):
    model = CartItem


class Cartadmin (admin.ModelAdmin):
    inlines = (Cartinline,)


class EditorAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    readonly_fields = ('ID_NO',)

    formfield_overrides = {
            models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Blog, EditorAdmin)
admin.site.register(Category)
admin.site.register(Item, EditorAdmin)
admin.site.register(Tag)
admin.site.register(Cart,Cartadmin)
admin.site.register(CartItem)
admin.site.register(Main_Page)
admin.site.register(Large_banner)
admin.site.register(Colors)
admin.site.register(SubCategory)
admin.site.register(ChildCategory)