import game.models
from django import forms
from django.contrib.auth.models import User


# class SuggestionForm(forms.ModelForm):
#     class Meta:
#         model = game.models.Suggestion
#         exclude = ["user"]


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=36, label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=36, label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class MessageForm(forms.Form):
    to_user = forms.ModelChoiceField(queryset=User.objects.all(), label="Odbiorca")
    body = forms.CharField(widget=forms.Textarea(attrs={"style": "width: 100%;"}), label="Wiadomość")
