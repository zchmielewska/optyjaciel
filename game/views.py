import datetime
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import Quiz, AnswerSet
from .solver import match
from .transform import answers_to_scores_matrix


def main(request):
    if request.method == "GET":
        # If the user hasn't played yet, they should solve the quiz
        now = datetime.datetime.now()
        year = int(now.strftime("%Y"))
        week = int(now.strftime("%W"))
        quiz = Quiz.objects.get(year=year, week=week)
        return render(request, 'home.html', {"quiz": quiz})

        # If the user has already played, they should see the current result
        # TODO
    else:
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
        print(x)
        return HttpResponse("Wysłano quiz")


def test(request):
    # TODO: order_by id
    users_id = pd.DataFrame(list(AnswerSet.objects.filter(quiz_id=1).values('user_id')))
    answers = pd.DataFrame(list(AnswerSet.objects.filter(quiz_id=1)
                                .values('answer0', 'answer1', 'answer2', 'answer3', 'answer4',
                                        'answer5', 'answer6', 'answer7', 'answer8', 'answer9')))



    scores = answers_to_scores_matrix(answers)
    match_matrix = match(scores)

    print("match_matrix")
    print(match_matrix)
    print("")
    print("users_id")
    print(users_id)

    print(users_id.iloc[2] + 2)

    data = []
    n = len(users_id)
    # for i in range(n):
    #     for j in range(n):
    #         data.append([1, ])

    return HttpResponse("nanana")
