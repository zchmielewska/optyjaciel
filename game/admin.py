from django.contrib import admin

import game.models


@admin.register(game.models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz_question", "answer")


@admin.register(game.models.Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("quiz", "user", "matched_user", "matched_at")
    ordering = ("-matched_at",)


@admin.register(game.models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "title", "sent_at")
    ordering = ("-sent_at",)


@admin.register(game.models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "option1", "option2")


@admin.register(game.models.QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "question", "question_index")
    ordering = ("-quiz", "question_index")


@admin.register(game.models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("year", "week")
    ordering = ("-year", "-week")


@admin.register(game.models.Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "option1", "option2", "suggested_at")
    ordering = ("-suggested_at",)


@admin.register(game.models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created",)
    ordering = ("-created",)
    prepopulated_fields = {"slug": ("title",)}

