from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=50, blank=False)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
    def get_display_name(self):
        return self.short_name or self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_create_season_url(self):
        return reverse('create_season', args=[self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['contributor', 'slug'], name='unique_contributor_team_slug')
        ]


class Season(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    competition_list = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated list of competitions the team has entered for this season."
    )
    slug = models.SlugField(max_length=10, blank=True)

    def __str__(self):
        start_year = self.start_date.year
        end_year = self.end_date.year
        if start_year == end_year:
            label = f"{start_year}"
        else:
            label = f"{start_year % 100}/{end_year % 100}"
        return f"{self.team.name} {label}"
    
    @property
    def competitions(self):
        return [c.strip() for c in self.competition_list.split(',') if c.strip()]

    def save(self, *args, **kwargs):
        if not self.slug:
            start_year = self.start_date.year
            end_year = self.end_date.year
            if start_year == end_year:
                label = f"{start_year}"
            else:
                label = f"{start_year % 100}-{end_year % 100}"
            self.slug = slugify(label)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('season_detail', args=[self.team.slug, self.slug])
    
    def get_create_match_url(self):
        return reverse('create_match', args=[self.team.slug, self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'start_date', 'end_date'], name='unique_team_season_dates'),
            models.UniqueConstraint(fields=['team', 'slug'], name='unique_team_season_slug'),
        ]


class Match(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    opponent = models.CharField(max_length=100)
    is_home = models.BooleanField(default=True)
    competition = models.CharField(max_length=100, blank=True)
    round = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. 'Quarter-Final', 'Round 3', 'Group Stage', etc."
    )
    attendance = models.PositiveIntegerField(null=True, blank=True)
    team_score = models.PositiveSmallIntegerField(null=True, blank=True)
    opponent_score = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        location = "vs" if self.is_home else "@"
        return f"{self.season.team.short_name or self.season.team.name} {location} {self.opponent} ({self.date})"

