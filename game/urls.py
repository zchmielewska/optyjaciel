from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name="current-game"),
    path('rules/', views.RulesView.as_view(), name="rules"),
    path('suggest-question/', views.SuggestQuestionView.as_view(), name="suggest-question"),
]