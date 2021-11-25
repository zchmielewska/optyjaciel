from django import forms
from django.core.exceptions import ValidationError
from game.models import *


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ["user"]


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=36, label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=36, label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ["from_user", "sent_at", "new"]
