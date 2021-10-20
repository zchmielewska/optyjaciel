import datetime
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import Quiz, AnswerSet
from .solver import derive_match_matrix


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
    x = AnswerSet.objects.filter(quiz_id=1).values('answer0', 'answer1', 'answer2', 'answer3', 'answer4',
                                                   'answer5', 'answer6', 'answer7', 'answer8', 'answer9')
    df = pd.DataFrame(list(x))

    n = len(df.index)
    scores = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            scores[i, j] = sum(df.iloc[i] == df.iloc[j])

    match_matrix = derive_match_matrix(scores)
    print(match_matrix)

    return HttpResponse(df)
