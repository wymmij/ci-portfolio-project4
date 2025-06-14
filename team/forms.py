from django import forms
from .models import Team, Season

class TeamSelectionForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'short_name', 'city', 'country', 'is_public']


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['start_date', 'end_date']
