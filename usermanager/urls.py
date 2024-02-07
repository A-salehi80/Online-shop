from django.contrib.auth import views
from usermanager.forms import UserLoginForm
from django.urls import include, path
from . import views as user

app_name = 'usermanager'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path('signup/', user.register, name='register'),
]



