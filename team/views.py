from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TeamSelectionForm
from .models import Team

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
