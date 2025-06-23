from django.contrib import admin
from .models import Team, Season, Match

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'city', 'country', 'contributor')
    search_fields = ('name', 'short_name', 'city', 'country')

class MatchInline(admin.TabularInline):
    model = Match
    extra = 0
    
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('team', 'start_date', 'end_date', 'contributor', 'competition_list')
    list_filter = ('team', 'contributor')
    search_fields = ('team__name',)
    inlines = [MatchInline]

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('date', 'opponent', 'season', 'competition', 'is_home')
    list_filter = ('season', 'is_home')
    search_fields = ('opponent', 'competition')
