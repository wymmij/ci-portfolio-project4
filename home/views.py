from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from team.models import Season, Team


@login_required
def dashboard_view(request):
    """
    Display the contributor's dashboard view.

    **Context**

    ``team``
        The first :model:`team.Team` instance belonging to the logged-in user.
    ``seasons``
        A queryset of :model:`team.Season` instances linked to the logged-in user,
        ordered by descending start date.

    **Template:**

    :template:`home/dashboard.html`
    """
    team = Team.objects.filter(contributor=request.user).first()
    seasons = Season.objects.filter(contributor=request.user).order_by(
        "-start_date"
    )
    return render(
        request,
        "home/dashboard.html",
        {
            "team": team,
            "seasons": seasons,
        },
    )


def home_view(request):
    """
    Render the public home page of the application.

    **Template:**

    :template:`home/home.html`
    """
    return render(request, "home/home.html")
