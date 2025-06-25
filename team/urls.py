from django.urls import path
from .views import (
    choose_team_view,
    create_season_view,
    season_detail_view,
    create_match_view,
    edit_match_view,
    delete_match_view,
    import_matches_view,
    match_detail_view,
)

urlpatterns = [
    path("choose-team/", choose_team_view, name="choose_team"),
    path(
        "<slug:team_slug>/season/create/",
        create_season_view,
        name="create_season",
    ),
    path(
        "<slug:team_slug>/season/<slug:season_slug>/",
        season_detail_view,
        name="season_detail",
    ),
    path(
        "<slug:team_slug>/season/<slug:season_slug>/import/",
        import_matches_view,
        name="import_matches",
    ),
    path(
        "<slug:team_slug>/season/<slug:season_slug>/match/create/",
        create_match_view,
        name="create_match",
    ),
    path(
        "<slug:team_slug>/season/<slug:season_slug>/match/<int:match_id>/edit/",
        edit_match_view,
        name="edit_match",
    ),
    path(
        "<slug:team_slug>/season/<slug:season_slug>/match/<int:match_id>/delete/",
        delete_match_view,
        name="delete_match",
    ),
    path(
        "team/<slug:team_slug>/season/<slug:season_slug>/match/<int:match_id>/",
        match_detail_view,
        name="match_detail",
    ),
]
