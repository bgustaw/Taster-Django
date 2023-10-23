from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from Taster.models import Recipe, Country
from .managers import CustomUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), unique=True, max_length=30, validators=[username_validator],
                                error_messages={
                                    "unique": _("A user with that username already exists."),
                                }, )
    country = models.ForeignKey(Country, max_length=40, blank=True, null=True, default='', on_delete=models.SET_NULL)
    liked_recipes = models.ManyToManyField(Recipe, default='', blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_country(self):
        return self.country

    def get_liked_recipes(self):
        return self.liked_recipes.all()


