from django.contrib import admin
from .models import Blog, Tag, Category
from tiny.widgets import TinyMCE
from django.db import models

admin.site.register(Tag)


class TextEditorAdmin(admin.ModelAdmin):

    list_display = ["__str__"]
    formfield_overrides = {
     models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Blog, TextEditorAdmin)
admin.site.register(Category, TextEditorAdmin)
