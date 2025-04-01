from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from account.forms import UserRegistrationForm
from account.models import Profile


class RegisterView(View):
    @csrf_exempt
    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, "account/register.html", {"user_form": user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user, nickname=new_user.username)
            return render(request, "account/register_done.html", {"new_user": new_user})
        return render(request, "account/register.html", {"user_form": user_form})
