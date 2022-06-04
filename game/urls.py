from django.contrib.sitemaps.views import sitemap
from django.urls import path

from game import views

urlpatterns = [
    path("", views.RulesView.as_view(), name="rules"),
    path("game/", views.GameView.as_view(), name="game"),
    path("compatibility/<int:quiz_id>/<int:user1_id>/<int:user2_id>/", views.CompatibilityView.as_view(),
         name="compatibility"),
    path("matches/", views.MatchesView.as_view(), name="matches"),
    path("suggest/", views.SuggestionView.as_view(), name="suggest"),
    path("thanks/", views.ThanksView.as_view(), name="thanks"),
    path("wiadomosci/odebrane/", views.MessageInboxView.as_view(), name="message-inbox"),
    path("wiadomosci/wyslane/", views.MessageOutboxView.as_view(), name="message-outbox"),
    path("wiadomosci/utworz/", views.MessageWriteView.as_view(), name="message-write"),
    path("wiadomosci/utworz/<int:to_user_id>/", views.MessageWriteView.as_view(), name="message-write"),
    path("wiadomosci/czytaj/<int:message_id>/", views.MessageReadView.as_view(), name="message-read"),
]
