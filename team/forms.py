from django import forms
from .models import Team, Season, Match

class TeamSelectionForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'short_name', 'city', 'country', 'is_public']


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['start_date', 'end_date', 'competition_list']
        labels = {'competition_list': 'Competitions (comma-separated)',}
        widgets = {
            'competition_list': forms.TextInput(attrs={'placeholder': 'e.g. Championship, FA Cup, League Cup'}),
        }


class MatchForm(forms.ModelForm):
    competition = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Match
        fields = [
            'date', 'time', 'opponent', 'is_home', 
            'competition', 'round', 'attendance', 
            'team_score', 'opponent_score'
        ]

    def __init__(self, *args, season=None, **kwargs):
        super().__init__(*args, **kwargs)
        if season:
            self.fields['competition'].choices = [(c, c) for c in season.competitions]
