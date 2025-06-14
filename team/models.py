from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def get_display_name(self):
        return self.short_name or self.name


class Season(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=10, unique=True)

    def __str__(self):
        start_year = self.start_date.year
        end_year = self.end_date.year
        if start_year == end_year:
            label = f"{start_year}"
        else:
            label = f"{start_year % 100}/{end_year % 100}"
        return f"{self.team.name} {label}"

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

    class Meta:
        unique_together = ('team', 'start_date', 'end_date')


class Match(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    date = models.DateField()
    opponent = models.CharField(max_length=100)
    is_home = models.BooleanField(default=True)
    team_score = models.PositiveSmallIntegerField(null=True, blank=True)
    opponent_score = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        location = "vs" if self.is_home else "@"
        return f"{self.season.team.short_name or self.season.team.name} {location} {self.opponent} ({self.date})"
