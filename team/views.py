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
def create_season_view(request, team_slug):
    team = get_object_or_404(Team, slug=team_slug, contributor=request.user)

    if request.method == 'POST':
        form = SeasonForm(request.POST)
        if form.is_valid():
            season = form.save(commit=False)
            season.contributor = request.user
            season.team = team
            season.save()
            messages.success(request, 'Season created successfully!')
            return redirect('season_detail', team_slug=team.slug, season_slug=season.slug)
            # return redirect('dashboard')
    else:
        form = SeasonForm()

    return render(request, 'team/season_form.html', {'form': form, 'team': team})


@login_required
def season_detail_view(request, team_slug, season_slug):
    season = get_object_or_404(Season, slug=season_slug, team__slug=team_slug, contributor=request.user)
    matches = season.match_set.order_by('date')
    return render(request, 'team/season_detail.html', {
        'season': season,
        'matches': matches,
    })


@login_required
def create_match_view(request, team_slug, season_slug):
    team = get_object_or_404(Team, slug=team_slug, contributor=request.user)
    season = get_object_or_404(Season, slug=season_slug, team=team, contributor=request.user)

    if request.method == 'POST':
        form = MatchForm(request.POST, season=season)
        if form.is_valid():
            match = form.save(commit=False)
            match.season = season
            match.save()
            messages.success(request, 'Match added successfully!')
            return redirect('season_detail', team_slug=team.slug, season_slug=season.slug)
    else:
        form = MatchForm(season=season)

    return render(request, 'team/match_form.html', {
        'form': form,
        'season': season,
    })


@login_required
def edit_match_view(request, team_slug, season_slug, match_id):
    team = get_object_or_404(Team, slug=team_slug, contributor=request.user)
    season = get_object_or_404(Season, slug=season_slug, team=team)
    match = get_object_or_404(Match, id=match_id, season=season)

    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match, season=season)
        if form.is_valid():
            form.save()
            messages.success(request, 'Match updated successfully.')
            return redirect('season_detail', team_slug=team.slug, season_slug=season.slug)
    else:
        form = MatchForm(instance=match, season=season)

    return render(request, 'team/match_form.html', {
        'form': form,
        'season': season,
        'match': match,
    })


@login_required
def delete_match_view(request, team_slug, season_slug, match_id):
    team = get_object_or_404(Team, slug=team_slug, contributor=request.user)
    season = get_object_or_404(Season, slug=season_slug, team=team)
    match = get_object_or_404(Match, id=match_id, season=season)

    if request.method == 'POST':
        match.delete()
        messages.success(request, 'Match deleted successfully.')
        return redirect('season_detail', team_slug=team.slug, season_slug=season.slug)

    return render(request, 'team/match_confirm_delete.html', {
        'match': match,
        'season': season,
    })
