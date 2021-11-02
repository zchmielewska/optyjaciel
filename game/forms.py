from django.forms import ModelForm
from game.models import Suggestion


class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        exclude = ["user"]
