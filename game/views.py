import pandas as pd
import game.utils.utils
import game.utils.solver
import game.utils.transform
import django.utils.timezone

from .forms import SuggestionForm
from .models import Quiz, QuizItem, Answer, Match, User, Suggestion
from django.db import transaction
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView

USER_ID = 4


class MainView(View):
    def get(self, request):
        user = User.objects.get(id=USER_ID)
        quiz = game.utils.utils.get_current_quiz()
        # quiz = Quiz.objects.get(id=1)  # TODO remove; used to add data to previous quizes
        played = len(Match.objects.filter(quiz=quiz, user=user)) > 0  # TODO czy user tak zostaje?

        if not played:
            quizitems = quiz.quizitem_set.all().order_by("question_set_index")
            ctx = {
                "quiz": quiz,
                "quizitems": quizitems,
            }
            return render(request, 'home.html', ctx)
        else:
            ctx = self.get_match_ctx(quiz, user)
            return render(request, "match.html", ctx)

    def post(self, request):
        user = User.objects.get(id=USER_ID)
        post = QueryDict.dict(request.POST)
        post.pop("csrfmiddlewaretoken")
        quiz_id = post.pop("quiz_id")
        quiz = Quiz.objects.get(id=quiz_id)

        with transaction.atomic():
            # Add logged user's answers to db
            for key, value in post.items():
                Answer.objects.create(
                    user_id=USER_ID,  # TODO zmień usera
                    quiz_item_id=key,
                    answer=value
                )

            # Get answers of all users and recalculate matches
            answers, users_id = self.get_answers(quiz)
            scores = game.utils.transform.answers_to_scores_matrix(answers)
            match_matrix = game.utils.solver.match(scores)
            match_table = game.utils.transform.match_matrix_to_match_table(match_matrix, users_id)

            # Save new matches
            for index, row in match_table.iterrows():
                matched_user_id = row["matched_user"] if not pd.isnull(row["matched_user"]) else None
                Match.objects.create(quiz_id=quiz_id, user_id=row["user"], matched_user_id=matched_user_id)

        ctx = self.get_match_ctx(quiz, user)
        return render(request, "match.html", ctx)

    def get_match_ctx(self, quiz, user):
        match = Match.objects.filter(quiz=quiz, user=user).order_by("-matched_at").first()
        matched_user = match.matched_user
        score = game.utils.utils.calculate_score(quiz, user, matched_user) if matched_user else 0
        ctx = {
            "quiz": quiz,
            "user_id": user.id,
            "matched_user": matched_user,
            "score": score,
            "points": game.utils.utils.conjugate_points(score),
            "remaining_time_in_week": game.utils.utils.get_remaining_time_in_week(),
        }
        return ctx

    def get_answers(self, quiz):
        answers_list = []
        for i in range(10):
            question_set_index = i+1
            quiz_item = quiz.quizitem_set.get(question_set_index=question_set_index)
            quiz_item_answers = quiz_item.answer_set.all().order_by("user_id")
            if question_set_index == 1:
                df = pd.DataFrame(list(quiz_item_answers.values("user_id", "answer")))
            else:
                df = pd.DataFrame(list(quiz_item_answers.values("answer")))
            df = df.rename(columns={"answer": "answer" + str(question_set_index)})
            answers_list.append(df)

        df = pd.concat(answers_list, axis=1)
        answers = df[["answer" + str(i+1) for i in range(10)]]
        users_id = list(df["user_id"])
        return answers, users_id


class CompatibilityView(View):
    def get(self, request, quiz_id, user1_id, user2_id):
        quiz = Quiz.objects.get(id=quiz_id)
        user1 = User.objects.get(id=user1_id)
        user2 = User.objects.get(id=user2_id)
        quiz_items = quiz.quizitem_set.all().order_by("question_set_index")

        elements = []
        for quiz_item in quiz_items:
            question = quiz_item.question_set.question
            answer1 = self.get_answer(quiz_item, user1)
            answer2 = self.get_answer(quiz_item, user2)
            elements.append((question, answer1, answer2))

        ctx = {
            "quiz": quiz,
            "user1": user1,
            "user2": user2,
            "elements": elements,
        }

        return render(request, "compatibility.html", ctx)

    def get_answer(self, quiz_item, user):
        answer_object = Answer.objects.get(user=user, quiz_item=quiz_item)
        answer = answer_object.answer

        if answer == 1:
            result = quiz_item.question_set.option1
        elif answer == 2:
            result = quiz_item.question_set.option2
        elif answer == 3:
            result = quiz_item.question_set.option3
        else:
            result = quiz_item.question_set.option4

        return result


class MatchesView(View):
    # Znajdź wszystkie rundy w których brał udział użytkownik

    pass


class RulesView(View):
    def get(self, request):
        return render(request, "rules.html")


class SuggestionView(FormView):
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
            user_id=USER_ID,  # TODO
        )

        return redirect("thanks")


class ThanksView(View):
    def get(self, request):
        return render(request, "thanks.html")
