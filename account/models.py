from django.contrib.auth.models import User

# Changes to the built-in User model
# User._meta.get_field('email')._unique = True
# User._meta.get_field('email').blank = False
# User._meta.get_field('email').null = False
