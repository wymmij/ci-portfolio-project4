from django.contrib import admin
from .models import Team, Season


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'city', 'country', 'contributor')
    search_fields = ('name', 'short_name', 'city', 'country')

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('team', 'start_date', 'end_date', 'contributor')
    list_filter = ('team', 'contributor')
    search_fields = ('team__name',)
