from game import forms, models
from game.utils import transform, utils
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import Http404, QueryDict
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView


class RulesView(View):
    def get(self, request):
        return render(request, "rules.html")


class GameView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        quiz = utils.get_current_quiz()
        played = len(models.Match.objects.filter(quiz=quiz, user=user)) > 0

        if not played:
            quiz_questions = quiz.quizquestion_set.order_by("question_index")
            ctx = {
                "quiz": quiz,
                "quiz_questions": quiz_questions,
            }
            return render(request, 'game_quiz.html', ctx)
        else:
            ctx = utils.get_match_context(quiz, user)
            ctx["remaining_time_in_week"] = utils.get_remaining_time_in_week()
            return render(request, "game_match.html", ctx)

    def post(self, request):
        user = request.user
        post = QueryDict.dict(request.POST)
        post.pop("csrfmiddlewaretoken")
        quiz_id = post.pop("quiz_id")
        quiz = models.Quiz.objects.get(id=quiz_id)

        # Saving answers and recalculation of matches must happen simultaneously
        with transaction.atomic():
            for key, value in post.items():
                models.Answer.objects.create(
                    user=request.user,
                    quiz_question_id=key,
                    answer=value
                )
            transform.recalculate_and_save_matches(quiz)

        ctx = utils.get_match_context(quiz, user)
        ctx["remaining_time_in_week"] = utils.get_remaining_time_in_week()
        return render(request, "game_match.html", ctx)


class CompatibilityView(View):
    def get(self, request, quiz_id, user1_id, user2_id):
        quiz = models.Quiz.objects.get(id=quiz_id)
        user1 = User.objects.get(id=user1_id)
        user2 = User.objects.get(id=user2_id)
        quiz_questions = quiz.quizquestion_set.order_by("question_index")

        elements = []
        for quiz_question in quiz_questions:
            question = quiz_question.question.question
            answer1 = utils.get_text_answer(quiz_question, user1)
            answer2 = utils.get_text_answer(quiz_question, user2)
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
        matches = utils.get_matches_context(user)
        return render(request, "previous_matches.html", {"matches": matches})


class SuggestionView(LoginRequiredMixin, FormView):
    template_name = "suggest.html"
    form_class = forms.SuggestionForm
    success_url = "/"

    def form_valid(self, form):
        question = form.cleaned_data.get("question")
        option1 = form.cleaned_data.get("option1")
        option2 = form.cleaned_data.get("option2")
        option3 = form.cleaned_data.get("option3")
        option4 = form.cleaned_data.get("option4")

        models.Suggestion.objects.create(
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
        form = forms.RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
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
        form = forms.LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
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


class MessageInboxView(LoginRequiredMixin, View):
    def get(self, request):
        messages_in = models.Message.objects.filter(to_user=request.user).order_by("-sent_at")
        return render(request, "message_inbox.html", {"messages_in": messages_in})


class MessageOutboxView(LoginRequiredMixin, View):
    def get(self, request):
        messages_out = models.Message.objects.filter(from_user=request.user).order_by("-sent_at")
        return render(request, "message_outbox.html", {"messages_out": messages_out})


class MessageWriteView(LoginRequiredMixin, View):
    def get(self, request, to_user_id=0):
        if to_user_id == 0:
            matches = utils.get_matches_queryset(request.user)
            form = forms.MessageForm()
        else:
            match = User.objects.get(id=to_user_id)
            matches = User.objects.filter(id=match.id)
            form = forms.MessageForm(initial={"to_user": match})
        form.fields["to_user"].queryset = matches
        no_matches = matches.count()
        ctx = {
            "form": form,
            "no_matches": no_matches,
        }
        return render(request, "message_write.html", ctx)

    def post(self, request):
        form = forms.MessageForm(request.POST)
        if form.is_valid():
            to_user = form.cleaned_data.get("to_user")
            title = form.cleaned_data.get("title")
            body = form.cleaned_data.get("body")
            models.Message.objects.create(
                from_user=self.request.user,
                to_user=to_user,
                title=title,
                body=body,
            )
            return redirect("message-outbox")


class MessageReadView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        message = models.Message.objects.get(id=message_id)

        if request.user == message.to_user:
            msg_type = "in"
        elif request.user == message.from_user:
            msg_type = "out"
        else:
            raise Http404("Wiadomość nie istnieje.")

        if msg_type == "in" and message.new:
            message.new = False
            message.save()

        ctx = {
            "msg_type": msg_type,
            "message": message,
        }
        return render(request, "message_read.html", ctx)
