import datetime
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Quiz, AnswerSet, Match
from .solver import match
from .transform import answers_to_scores_matrix


class MainView(View):
    def get(self, request):
        # has_played = len(Match.objects.filter(quiz_id=1).filter(user_id=1)) > 0
        has_played = False

        if not has_played:
            # If the user hasn't played yet, they should solve the quiz
            now = datetime.datetime.now()
            year = int(now.strftime("%Y"))
            week = int(now.strftime("%W"))
            quiz = Quiz.objects.get(year=year, week=week)
            return render(request, 'home.html', {"quiz": quiz})

        else:
            # If the user has already played, they should see the current result
            # TODO
            match = Match.objects.get(quiz_id=1, user_id=1)
            matched_user = match.matched_user
            return HttpResponse(matched_user)

    def post(self, request):
        # Save users answers
        AnswerSet.objects.create(user_id=1,
                                 quiz_id=1,
                                 answer0=request.POST.get("question-set0"),
                                 answer1=request.POST.get("question-set1"),
                                 answer2=request.POST.get("question-set2"),
                                 answer3=request.POST.get("question-set3"),
                                 answer4=request.POST.get("question-set4"),
                                 answer5=request.POST.get("question-set5"),
                                 answer6=request.POST.get("question-set6"),
                                 answer7=request.POST.get("question-set7"),
                                 answer8=request.POST.get("question-set8"),
                                 answer9=request.POST.get("question-set9"))

        # Create new matchings
        x = AnswerSet.objects.filter(quiz_id=1)
        return HttpResponse("Wysłano quiz")


def test(request):
    # TODO: order_by id
    users_id_objects = list(AnswerSet.objects.filter(quiz_id=1).values('user_id'))
    users_id = [user_id_object["user_id"] for user_id_object in users_id_objects]

    answers = pd.DataFrame(list(AnswerSet.objects.filter(quiz_id=1)
                                .values('answer0', 'answer1', 'answer2', 'answer3', 'answer4',
                                        'answer5', 'answer6', 'answer7', 'answer8', 'answer9')))

    scores = answers_to_scores_matrix(answers)
    match_matrix = match(scores)

    data = []
    n = len(users_id)
    for i in range(n):
        for j in range(n):
            if match_matrix[i, j] == 1:
                data.append([users_id[i], users_id[j]])
                break
            else:
                if j == n-1:
                    data.append([users_id[i], None])
    df = pd.DataFrame(data, columns=["user", "matched_user"])

    for index, row in df.iterrows():
        Match.objects.create(quiz_id=1, user_id=row["user"], matched_user_id=row["matched_user"])

    return HttpResponse("kukuryku")


class RulesView(View):
    def get(self, request):
        return render(request, "rules.html")


class SuggestQuestionView(View):
    def get(self, request):
        return render(request, "suggest_question.html")

