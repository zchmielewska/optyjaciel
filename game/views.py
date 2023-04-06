from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.db import transaction
from django.http import Http404, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import FormView
from random import sample

from game import forms, models
from game.utils import db_control, transform, utils
from .tasks import send_mail_to_user


DOMAIN = settings.DEFAULT_DOMAIN


class RulesView(View):
    """The description of the game's rules."""
    def get(self, request):
        return render(request, "game/rules.html")


class GameView(LoginRequiredMixin, View):
    """
    The game for the current week.
    If the user hasn't played yet, returns the quiz for the current week.
    If the user has already played, returns the current match.
    """
    def get(self, request):
        user = request.user
        quiz = db_control.get_current_quiz()
        played = models.Match.objects.filter(quiz=quiz, user=user).count() > 0

        if not played:
            quiz_questions = quiz.quizquestion_set.order_by("question_index")
            ctx = {
                "quiz": quiz,
                "quiz_questions": quiz_questions,
            }
            return render(request, "game/game_quiz.html", ctx)
        else:
            ctx = db_control.get_match_context(quiz, user)
            ctx["previous_game"] = False
            ctx["remaining_time_in_week"] = utils.get_remaining_time_in_week()
            return render(request, "game/game_match.html", ctx)

    def post(self, request):
        post = QueryDict.dict(request.POST)
        quiz = models.Quiz.objects.get(id=post.get("quiz_id"))
        quiz_questions = quiz.quizquestion_set.order_by("question_index")
        answers = [models.Answer(user=request.user, quiz_question_id=qq.id, answer=post.get(str(qq.id)))
                   for qq in quiz_questions]

        with transaction.atomic():
            models.Answer.objects.bulk_create(answers)
            transform.recalculate_and_save_matches(quiz)

        return redirect("game")


class CompatibilityView(LoginRequiredMixin, View):
    """Juxtaposition of answers of two users for the given quiz."""
    def get(self, request, quiz_id, user1_id, user2_id):
        quiz = get_object_or_404(models.Quiz, pk=quiz_id)
        user1 = get_object_or_404(User, pk=user1_id)
        user2 = get_object_or_404(User, pk=user2_id)

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
    """Matches from all previous games."""
    def get(self, request):
        user = request.user
        quizes = db_control.list_quizes(user)
        matches_context = []
        for quiz in quizes:
            match_context = db_control.get_match_context(quiz, user, nest=False)
            matches_context.append(match_context)

        ctx = {
            "matches": matches_context,
            "previous_game": True
        }
        return render(request, "game/matches.html", ctx)


class SuggestionView(LoginRequiredMixin, FormView):
    """Form to send the suggestion for question."""
    template_name = "game/suggest.html"
    form_class = forms.SuggestionForm
    success_url = "/"

    def form_valid(self, form):
        question = form.cleaned_data.get("question")
        option1 = form.cleaned_data.get("option1")
        option2 = form.cleaned_data.get("option2")

        models.Suggestion.objects.create(
            question=question,
            option1=option1,
            option2=option2,
            user=self.request.user,
        )
        return redirect("thanks")


class ThanksView(View):
    def get(self, request):
        return render(request, "game/thanks.html")


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
        no_matches = matches.count()
        ctx = {
            "form": form,
            "no_matches": no_matches,
        }
        return render(request, "message/message_write.html", ctx)

    def post(self, request, to_user_id=None):
        user = request.user
        form = forms.MessageForm(request.POST)

        if form.is_valid():
            # Create new message
            to_user = form.cleaned_data.get("to_user")
            title = form.cleaned_data.get("title")
            body = form.cleaned_data.get("body")
            msg = models.Message.objects.create(
                from_user=self.request.user,
                to_user=to_user,
                title=title,
                body=body,
            )

            # Inform user by e-mail
            subject = f"optyjaciel | nowa wiadomość od {user.username}"
            ctx = {"user": user, "msg": msg, "domain": DOMAIN}
            html_message = render_to_string("email/new-message.html", ctx)
            plain_message = strip_tags(html_message)
            # send_mail_to_user.delay(subject, plain_message, html_message, to_email=to_user.email)
            send_mail_to_user(subject, plain_message, html_message, to_email=to_user.email)
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


class BlogView(View):
    def get(self, request):
        posts = models.Post.objects.all()
        return render(request, "game/blog.html", {"posts": posts})


class BlogPostView(View):
    def get(self, request, slug):
        post = get_object_or_404(models.Post, slug=slug)

        # Read also these posts
        pks = models.Post.objects.exclude(id=post.id).values_list("pk", flat=True)
        if len(pks) <= 3:
            random_pks = pks
        else:
            random_pks = sample(list(pks), 3)
        random_posts = models.Post.objects.filter(pk__in=random_pks)

        return render(request, "game/blog_post.html", {"post": post, "random_posts": random_posts})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, "game/profile.html", {"user": user})


class ProfileDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "game/profile_delete.html")

    def post(self, request):
        user = request.user
        user.username = user.id
        user.email = ""
        password = User.objects.make_random_password()
        user.set_password(password)
        user.is_active = False
        user.save()
        return logout_then_login(request)


class AboutView(View):
    def get(self, request):
        return render(request, "game/about.html")
