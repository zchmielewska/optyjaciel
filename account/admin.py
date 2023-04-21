from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

import account.models

# Alter default user admin
UserAdmin.list_display = ("id", "username", "email", "is_active")
UserAdmin.ordering = ("-id", )


@admin.register(account.models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname")
    ordering = ("-id",)
