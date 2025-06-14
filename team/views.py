from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team
from .forms import TeamSelectionForm, SeasonForm


@login_required
def choose_team_view(request):
    if Team.objects.filter(contributor=request.user).exists():
        # Skip if user already has a team
        return redirect('dashboard')

    if request.method == 'POST':
        form = TeamSelectionForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.contributor = request.user
            team.save()
            return redirect('dashboard')
    else:
        form = TeamSelectionForm()

    return render(request, 'team/choose_team.html', {'form': form})


@login_required
def create_season_view(request):
    team = Team.objects.filter(contributor=request.user).first()
    if not team:
        return redirect('choose_team')  # Safety net

    if request.method == 'POST':
        form = SeasonForm(request.POST)
        if form.is_valid():
            season = form.save(commit=False)
            season.contributor = request.user
            season.team = team
            season.save()
            messages.success(request, 'Season created successfully!')
            return redirect('dashboard')
    else:
        form = SeasonForm()

    return render(request, 'team/season_form.html', {'form': form})

