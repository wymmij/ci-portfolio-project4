from django import forms
from .models import Team

class TeamSelectionForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'short_name', 'city', 'country', 'is_public']
