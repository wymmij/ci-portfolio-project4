from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from team.models import Season


@login_required
def dashboard_view(request):
    seasons = Season.objects.filter(contributor=request.user).order_by('-start_date')
    return render(request, 'home/dashboard.html', {
        'seasons': seasons,
    })


def home_view(request):
    return render(request, 'home/home.html')