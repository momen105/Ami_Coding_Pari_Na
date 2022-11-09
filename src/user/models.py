from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """
    This is the manager for custom user model
    """

    def create_user(self, username, password=None):

        if not username:
            raise ValueError("Username should not be empty")
        if not password:
            raise ValueError("Password should not be empty")

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model Class
    """

    username = models.CharField(
        max_length=100, verbose_name="Username", unique=True, blank=False
    )
    is_staff = models.BooleanField(
        verbose_name="Staff Status",
        default=False,
        help_text="Designate if the user has " "staff status",
    )
    is_active = models.BooleanField(
        verbose_name="Active Status",
        default=True,
        help_text="Designate if the user has " "active status",
    )
    is_superuser = models.BooleanField(
        verbose_name="Superuser Status",
        default=False,
        help_text="Designate if the " "user has superuser " "status",
    )
    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username


class SearchModel(models.Model):
    """
    Model to store user search data
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="search_user")
    input_values = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
