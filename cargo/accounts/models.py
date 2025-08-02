from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

from accounts.utils import generate_next_auth_key


class CustomUserManager(BaseUserManager):
    def create_user(self, gmail, phone_number, first_name, last_name):
        if not gmail:
            raise ValueError("The Gmail field is required")
        user = self.model(
            gmail=self.normalize_email(gmail),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, gmail, phone_number, first_name, last_name, password=None):
        user = self.create_user(
            gmail=gmail,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    gmail = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    auth_key = models.CharField(max_length=5, unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'gmail'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    def __str__(self):
        return self.gmail

    def __int__(self):
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def change_password(self, new_password):
        return True

    class Meta:
        ordering = ['auth_key']

    def save(self, *args, **kwargs):
        if not self.auth_key:
            self.auth_key = generate_next_auth_key()
        super().save(*args, **kwargs)
