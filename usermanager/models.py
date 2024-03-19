from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, PermissionManager,UserManager, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from main.models import Cart



class User(AbstractBaseUser, PermissionsMixin, PermissionManager):
    email = models.EmailField(blank=True, null=True)
    groups = models.OneToOneField(Group, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=20, unique=True, validators=[UnicodeUsernameValidator()],)
    USERNAME_FIELD = 'username'
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)      # a admin user; non super-user
    admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the object is being created for the first time
        super(User, self).save(*args, **kwargs)  # Save the current object

        if created:  # If the object is being created
            # Create a profile object for the user associated with the blog
            cart = Cart.objects.create()
            Profile.objects.create(user=self, cart=cart)





def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'userdata/User_{0}/{1}'.format(instance.national_id, str(instance.first_name)+str(instance.last_name)+'.jpg')


class Profile(models.Model):
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    GENDER_STATUS = (
        (1, "MALE"),
        (2, "PREFER NOT TO SAY"),
        (3, "FEMALE"),
    )
    gender = models.SmallIntegerField(choices=GENDER_STATUS, blank=True, null=True)
    address = models.CharField(max_length=225, blank=True, null=True)
    national_id = models.CharField(max_length=15, unique=True,blank=True,null=True)
    profile = models.FileField(upload_to=user_directory_path)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        user = self.user
        user = str(user)
        return user
















# Create your models here.
