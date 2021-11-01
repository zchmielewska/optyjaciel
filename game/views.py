import pandas as pd
import game.utils.utils
import game.utils.solver
import game.utils.transform
import django.utils.timezone
from .models import Quiz, Answer, Match
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.views import View


USER_ID = 6


class MainView(View):
    def get(self, request):
        quiz = game.utils.utils.get_current_quiz()
        # played = len(Match.objects.filter(quiz=quiz).filter(user_id=1)) > 0
        played = False

        if not played:
            quizitems = quiz.quizitem_set.all().order_by("question_set_index")
            ctx = {
                "quiz_id": quiz.id,
                "quizitems": quizitems,
            }
            return render(request, 'home.html', ctx)
        else:
            match = Match.objects.get(quiz=quiz, user_id=USER_ID)  # TODO zmień user_id
            ctx = {
                "matched_user": match.matched_user,
                "remaining_time_in_week": game.utils.utils.get_remaining_time_in_week(),
            }
            return render(request, "match.html", ctx)

    def post(self, request):
        post = QueryDict.dict(request.POST)
        post.pop("csrfmiddlewaretoken")
        quiz_id = post.pop("quiz_id")
        quiz = Quiz.objects.get(id=quiz_id)

        # Add user's answers to db
        for key, value in post.items():
            Answer.objects.create(
                user_id=USER_ID,  # TODO zmień usera
                quiz_item_id=key,
                answer=value
            )

        answers, users_id = self.get_answers(quiz)
        scores = game.utils.transform.answers_to_scores_matrix(answers)
        match_matrix = game.utils.solver.match(scores)
        match_table = game.utils.transform.match_matrix_to_match_table(match_matrix, users_id)
        for index, row in match_table.iterrows():
            Match.objects.create(quiz_id=quiz_id, user_id=row["user"], matched_user_id=row["matched_user"])

        match = Match.objects.get(quiz=quiz, user_id=USER_ID)  # TODO zmień user_id
        ctx = {
            "matched_user": match.matched_user,
            "remaining_time_in_week": game.utils.utils.get_remaining_time_in_week(),
        }
        return render(request, "match.html", ctx)


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


def test2(request):
    answers_list = []
    i = 1
    quiz_item = quiz.quizitem_set.filter(question_set_index=i)
    quiz_item_answers = quiz_item.answer_set.all().order_by("user_id")
    if i == 1:
        df = quiz_item_answers.values("user_id", "answer")
    else:
        df = quiz_item_answers.values("answer")
    answers_list.append(df)
    answers = pd.concat(answers_list, axis=1)

    pass


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
        return render(request, "suggest.html")

