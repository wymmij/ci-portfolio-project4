from django.urls import path
from .views import choose_team_view, create_season_view, season_detail_view, create_match_view

urlpatterns = [
    path('choose-team/', choose_team_view, name='choose_team'),
    path('season/create/', create_season_view, name='create_season'),
    path('season/<slug:season_slug>/', season_detail_view, name='season_detail'),
    path('season/<slug:season_slug>/match/create/', create_match_view, name='create_match'),
]
