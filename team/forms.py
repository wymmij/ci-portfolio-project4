from django import forms
from django.forms import DateInput, TimeInput
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
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'competition_list': forms.TextInput(attrs={'placeholder': 'e.g. Championship, FA Cup, League Cup'}),
        }


class MatchForm(forms.ModelForm):
    competition = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Match
        fields = [
            'date', 'time', 'opponent', 'is_home', 
            'competition', 'round', 'attendance', 
            'team_score', 'opponent_score', 'goals'
        ]
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
            'opponent': forms.TextInput(attrs={'placeholder': 'e.g. Leeds United'}),
            'round': forms.TextInput(attrs={'placeholder': 'e.g. Matchday 1, Quarter Final'}),
            'goals': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': "e.g. Smith 45+2, 76, Windass 83, Bannan 90+1"
            }),
        }

    def __init__(self, *args, season=None, **kwargs):
        super().__init__(*args, **kwargs)
        if season:
            self.fields['competition'].choices = [(c, c) for c in season.competitions]


class MatchImportForm(forms.Form):
    tsv_file = forms.FileField(label="Select TSV File")
