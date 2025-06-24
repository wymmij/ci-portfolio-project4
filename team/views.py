import csv
from datetime import date, time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, Season, Match
from .forms import TeamSelectionForm, SeasonForm, MatchForm, MatchImportForm


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


REQUIRED_FIELDS = {'date', 'opponent'}

@login_required
def import_matches_view(request, team_slug, season_slug):
    team = get_object_or_404(Team, slug=team_slug, contributor=request.user)
    season = get_object_or_404(Season, slug=season_slug, team=team)

    if request.method == 'POST' and request.FILES.get('tsv_file'):
        file = request.FILES['tsv_file']
        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file, delimiter='\t')

            if not reader.fieldnames:
                messages.error(request, "The uploaded file is empty or missing a header row.")
                return redirect('season_detail', team_slug=team.slug, season_slug=season.slug)

            missing = REQUIRED_FIELDS - set(reader.fieldnames)
            if missing:
                messages.error(request, f"Missing required fields: {', '.join(missing)}")
                return redirect('season_detail', team_slug=team.slug, season_slug=season.slug)

            created_count = 0
            for row in reader:
                # Required
                match_date = date.fromisoformat(row['date'])
                opponent = row['opponent']

                # Optional fields
                is_home = row.get('is_home', 'TRUE').strip().lower() == 'true'
                competition = row.get('competition', '').strip()
                match_round = row.get('round', '').strip()
                goals = row.get('goals', '').strip()

                team_score = row.get('team_score')
                opponent_score = row.get('opponent_score')
                team_score = int(team_score) if team_score and team_score.isdigit() else None
                opponent_score = int(opponent_score) if opponent_score and opponent_score.isdigit() else None

                attendance = row.get('attendance')
                attendance = int(attendance) if attendance and attendance.isdigit() else None

                match_time = row.get('time')
                try:
                    match_time = time.fromisoformat(match_time.strip()) if match_time else None
                except ValueError:
                    match_time = None

                home_field = row.get('is_home', '').strip().lower()
                valid_home_values = {'home', 'h', 'true', 'yes', '1'}
                valid_away_values = {'away', 'a', 'false', 'no', '0'}

                if home_field in valid_home_values:
                    is_home = True
                elif home_field in valid_away_values:
                    is_home = False
                else:
                    is_home = False
                    messages.warning(request, f"Row {reader.line_num}: Unrecognized value '{home_field}' for is_home. Defaulting to away.")

                Match.objects.create(
                    season=season,
                    date=match_date,
                    opponent=opponent,
                    is_home=is_home,
                    competition=competition,
                    round=match_round,
                    goals=goals,
                    attendance=attendance,
                    team_score=team_score,
                    opponent_score=opponent_score,
                    time=match_time
                )
                created_count += 1

            messages.success(request, f"{created_count} match record(s) imported successfully.")
        except Exception as e:
            messages.error(request, f"Import failed: {e}")

        return redirect('season_detail', team_slug=team.slug, season_slug=season.slug)

    return render(request, 'team/import_matches.html', {
        'season': season,
        'form': MatchImportForm(),
    })

