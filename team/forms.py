from django import forms
from .models import Team, Season, Match

class TeamSelectionForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'short_name', 'city', 'country', 'is_public']


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['start_date', 'end_date']


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['date', 'opponent', 'is_home', 'team_score', 'opponent_score', 'notes']
