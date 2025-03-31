from django.urls import path
from game import views


urlpatterns = [
    path("", views.RulesView.as_view(), name="rules"),
    path("game/", views.GameView.as_view(), name="game"),
    path("compatibility/<int:quiz_id>/<int:user1_id>/<int:user2_id>/", views.CompatibilityView.as_view(), name="compatibility"),
    path("matches/", views.MatchesView.as_view(), name="matches"),
    path("message/inbox/", views.MessageInboxView.as_view(), name="message-inbox"),
    path("message/outbox/", views.MessageOutboxView.as_view(), name="message-outbox"),
    path("message/write/", views.MessageWriteView.as_view(), name="message-write"),
    path("message/write/<int:to_user_id>/", views.MessageWriteView.as_view(), name="message-write"),
    path("message/read/<int:message_id>/", views.MessageReadView.as_view(), name="message-read"),
    path("blog/", views.BlogView.as_view(), name="blog"),
    path("blog/<slug>", views.BlogPostView.as_view(), name="post"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/delete/", views.ProfileDeleteView.as_view(), name="profile-delete"),
]
