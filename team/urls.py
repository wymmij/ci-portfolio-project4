from django.urls import path
from .views import choose_team_view, create_season_view

urlpatterns = [
    path('choose-team/', choose_team_view, name='choose_team'),
    path('season/create/', create_season_view, name='create_season'),
]
