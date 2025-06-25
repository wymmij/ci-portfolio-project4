from django.test import TestCase
from team.forms import TeamSelectionForm, SeasonForm, MatchForm
from team.models import User, Team, Season
from datetime import date


class TestTeamSelectionForm(TestCase):

    def test_valid_form(self):
        """Form is valid when all required Team fields are provided."""
        form = TeamSelectionForm(
            data={
                "name": "Sheffield Wednesday",
                "short_name": "SWFC",
                "city": "Sheffield",
                "country": "England",
                "is_public": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Form is invalid when required Team fields are missing."""
        form = TeamSelectionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("city", form.errors)
        self.assertIn("country", form.errors)


class TestSeasonForm(TestCase):

    def test_valid_form(self):
        """Season form accepts valid date range and competition list."""
        form = SeasonForm(
            data={
                "start_date": date(2024, 8, 1),
                "end_date": date(2025, 5, 20),
                "competition_list": "Championship, FA Cup",
            }
        )
        self.assertTrue(form.is_valid())

    def test_blank_competitions_is_allowed(self):
        """Form is valid when competition_list is left empty."""
        form = SeasonForm(
            data={
                "start_date": date(2024, 8, 1),
                "end_date": date(2025, 5, 20),
                "competition_list": "",
            }
        )
        self.assertTrue(form.is_valid())


class TestMatchForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.team = Team.objects.create(
            name="Sheffield Wednesday",
            country="England",
            contributor=self.user,
        )
        self.season = Season.objects.create(
            team=self.team,
            contributor=self.user,
            start_date=date(2024, 8, 1),
            end_date=date(2025, 5, 20),
            competition_list="Championship, FA Cup",
        )

    def test_valid_form_with_season_context(self):
        """Match form is valid when required fields and season context are provided."""
        form = MatchForm(
            data={
                "date": date(2024, 9, 1),
                "opponent": "Leeds United",
                "is_home": True,
                "competition": "Championship",
                "round": "Matchday 1",
            },
            season=self.season,
        )
        self.assertTrue(form.is_valid())

    def test_competition_choices_are_set(self):
        """Competition field choices are populated from the related season’s competitions."""
        form = MatchForm(season=self.season)
        expected_choices = [
            ("Championship", "Championship"),
            ("FA Cup", "FA Cup"),
        ]
        self.assertEqual(form.fields["competition"].choices, expected_choices)

    def test_competition_dropdown_uses_season_competitions(self):
        """Season competitions appear in competition field choices."""
        form = MatchForm(season=self.season)
        self.assertIn(
            ("Championship", "Championship"),
            form.fields["competition"].choices,
        )
        self.assertIn(("FA Cup", "FA Cup"), form.fields["competition"].choices)

    def test_missing_required_fields(self):
        """Form is invalid when required Match fields are missing."""
        form = MatchForm(data={}, season=self.season)
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)
        self.assertIn("opponent", form.errors)

    def test_goals_field_accepts_valid_text(self):
        """Form is valid when a well-formatted goals string is provided."""
        form = MatchForm(
            data={
                "date": date(2024, 9, 1),
                "opponent": "Leeds United",
                "is_home": True,
                "competition": "Championship",
                "round": "Matchday 1",
                "team_score": 3,
                "opponent_score": 1,
                "goals": "Smith 45+2, Windass 78, Bannan 90+1",
            },
            season=self.season,
        )
        self.assertTrue(form.is_valid())

    def test_invalid_date_format_rejected(self):
        """Form is invalid when date format is incorrect."""
        form = MatchForm(
            data={
                "date": "invalid-date",
                "opponent": "Leeds United",
                "is_home": True,
            },
            season=self.season,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

    def test_attendance_must_be_positive_integer(self):
        """Form is invalid when attendance is non-numeric."""
        form = MatchForm(
            data={
                "date": date(2024, 9, 1),
                "opponent": "Leeds United",
                "is_home": True,
                "attendance": "thirty thousand",
            },
            season=self.season,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("attendance", form.errors)
