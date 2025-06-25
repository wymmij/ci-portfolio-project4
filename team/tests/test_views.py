from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, time
from team.models import Team, Season, Match


class TestChooseTeamView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

    def test_get_form_when_no_team_exists(self):
        response = self.client.get(reverse("choose_team"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertIn("form", response.context)

    def test_redirect_if_team_already_exists(self):
        self.user.teams.create(
            name="Sheffield Wednesday",
            short_name="Sheff Weds",
            country="England",
            contributor=self.user,
        )
        response = self.client.get(reverse("choose_team"))
        self.assertRedirects(response, reverse("dashboard"))

    def test_post_valid_form_creates_team(self):
        response = self.client.post(
            reverse("choose_team"),
            {
                "name": "Sheffield Wednesday",
                "short_name": "Sheff Weds",
                "city": "Sheffield",
                "country": "England",
                "is_public": True,
            },
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(
            self.user.teams.filter(name="Sheffield Wednesday").exists()
        )


class TestCreateSeasonView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.team = self.user.teams.create(
            name="SWFC",
            short_name="Wednesday",
            city="Sheffield",
            country="England",
        )
        self.url = reverse("create_season", args=[self.team.slug])

    def test_get_season_form_as_logged_in_user(self):
        """Logged-in user sees the season creation form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")
        self.assertIn("form", response.context)

    def test_post_valid_season_form_creates_season(self):
        """Posting valid data creates a new season and redirects."""
        data = {
            "start_date": date(2024, 8, 1),
            "end_date": date(2025, 5, 10),
            "competition_list": "Championship, FA Cup",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Season.objects.count(), 1)
        season = Season.objects.first()
        self.assertEqual(season.team, self.team)
        self.assertRedirects(
            response,
            reverse("season_detail", args=[self.team.slug, season.slug]),
        )

    def test_post_invalid_season_data_shows_errors(self):
        """Invalid submission re-renders the form with errors."""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "start_date", "This field is required."
        )
        self.assertFormError(
            response, "form", "end_date", "This field is required."
        )

    def test_login_required_to_create_season(self):
        """Unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")


class TestSeasonDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

        self.team = Team.objects.create(
            name="Charlton Athletic",
            short_name="CAFC",
            city="London",
            country="England",
            contributor=self.user,
        )

        self.season = Season.objects.create(
            team=self.team,
            contributor=self.user,
            start_date=date(2024, 8, 1),
            end_date=date(2025, 5, 10),
            competition_list="Championship, FA Cup",
        )

        self.url = reverse(
            "season_detail", args=[self.team.slug, self.season.slug]
        )

    def test_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_season_detail_view_loads_for_logged_in_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.team.name)
        self.assertTemplateUsed(response, "team/season_detail.html")

    def test_only_user_seasons_are_accessible(self):
        other_user = User.objects.create_user(
            username="otheruser", password="testpass"
        )
        other_team = Team.objects.create(
            name="Leeds United",
            city="Leeds",
            country="England",
            contributor=other_user,
        )
        other_season = Season.objects.create(
            team=other_team,
            contributor=other_user,
            start_date=date(2024, 8, 1),
            end_date=date(2025, 5, 10),
            competition_list="Championship",
        )
        url = reverse(
            "season_detail", args=[other_team.slug, other_season.slug]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_matches_are_sorted_by_date(self):
        Match.objects.create(
            season=self.season,
            date=date(2025, 4, 1),
            opponent="Sunderland",
            is_home=True,
        )
        Match.objects.create(
            season=self.season,
            date=date(2024, 8, 1),
            opponent="Millwall",
            is_home=True,
        )
        response = self.client.get(self.url)
        content = response.content.decode()
        self.assertTrue(
            content.index("Millwall") < content.index("Sunderland")
        )


class TestCreateMatchView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.team = self.user.teams.create(
            name="Charlton Athletic",
            short_name="Charlton",
            city="London",
            country="England",
        )
        self.season = Season.objects.create(
            team=self.team,
            contributor=self.user,
            start_date=date(2024, 8, 1),
            end_date=date(2025, 5, 20),
            competition_list="Championship, FA Cup",
        )
        self.url = reverse(
            "create_match", args=[self.team.slug, self.season.slug]
        )

    def test_get_match_form(self):
        """Logged-in user sees the match creation form for their season."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")
        self.assertIn("form", response.context)
        self.assertEqual(response.context["season"], self.season)

    def test_post_valid_match_data_creates_match(self):
        """Posting valid match data creates a Match and redirects to dashboard."""
        data = {
            "date": date(2024, 9, 1),
            "time": time(15, 0),
            "opponent": "Leeds United",
            "is_home": True,
            "competition": "Championship",
            "round": "Matchday 1",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Match.objects.count(), 1)
        match = Match.objects.first()
        self.assertEqual(match.opponent, "Leeds United")
        self.assertRedirects(
            response,
            reverse("season_detail", args=[self.team.slug, self.season.slug]),
        )

    def test_form_rejects_missing_required_fields(self):
        """Missing required match fields results in form error."""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "date", "This field is required."
        )
        self.assertFormError(
            response, "form", "opponent", "This field is required."
        )

    def test_login_required_for_match_creation(self):
        """Anonymous users are redirected to login page."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")


class TestEditMatchView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.team = self.user.teams.create(
            name="Charlton Athletic",
            short_name="CAFC",
            city="London",
            country="England",
        )
        self.season = Season.objects.create(
            team=self.team,
            contributor=self.user,
            start_date=date(2024, 8, 1),
            end_date=date(2025, 5, 10),
            competition_list="Championship",
        )
        self.match = Match.objects.create(
            season=self.season,
            date=date(2024, 9, 1),
            opponent="Sunderland",
            is_home=True,
        )
        self.url = reverse(
            "edit_match",
            args=[self.team.slug, self.season.slug, self.match.id],
        )

    def test_get_edit_form_populates_fields(self):
        """Form pre-fills with existing match data for editing."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sunderland")
        self.assertIn("form", response.context)

    def test_post_valid_edit_updates_match(self):
        """Valid form submission updates the match and redirects."""
        response = self.client.post(
            self.url,
            {
                "date": "2024-09-01",
                "opponent": "Newcastle",
                "is_home": True,
                "competition": "Championship",
                "round": "",
            },
        )
        self.match.refresh_from_db()
        self.assertEqual(self.match.opponent, "Newcastle")
        self.assertRedirects(
            response,
            reverse("season_detail", args=[self.team.slug, self.season.slug]),
        )

    def test_post_invalid_edit_shows_errors(self):
        """Invalid submission shows form validation errors."""
        response = self.client.post(
            self.url,
            {
                "date": "",
                "opponent": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "date", "This field is required."
        )
        self.assertFormError(
            response, "form", "opponent", "This field is required."
        )


class TestDeleteMatchView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.team = self.user.teams.create(
            name="Charlton Athletic",
            short_name="CAFC",
            city="London",
            country="England",
        )
        self.season = Season.objects.create(
            team=self.team,
            contributor=self.user,
            start_date=date(2024, 8, 1),
            end_date=date(2025, 5, 10),
            competition_list="Championship",
        )
        self.match = Match.objects.create(
            season=self.season,
            date=date(2024, 9, 1),
            opponent="Sunderland",
            is_home=True,
        )
        self.url = reverse(
            "delete_match",
            args=[self.team.slug, self.season.slug, self.match.id],
        )

    def test_get_delete_confirmation_page(self):
        """GET request shows the match delete confirmation page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "team/match_confirm_delete.html")
        self.assertContains(response, "Sunderland")

    def test_post_deletes_match_and_redirects(self):
        """POST request deletes the match and redirects to season detail."""
        response = self.client.post(self.url)
        self.assertFalse(Match.objects.filter(id=self.match.id).exists())
        self.assertRedirects(
            response,
            reverse("season_detail", args=[self.team.slug, self.season.slug]),
        )


class TestMatchDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.team = Team.objects.create(
            name="Sheffield Wednesday",
            slug="sheffield-wednesday",
            contributor=self.user,
        )
        self.season = Season.objects.create(
            team=self.team,
            start_date=date(2023, 8, 1),
            end_date=date(2024, 5, 31),
            contributor=self.user,
        )
        self.match = Match.objects.create(
            season=self.season,
            opponent="Leeds United",
            date=date(2023, 9, 15),
            is_home=True,
            team_score=2,
            opponent_score=1,
            attendance=30200,
        )
        self.detail_url = reverse(
            "match_detail",
            args=[self.team.slug, self.season.slug, self.match.id],
        )
        self.client.login(username="testuser", password="password")

    def test_match_detail_view_status_code(self):
        """Returns 200 OK for valid match detail URL."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_match_detail_template_used(self):
        """Renders the correct match detail template."""
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, "team/match_detail.html")

    def test_match_detail_content(self):
        """Displays opponent name and formatted scoreline."""
        response = self.client.get(self.detail_url)
        self.assertContains(response, "Leeds United")
        self.assertContains(response, "2–1")

    def test_match_detail_404_for_invalid_id(self):
        """Returns 404 for non-existent match ID."""
        bad_url = reverse(
            "match_detail", args=[self.team.slug, self.season.slug, 999]
        )
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_attendance_formatting(self):
        """Displays attendance with thousands separator."""
        response = self.client.get(self.detail_url)
        self.assertContains(response, "30,200")
