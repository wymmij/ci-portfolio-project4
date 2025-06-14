from django.urls import path
from .views import choose_team_view

urlpatterns = [
    path('choose-team/', choose_team_view, name='choose_team'),
]
