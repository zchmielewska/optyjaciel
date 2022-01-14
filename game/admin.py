import game.models
from django.contrib import admin


admin.site.register(game.models.Question)
admin.site.register(game.models.Quiz)
admin.site.register(game.models.QuizQuestion)
admin.site.register(game.models.Answer)
admin.site.register(game.models.Match)
admin.site.register(game.models.Suggestion)
admin.site.register(game.models.Message)
admin.site.register(game.models.Post)
