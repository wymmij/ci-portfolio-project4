from django.test import TestCase
from django.contrib.auth.models import User
from team.models import Team, Season, Match
from datetime import date, time


class TestTeamModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(
            name='Sheffield Wednesday',
            short_name='SWFC',
            city='Sheffield',
            country='England',
            contributor=self.user
        )

    def test_str_returns_team_name(self):
        """Returns the team name as string representation."""
        self.assertEqual(str(self.team), 'Sheffield Wednesday')

    def test_get_display_name_returns_short_name(self):
        """Returns the short name if set."""
        self.assertEqual(self.team.get_display_name(), 'SWFC')

    def test_get_display_name_falls_back_to_name(self):
        """Falls back to full name if no short name."""
        self.team.short_name = ''
        self.assertEqual(self.team.get_display_name(), 'Sheffield Wednesday')

    def test_get_create_season_url(self):
        """Returns correct URL for creating a season for this team."""
        url = self.team.get_create_season_url()
        self.assertIn(self.team.slug, url)


class TestSeasonModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(
            name='Charlton Athletic',
            city='London',
            country='England',
            contributor=self.user
        )
        self.season = Season.objects.create(
            team=self.team,
            start_date=date(2024, 8, 1),
            end_date=date(2025, 5, 15),
            competition_list='Championship, FA Cup',
            contributor=self.user
        )

    def test_str_returns_expected_format(self):
        """Returns 'Team YY/YY' when season spans two years."""
        self.assertIn('Charlton Athletic', str(self.season))
        self.assertIn('24/25', str(self.season))

    def test_season_str_single_year_format(self):
        """Returns 'Team YYYY' when season starts and ends in the same year."""
        season = Season(
            team=self.team,
            contributor=self.user,
            start_date=date(2024, 3, 1),
            end_date=date(2024, 11, 1)
        )
        self.assertEqual(str(season), 'Charlton Athletic 2024')

    def test_season_slug_single_year_format(self):
        """Generates correct slug for same-year season on save."""
        season = Season(
            team=self.team,
            contributor=self.user,
            start_date=date(2024, 3, 1),
            end_date=date(2024, 11, 1)
        )
        season.save()
        self.assertEqual(season.slug, '2024')    

    def test_competitions_parses_correctly(self):
        """Parses competition_list into individual competition names."""
        self.assertEqual(self.season.competitions, ['Championship', 'FA Cup'])

    def test_get_absolute_url_contains_expected_slugs(self):
        """Returns season detail URL."""
        url = self.season.get_absolute_url()
        self.assertIn(self.team.slug, url)
        self.assertIn(self.season.slug, url)

    def test_get_create_match_url_contains_expected_slugs(self):
        """Returns URL for creating a match in the season."""
        url = self.season.get_create_match_url()
        self.assertIn(self.team.slug, url)
        self.assertIn(self.season.slug, url)


class TestMatchModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(
            name='Fulham',
            city='London',
            country='England',
            contributor=self.user
        )
        self.season = Season.objects.create(
            team=self.team,
            start_date=date(2024, 8, 1),
            end_date=date(2025, 5, 15),
            contributor=self.user
        )
        self.match = Match.objects.create(
            season=self.season,
            date=date(2024, 9, 1),
            time=time(15, 0),
            opponent='QPR',
            is_home=True,
            competition='Championship',
            round='Matchday 1',
            team_score=2,
            opponent_score=1
        )

    def test_str_includes_teams_and_date(self):
        """Returns formatted match string with date and opponent."""
        self.assertIn('Fulham', str(self.match))
        self.assertIn('QPR', str(self.match))
        self.assertIn('2024', str(self.match))

    def test_outcome_home_win(self):
        """Returns 'W' for a win outcome."""
        self.assertEqual(self.match.outcome, 'W')

    def test_outcome_draw(self):
        """Returns 'D' for a draw outcome."""
        self.match.opponent_score = 2
        self.match.save()
        self.assertEqual(self.match.outcome, 'D')

    def test_outcome_loss(self):
        """Returns 'L' for a loss outcome."""
        self.match.opponent_score = 3
        self.match.save()
        self.assertEqual(self.match.outcome, 'L')

    def test_get_short_date_format(self):
        """Displays short date."""
        self.assertEqual(self.match.get_short_date(), '01-09-24')

    def test_get_scoreline_home(self):
        """Displays scoreline from home perspective."""
        self.assertEqual(self.match.get_scoreline(), '2–1')

    def test_get_scoreline_away(self):
        """Displays scoreline from away perspective."""
        self.match.is_home = False
        self.match.save()
        self.assertEqual(self.match.get_scoreline(), '1–2')

    def test_get_home_and_away_teams(self):
        """Returns correct home/away team labels with bold formatting."""
        self.assertEqual(self.match.get_home_team(), '<strong>Fulham</strong>')
        self.assertEqual(self.match.get_away_team(), 'QPR')

