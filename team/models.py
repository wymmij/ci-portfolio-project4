from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.urls import reverse


# Create your models here.
class Team(models.Model):
    """
    Represents a football team associated with a specific :model:`auth.User` contributor.

    **Fields**
    - ``name``: Full name of the team (must be unique)
    - ``short_name``: Optional abbreviated name for compact display
    - ``city`` and ``country``: Geographic location of the team
    - ``contributor``: ForeignKey to :model:`auth.User`, identifying the user who created the team
    - ``slug``: URL-safe identifier auto-generated from the team name
    - ``is_public``: Visibility flag (future use)

    **Constraints**
    - Enforces uniqueness of team slug per contributor

    **Methods**
    - ``get_display_name``: Returns the short name if available, otherwise the full name
    - ``get_create_season_url``: Constructs the URL to initiate a new season for this team
    """

    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=50, blank=False)
    contributor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="teams"
    )
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        """Return the team name."""
        return self.name

    def get_display_name(self):
        """Return short name if defined, otherwise full name."""
        return self.short_name or self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_create_season_url(self):
        """Return URL for creating a new season for this team."""
        return reverse("create_season", args=[self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contributor", "slug"],
                name="unique_contributor_team_slug",
            )
        ]


class Season(models.Model):
    """
    Encapsulates a single football season for a specific :model:`team.Team`.

    **Fields**
    - ``team``: ForeignKey to :model:`team.Team`, indicating which team the season belongs to
    - ``start_date`` and ``end_date``: Temporal bounds of the season
    - ``contributor``: ForeignKey to :model:`auth.User`, denoting the creator of this season
    - ``competition_list``: Comma-separated competitions (parsed as property)
    - ``slug``: URL slug, derived from season year range

    **Constraints**
    - Enforces uniqueness of season per team by date and slug

    **Properties**
    - ``competitions``: Parses and returns a list of trimmed competition names

    **Methods**
    - ``get_absolute_url``: Returns the URL to this season’s overview
    - ``get_create_match_url``: Returns the URL to create a new match for this season
    """

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    competition_list = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated list of competitions the team has entered for this season.",
    )
    slug = models.SlugField(max_length=10, blank=True)

    def __str__(self):
        """Return season string showing team and date range."""
        start_year = self.start_date.year
        end_year = self.end_date.year
        if start_year == end_year:
            label = f"{start_year}"
        else:
            label = f"{start_year % 100}/{end_year % 100}"
        return f"{self.team.name} {label}"

    @property
    def competitions(self):
        """Return list of competition names from CSV field."""
        return [
            c.strip() for c in self.competition_list.split(",") if c.strip()
        ]

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
        """Return URL to the season detail view."""
        return reverse("season_detail", args=[self.team.slug, self.slug])

    def get_create_match_url(self):
        """Return URL for creating a new match in this season."""
        return reverse("create_match", args=[self.team.slug, self.slug])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team", "start_date", "end_date"],
                name="unique_team_season_dates",
            ),
            models.UniqueConstraint(
                fields=["team", "slug"], name="unique_team_season_slug"
            ),
        ]


class Match(models.Model):
    """
    Represents a single football match within a :model:`team.Season`.

    **Fields**
    - ``season``: ForeignKey to :model:`team.Season`
    - ``date`` and ``time``: Scheduling data
    - ``opponent``: Name of opposing team
    - ``is_home``: Boolean indicating whether the team played at home
    - ``competition`` and ``round``: Metadata about the match
    - ``attendance``: Optional attendance figure
    - ``team_score`` and ``opponent_score``: Final scores
    - ``goals``: Formatted string denoting goal scorers and timings

    **Methods**
    - ``__str__``: Returns a concise textual summary of the match
    - ``outcome``: Returns match result code ('W', 'D', or 'L') based on score
    - ``get_scoreline``: Returns the score as a string, formatted according to home/away status
    - ``get_short_date``: Returns a compact date string (dd-mm-yy)
    - ``get_home_team`` / ``get_away_team``: Returns the name of the teams with HTML formatting, highlighting the contributor’s team
    """

    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    opponent = models.CharField(max_length=100)
    is_home = models.BooleanField(default=True)
    competition = models.CharField(max_length=100, blank=True)
    round = models.CharField(max_length=50, blank=True)
    attendance = models.PositiveIntegerField(null=True, blank=True)
    team_score = models.PositiveSmallIntegerField(null=True, blank=True)
    opponent_score = models.PositiveSmallIntegerField(null=True, blank=True)
    goals = models.TextField(
        blank=True,
        help_text=(
            "Enter goals in format: 'Smith 45+2, 76, Windass 83, Bannan 90+1'. "
            "List scorer names followed by goal minutes. Separate players with commas."
        ),
    )

    def __str__(self):
        """Return human-readable match summary."""
        location = "vs" if self.is_home else "@"
        return f"{self.season.team.short_name or self.season.team.name} {location} {self.opponent} ({self.date})"

    @property
    def outcome(self):
        """Return 'W', 'D', or 'L' based on match result."""
        if self.team_score is None or self.opponent_score is None:
            return ""
        if self.team_score > self.opponent_score:
            return "W"
        elif self.team_score == self.opponent_score:
            return "D"
        else:
            return "L"

    def get_short_date(self):
        """Return date in short dd-mm-yy format."""
        return self.date.strftime("%d-%m-%y")

    def get_scoreline(self):
        """Return formatted score with correct home/away alignment."""
        if self.team_score is None or self.opponent_score is None:
            return ""
        return (
            f"{self.team_score}–{self.opponent_score}"
            if self.is_home
            else f"{self.opponent_score}–{self.team_score}"
        )

    def get_home_team(self):
        """Return formatted home team name, bolding contributor's team."""
        return (
            mark_safe(f"<strong>{self.season.team.name}</strong>")
            if self.is_home
            else self.opponent
        )

    def get_away_team(self):
        """Return formatted away team name, bolding contributor's team."""
        return (
            mark_safe(self.opponent)
            if self.is_home
            else mark_safe(f"<strong>{self.season.team.name}</strong>")
        )
