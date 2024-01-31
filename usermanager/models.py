from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, PermissionManager,UserManager, Group
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractBaseUser, PermissionsMixin, PermissionManager):
    email = models.EmailField( max_length=80)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=20
                                , unique=True,
                                validators=[UnicodeUsernameValidator()],

                                )
    USERNAME_FIELD = 'username'
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)      # a admin user; non super-user
    admin = models.BooleanField(default=False)











# Create your models here.
