import numpy as np
import pandas as pd
import pytest
from django.test import TestCase

from game import models
from game.utils import transform
from game.utils import solver


class Transform00Test(TestCase):
    def test_answers_to_scores_matrix(self):
        a1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        a2 = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]
        a3 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        s1 = np.array([10])
        s2 = np.array([[10, 3], [3, 10]])
        s3 = np.array([[10, 3, 0], [3, 10, 2], [0, 2, 10]])
        self.assertEqual(transform.answers_to_scores_matrix(pd.DataFrame([a1])), s1)
        self.assertTrue((transform.answers_to_scores_matrix(pd.DataFrame([a1, a2])) == s2).all())
        self.assertTrue((transform.answers_to_scores_matrix(pd.DataFrame([a1, a2, a3])) == s3).all())

        a4 = [1, 2, 3]
        self.assertRaises(ValueError, transform.answers_to_scores_matrix, pd.DataFrame([a4]))
        self.assertRaises(ValueError, transform.answers_to_scores_matrix, pd.DataFrame([]))

    def test_match_matrix_to_match_table(self):
        m1 = np.array([0])
        l1 = [1]
        df1 = pd.DataFrame([[1, None]], columns=["user", "matched_user"])
        self.assertTrue((transform.match_matrix_to_match_table(m1, l1).equals(df1)))

        m2 = np.array([[0, 1], [1, 0]])
        l2 = [1, 2]
        df2 = pd.DataFrame([[1, 2], [2, 1]], columns=["user", "matched_user"])
        self.assertTrue((transform.match_matrix_to_match_table(m2, l2).equals(df2)))

        m3 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
        l3 = [1, 5, 7]
        df3 = pd.DataFrame([[1, 7], [5, None], [7, 1]], columns=["user", "matched_user"])
        self.assertTrue((transform.match_matrix_to_match_table(m3, l3).equals(df3)))


# DB contains 1 quiz + 2 users
class Transform02Test(TestCase):
    fixtures = ["02.json"]

    def test_get_answers(self):
        quiz = models.Quiz.objects.get(pk=1)
        answers, list_ids = transform.get_answers(quiz)
        df = pd.DataFrame([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]],
                          columns=["answer" + str(i + 1) for i in range(10)])
        self.assertTrue(answers.equals(df))
        self.assertEqual(list_ids, [1, 2])

    def test_answers_to_scores_matrix(self):
        quiz = models.Quiz.objects.get(pk=1)
        answers, list_ids = transform.get_answers(quiz)
        scores = transform.answers_to_scores_matrix(answers)
        m = np.array([
            [10, 3],
            [3, 10]
        ])
        self.assertTrue((scores == m).all())

    def test_recalculate_and_save_matches(self):
        self.assertEqual(models.Match.objects.count(), 0)
        quiz = models.Quiz.objects.get(pk=1)
        transform.recalculate_and_save_matches(quiz)
        self.assertEqual(models.Match.objects.count(), 2)
        match1 = models.Match.objects.all()[0]
        match2 = models.Match.objects.all()[1]
        self.assertEqual(match1.user.id, 1)
        self.assertEqual(match1.matched_user.id, 2)
        self.assertEqual(match2.user.id, 2)
        self.assertEqual(match2.matched_user.id, 1)
        self.assertEqual(match1.quiz.id, 1)
        self.assertEqual(match2.quiz.id, 1)


# DB contains 3 quizes + 1 user who answered to 2 quizes
class DbControl03Test(TestCase):
    fixtures = ["03.json"]

    def test_get_answers(self):
        quiz = models.Quiz.objects.get(pk=1)
        answers, list_ids = transform.get_answers(quiz)
        df = pd.DataFrame([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                          columns=["answer" + str(i + 1) for i in range(10)])
        self.assertTrue(answers.equals(df))
        self.assertEqual(list_ids, [1])

    def test_answers_to_scores_matrix(self):
        quiz = models.Quiz.objects.get(pk=1)
        answers, list_ids = transform.get_answers(quiz)
        scores = transform.answers_to_scores_matrix(answers)
        m = np.array([10])
        self.assertTrue((scores == m).all())

    def test_match_matrix_to_match_table(self):
        quiz = models.Quiz.objects.get(pk=1)
        answers, list_ids = transform.get_answers(quiz)
        scores = transform.answers_to_scores_matrix(answers)
        match_matrix = solver.match(scores)
        match_table = transform.match_matrix_to_match_table(match_matrix, list_ids)
        df1 = pd.DataFrame([[1, None]], columns=["user", "matched_user"])
        self.assertTrue(match_table.equals(df1))
