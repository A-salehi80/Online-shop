from django.shortcuts import render
from .models import Blog


def index(request):
    blog = Blog.objects.all()

    context = {
        'blog': blog,
    }
    return render(request, 'index.html', context)


# Create your views here.
