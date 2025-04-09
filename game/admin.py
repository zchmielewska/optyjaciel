from django.contrib import admin
from game import models


@admin.register(models.Post)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")