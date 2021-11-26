from django import forms
from django.contrib.auth.models import User
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


class MessageForm(forms.Form):
    to_user = forms.ModelChoiceField(queryset=User.objects.all(), label="Odbiorca")
    title = forms.CharField(widget=forms.TextInput(attrs={"style": "width: 100%;"}), max_length=1024, label="Tytuł")
    body = forms.CharField(widget=forms.Textarea(attrs={"style": "width: 100%;"}), label="Wiadomość")
