import game.models
from django.contrib import admin


admin.site.register(game.models.Quiz)
admin.site.register(game.models.Question)
admin.site.register(game.models.QuizQuestion)
