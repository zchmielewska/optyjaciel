from django.urls import path
from .views import *

urlpatterns = [
    path('', RulesView.as_view(), name="rules"),
    path('runda/', GameView.as_view(), name="game"),
    path('kompatybilnosc/<int:quiz_id>/<int:user1_id>/<int:user2_id>/', CompatibilityView.as_view(),
         name="compatibility"),
    path('optyjaciele/', MatchesView.as_view(), name="matches"),
    path('zaproponuj-pytanie/', SuggestionView.as_view(), name="suggest"),
    path('dziekuje/', ThanksView.as_view(), name="thanks"),
    path('zarejestruj/', RegisterView.as_view(), name="register"),
    path('zaloguj/', LoginView.as_view(), name="login"),
    path('wyloguj/', LogoutView.as_view(), name="logout"),
]