from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from team.models import Team, Season
import datetime


class TestHomeViews(TestCase):
    def test_home_view_accessible(self):
        """The home page should load successfully for all users."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home.html")

    def test_dashboard_view_requires_login(self):
        """The dashboard view should redirect unauthenticated users to login."""
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, "/accounts/login/?next=/dashboard/")

    def test_dashboard_view_displays_seasons_for_logged_in_user(self):
        """Dashboard should display the logged-in user's team and seasons."""
        user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

        team = Team.objects.create(
            name="Test Team",
            short_name="TT",
            city="Nowhere",
            country="Neverland",
            contributor=user,
        )

        season = Season.objects.create(
            team=team,
            start_date=datetime.date(2024, 8, 1),
            end_date=datetime.date(2025, 5, 20),
            contributor=user,
            competition_list="Championship",
        )

        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/dashboard.html")
        self.assertIn("team", response.context)
        self.assertEqual(response.context["team"], team)
        self.assertIn("seasons", response.context)
        self.assertIn(season, response.context["seasons"])
