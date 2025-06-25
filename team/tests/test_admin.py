from django.contrib.admin.sites import site
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from team.models import Team, Season, Match

User = get_user_model()


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")

    def test_team_admin_registered(self):
        """Team model is registered in the admin site"""
        self.assertIn(Team, site._registry)

    def test_season_admin_registered(self):
        """Season model is registered in the admin site"""
        self.assertIn(Season, site._registry)

    def test_match_admin_registered(self):
        """Match model is registered in the admin site"""
        self.assertIn(Match, site._registry)

    def test_team_admin_page_loads(self):
        """Team admin changelist view loads successfully"""
        url = reverse("admin:team_team_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_season_admin_page_loads(self):
        """Season admin changelist view loads successfully"""
        url = reverse("admin:team_season_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_match_admin_page_loads(self):
        """Match admin changelist view loads successfully"""
        url = reverse("admin:team_match_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
