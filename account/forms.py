from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from game.utils.utils import string_is_integer


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        """Usernames are changed to ids when the account is deleted.
        Users can't register with numbers so that they don't clash with ids."""
        username = self.cleaned_data.get("username")
        if string_is_integer(username):
            raise forms.ValidationError("Nazwa użytkownika nie może być liczbą.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            self.add_error("password", error)
        return password

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Podane hasła różnią się.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == "":
            raise forms.ValidationError("Adres e-mail nie może być pusty.")
        return email

