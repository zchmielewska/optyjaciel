import pandas as pd
from django.urls import reverse_lazy

import game.utils.solver
import game.utils.transform
import game.utils.utils
import django.utils.timezone
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, CreateView


class RulesView(View):
    def get(self, request):
        return render(request, "rules.html")


class GameView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        quiz = game.utils.utils.get_current_quiz()
        played = len(Match.objects.filter(quiz=quiz, user=user)) > 0

        if not played:
            quiz_questions = quiz.quizquestion_set.order_by("question_index")
            ctx = {
                "quiz": quiz,
                "quiz_questions": quiz_questions,
            }
            return render(request, 'game_quiz.html', ctx)
        else:
            ctx = game.utils.utils.get_match_context(quiz, user)
            ctx["remaining_time_in_week"] = game.utils.utils.get_remaining_time_in_week()
            return render(request, "game_match.html", ctx)

    def post(self, request):
        user = request.user
        post = QueryDict.dict(request.POST)
        post.pop("csrfmiddlewaretoken")
        quiz_id = post.pop("quiz_id")
        quiz = Quiz.objects.get(id=quiz_id)

        with transaction.atomic():
            # Add user's answers to db
            for key, value in post.items():
                Answer.objects.create(
                    user=request.user,
                    quiz_question_id=key,
                    answer=value
                )
            game.utils.transform.recalculate_and_save_matches(quiz)

        ctx = game.utils.utils.get_match_context(quiz, user)
        ctx["remaining_time_in_week"] = game.utils.utils.get_remaining_time_in_week()
        return render(request, "game_match.html", ctx)


class CompatibilityView(View):
    def get(self, request, quiz_id, user1_id, user2_id):
        quiz = Quiz.objects.get(id=quiz_id)
        user1 = User.objects.get(id=user1_id)
        user2 = User.objects.get(id=user2_id)
        quiz_questions = quiz.quizquestion_set.order_by("question_index")

        elements = []
        for quiz_question in quiz_questions:
            question = quiz_question.question.question
            answer1 = game.utils.utils.get_text_answer(quiz_question, user1)
            answer2 = game.utils.utils.get_text_answer(quiz_question, user2)
            elements.append((question, answer1, answer2))

        ctx = {
            "quiz": quiz,
            "user1": user1,
            "user2": user2,
            "elements": elements,
        }
        return render(request, "compatibility.html", ctx)


class MatchesView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        current_quiz = game.utils.utils.get_current_quiz()

        # User might have participated only in few historical quizes
        answers = Answer.objects.filter(user=user)
        quiz_questions = [answer.quiz_question for answer in answers]
        quizes = []
        for quiz_question in quiz_questions:
            if quiz_question.quiz not in quizes and quiz_question.quiz != current_quiz:
                quizes.append(quiz_question.quiz)

        matches = []
        for quiz in quizes:
            match = game.utils.utils.get_match_context(quiz, user, nest=False)
            matches.append(match)

        return render(request, "previous_matches.html", {"matches": matches})


class SuggestionView(LoginRequiredMixin, FormView):
    template_name = "suggest.html"
    form_class = SuggestionForm
    success_url = "/"

    def form_valid(self, form):
        question = form.cleaned_data.get("question")
        option1 = form.cleaned_data.get("option1")
        option2 = form.cleaned_data.get("option2")
        option3 = form.cleaned_data.get("option3")
        option4 = form.cleaned_data.get("option4")

        Suggestion.objects.create(
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            user=self.request.user,
        )

        return redirect("thanks")


class ThanksView(View):
    def get(self, request):
        return render(request, "thanks.html")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            username_is_taken = username in User.objects.values_list("username", flat=True)
            if username_is_taken:
                form.add_error("username", "Ta nazwa użytkownika jest już zajęta :-(")
                return render(request, "register.html", {"form": form})

            user = User.objects.create_user(username=username, email=None, password=password)
            login(request, user)
            return redirect("rules")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                url_next = request.GET.get("next", "/")
                return redirect(url_next)
            else:
                form.add_error("username", "Nieprawidłowa nazwa użytkownika lub hasło.")
                return render(request, "login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("rules")


class MessageListView(View):
    def get(self, request):
        messages_in = Message.objects.filter(to_user=request.user)
        messages_out = Message.objects.filter(from_user=request.user)
        ctx = {
            "messages_in": messages_in,
            "messages_out": messages_out,
        }
        return render(request, "message_list.html", ctx)


class MessageWriteView(LoginRequiredMixin, FormView):
    template_name = "message_write.html"
    form_class = MessageForm
    success_url = "/"

    def form_valid(self, form):
        to_user = form.cleaned_data.get("to_user")
        title = form.cleaned_data.get("title")
        body = form.cleaned_data.get("body")
        Message.objects.create(
            from_user=self.request.user,
            to_user=to_user,
            title=title,
            body=body,
        )
        return redirect("thanks")


class MessageReadView(View):
    def get(self, request, message_id):
        message = Message.objects.get(id=message_id)
        return render(request, "message_read.html", {"message": message})

