from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name="game"),
    path('kompatybilnosc/<int:quiz_id>/<int:user1_id>/<int:user2_id>/', views.CompatibilityView.as_view(),
         name="compatibility"),
    path('zasady-gry/', views.RulesView.as_view(), name="rules"),
    path('zaproponuj-pytanie/', views.SuggestionView.as_view(), name="suggest"),
    path('dziekuje/', views.ThanksView.as_view(), name="thanks"),
]