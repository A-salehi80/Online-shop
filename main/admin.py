from django.contrib import admin
from .models import Blog, Tag, Category, Item, Cart, CartItem
from tiny.widgets import TinyMCE
from django.db import models




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
admin.site.register(Cart)
admin.site.register(CartItem)