from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model, password_validation

import usermanager.models


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 '
                        'placeholder-transparent focus:outline-none ''focus:ring-0 dark:text-primary-light',
               'data-placeholder': 'شماره موبایل یا ایمیل',
               'id': 'username',
               'type': 'text',
               'dir': "auto",
               'style': 'height:40px'
               }))
    password = forms.CharField(
        widget=forms.PasswordInput(
         attrs={
            'class': 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700'
                     ' placeholder-transparent ''focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder': 'شماره موبایل یا ایمیل',
            'id': 'password',
            'type': 'text',
            'dir': "auto"

        }))


class UserRegBase(forms.ModelForm):
    """
     A form that creates a user, with no privileges, from the given username and
     password.
     """

    error_messages = {
        "password_mismatch": _("رمزعبور با تکرارش همخوانی ندارد."),
        "existed_user": _("کاربری با این نام کاربری موجود است.لطفا نام کاربری را تغییر دهید"),
        "password_short": _("")


    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "id": "password1"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "id": "password2"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    email = forms.EmailField(
        label=_("email"),
        widget=forms.EmailInput(attrs={"id": "email"})
    )
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "username"}))

    class Meta:
        model = usermanager.models.User
        fields = ("username", "email")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user


class UserCreationForm(UserRegBase):
    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (
                username
                and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.error_messages['existed_user']
                    }
                )
            )
        else:
            return username
