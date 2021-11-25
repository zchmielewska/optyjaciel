from django.urls import resolve
from game.models import Message


def path_name(request):
    path_name = resolve(request.path).url_name
    return {"path_name": path_name}


def no_messages(request):
    no_messages = 0

    if request.user.is_authenticated:
        no_messages = Message.objects.filter(to_user=request.user, new=True).count()

    return {"no_messages": no_messages}
