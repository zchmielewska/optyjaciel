import datetime
from django.shortcuts import render
from .models import Quiz


def main(request):
    now = datetime.datetime.now()
    year = int(now.strftime("%Y"))
    week = int(now.strftime("%W"))
    quiz = Quiz.objects.get(year=year, week=week)
    return render(request, 'home.html', {"quiz": quiz})
