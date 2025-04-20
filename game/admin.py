from django.contrib import admin
from game import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "created_at")
