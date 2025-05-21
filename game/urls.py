from django.urls import path
from game import views


urlpatterns = [
    path("", views.GameView.as_view(), name="main"),
    path("zasady/", views.RulesView.as_view(), name="rules"),
    path("gra/", views.GameView.as_view(), name="game"),
    path("kompatybilnosc/<int:quiz_date>/<str:username1>/<str:username2>/", views.CompatibilityView.as_view(), name="compatibility"),
    path("optyjaciele/", views.MatchesView.as_view(), name="matches"),
    path("wiadomosc/odebrane/", views.MessageInboxView.as_view(), name="message-inbox"),
    path("wiadomosc/wyslane/", views.MessageOutboxView.as_view(), name="message-outbox"),
    path("wiadomosc/napisz/", views.MessageWriteView.as_view(), name="message-write"),
    path("wiadomosc/napisz/<str:to_username>/", views.MessageWriteView.as_view(), name="message-write"),
    path("wiadomosc/czytaj/<uuid:message_uuid>/", views.MessageReadView.as_view(), name="message-read"),
    path("pamietnik/", views.DiaryView.as_view(), name="blog"),
    path("pamietnik/<slug>", views.DiaryPostView.as_view(), name="post"),
    path("profil/", views.ProfileView.as_view(), name="profile"),
    path("profil/usun/", views.ProfileDeleteView.as_view(), name="profile-delete"),
]
