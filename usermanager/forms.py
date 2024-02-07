from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
               'data-placeholder': 'شماره موبایل یا ایمیل',
               'id': 'username',
               'type': 'text',
               'dir': "auto",
               'style': 'height:40px'
               }))
    password = forms.CharField(
        widget=forms.PasswordInput(
         attrs={
            'class': 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder': 'شماره موبایل یا ایمیل',
            'id': 'password',
            'type': 'text',
            'dir': "auto"

        }))