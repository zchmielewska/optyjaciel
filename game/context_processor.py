import django.utils.timezone


def my_cp(request):
    ctx = {
        "year": django.utils.timezone.now().isocalendar()[0],
        "week": django.utils.timezone.now().isocalendar()[1],
    }
    return ctx
