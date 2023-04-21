from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Changes to the built-in User model
# User._meta.get_field('email').blank = False
# User._meta.get_field('email').null = False


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=150)
