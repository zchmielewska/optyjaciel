from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.db import transaction
from django.http import Http404, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from random import sample

from game import forms, models
from game.utils import db_control, transform


class RulesView(View):
    """The description of the game's rules."""
    def get(self, request):
        return render(request, "game/rules.html")


class GameView(LoginRequiredMixin, View):
    """The game for the current day."""
    def get(self, request):
        user = request.user

        quiz = db_control.get_current_quiz()

        played = models.Answer.objects.filter(
            user=user,
            quiz_question__quiz=quiz
        ).exists()
        # played = models.Answer.objects.filter(quiz=quiz, user=user).exists()
        quiz_questions = quiz.quizquestion_set.order_by("question_index")

        ctx = {
            "quiz": quiz,
            "quiz_questions": quiz_questions,
            "played": played,
        }
        return render(request, "game/quiz.html", ctx)

    def post(self, request):
        post = QueryDict.dict(request.POST) # TODO ponoć QueryDict zbędny
        quiz = models.Quiz.objects.get(id=post.get("quiz_id"))
        quiz_questions = quiz.quizquestion_set.order_by("question_index")
        answers = [models.Answer(user=request.user, quiz_question_id=qq.id, answer=post.get(str(qq.id)))
                   for qq in quiz_questions]

        with transaction.atomic():
            models.Answer.objects.bulk_create(answers)
            # transform.recalculate_and_save_matches(quiz)  # TODO niepotrzebne bo tylko ran dziennie będą wyniki

        return redirect("game")


class CompatibilityView(LoginRequiredMixin, View):
    """Juxtaposition of answers of two users for the given quiz."""

    def get(self, request, quiz_date, username1, username2):
        quiz = get_object_or_404(models.Quiz, date=quiz_date)
        user1 = get_object_or_404(User, username=username1)
        user2 = get_object_or_404(User, username=username2)

        if not db_control.user_participated_in_quiz(user1, quiz):
            raise Http404("User hasn't participated in this quiz.")

        if not db_control.user_participated_in_quiz(user2, quiz):
            raise Http404("Matched user hasn't participated in this quiz.")

        if user1 != request.user:
            raise Http404("Can't show compatibility of other users.")

        quiz_questions = quiz.quizquestion_set.order_by("question_index")

        elements = []
        for quiz_question in quiz_questions:
            question = quiz_question.question.question
            answer1 = db_control.get_text_answer(quiz_question, user1)
            answer2 = db_control.get_text_answer(quiz_question, user2)
            elements.append((question, answer1, answer2))

        ctx = {
            "quiz": quiz,
            "user1": user1,
            "user2": user2,
            "elements": elements,
        }
        return render(request, "game/compatibility.html", ctx)


class MatchesView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        quizes = db_control.list_quizes(user)

        matches_context = []
        for quiz in quizes:
            match_context = db_control.get_match_context(quiz, user)
            matches_context.append(match_context)

        ctx = {"matches": matches_context}
        return render(request, "game/matches.html", ctx)


class MessageInboxView(LoginRequiredMixin, View):
    """List of received messages."""
    def get(self, request):
        messages_in = models.Message.objects.filter(to_user=request.user).order_by("-sent_at")
        return render(request, "message/message_inbox.html", {"messages_in": messages_in})


class MessageOutboxView(LoginRequiredMixin, View):
    def get(self, request):
        messages_out = models.Message.objects.filter(from_user=request.user).order_by("-sent_at")
        return render(request, "message/message_outbox.html", {"messages_out": messages_out})


class MessageWriteView(LoginRequiredMixin, View):
    """
    Form to write a message.
    If no to_user_id is provided, then the list of available recipients contains all previous matches.
    Otherwise, the list contains only one user implied by the id.
    """
    def get(self, request, to_user_id=None):
        if not to_user_id:
            matches = db_control.get_matches_queryset(request.user)
            form = forms.MessageForm()
        else:
            match = get_object_or_404(User, pk=to_user_id)
            if not db_control.user_is_match_with(request.user, match):
                raise Http404("User can only write to their matches.")

            matches = User.objects.filter(id=match.id)
            form = forms.MessageForm(initial={"to_user": match})
        form.fields["to_user"].queryset = matches
        num_matches = matches.count()
        ctx = {
            "form": form,
            "no_matches": num_matches,
        }
        return render(request, "message/message_write.html", ctx)

    def post(self, request, to_user_id=None):
        user = request.user
        form = forms.MessageForm(request.POST)

        if form.is_valid():
            # Create new message
            to_user = form.cleaned_data.get("to_user")
            body = form.cleaned_data.get("body")
            msg = models.Message.objects.create(
                from_user=self.request.user,
                to_user=to_user,
                body=body,
            )

            # Inform user by e-mail
            # subject = f"optyjaciel | nowa wiadomość od {user.username}"
            # ctx = {"user": user, "msg": msg, "domain": DOMAIN}
            # html_message = render_to_string("email/new-message.html", ctx)
            # plain_message = strip_tags(html_message)
            # send_mail_to_user.delay(subject, plain_message, html_message, to_email=to_user.email)
            # send_mail_to_user(subject, plain_message, html_message, to_email=to_user.email)
        return redirect("message-outbox")


class MessageReadView(LoginRequiredMixin, View):
    """Content of the message."""
    def get(self, request, message_id):
        message = get_object_or_404(models.Message, pk=message_id)
        if request.user == message.to_user:
            msg_type = "in"
        elif request.user == message.from_user:
            msg_type = "out"
        else:
            raise Http404("Wiadomość nie istnieje.")

        # Mark message as read
        if msg_type == "in" and message.new:
            message.new = False
            message.save()

        ctx = {
            "msg_type": msg_type,
            "message": message,
        }
        return render(request, "message/message_read.html", ctx)


class DiaryView(View):
    def get(self, request):
        posts = models.Post.objects.all()
        return render(request, "game/diary.html", {"posts": posts})


class DiaryPostView(View):
    def get(self, request, slug):
        post = get_object_or_404(models.Post, slug=slug)
        return render(request, "game/diary_post.html", {"post": post})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, "game/profile.html", {"user": user})


class ProfileDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "game/profile_delete.html")

    def post(self, request):
        user = request.user
        user.email = ""
        user.is_active = False
        user.save()

        user.profile.nickname = "[użytkownik usunięty]"
        user.profile.save()
        return logout_then_login(request)
