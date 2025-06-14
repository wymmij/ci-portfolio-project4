from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, Season, Match
from .forms import TeamSelectionForm, SeasonForm, MatchForm


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


@login_required
def season_detail_view(request, season_slug):
    season = get_object_or_404(Season, slug=season_slug, contributor=request.user)
    matches = season.match_set.order_by('date')
    return render(request, 'team/season_detail.html', {
        'season': season,
        'matches': matches,
    })


@login_required
def create_match_view(request, season_slug):
    season = get_object_or_404(Season, slug=season_slug, contributor=request.user)

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.season = season
            match.save()
            messages.success(request, 'Match added successfully!')
            return redirect('dashboard')
    else:
        form = MatchForm()

    return render(request, 'team/match_form.html', {
        'form': form,
        'season': season,
    })
