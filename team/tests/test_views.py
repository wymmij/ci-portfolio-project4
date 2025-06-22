from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from team.models import Team, Season
from datetime import date


class TestChooseTeamView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_form_when_no_team_exists(self):
        response = self.client.get(reverse('choose_team'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertIn('form', response.context)

    def test_redirect_if_team_already_exists(self):
        self.user.teams.create(
            name='Sheffield Wednesday',
            short_name='Sheff Weds',
            country='England',
            contributor=self.user
        )
        response = self.client.get(reverse('choose_team'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_post_valid_form_creates_team(self):
        response = self.client.post(reverse('choose_team'), {
            'name': 'Sheffield Wednesday',
            'short_name': 'Sheff Weds',
            'city': 'Sheffield',
            'country': 'England',
            'is_public': True
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(self.user.teams.filter(name='Sheffield Wednesday').exists())


class TestCreateSeasonView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.team = self.user.teams.create(
            name='SWFC', 
            short_name='Wednesday', 
            city='Sheffield',
            country='England')
        self.url = reverse('create_season', args=[self.team.slug])

    def test_get_season_form_as_logged_in_user(self):
        """Logged-in user sees the season creation form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertIn('form', response.context)

    def test_post_valid_season_form_creates_season(self):
        """Posting valid data creates a new season and redirects."""
        data = {
            'start_date': '2024-08-01',
            'end_date': '2025-05-10',
            'competition_list': 'Championship, FA Cup'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Season.objects.count(), 1)
        season = Season.objects.first()
        self.assertEqual(season.team, self.team)
        self.assertRedirects(response, reverse('season_detail', args=[self.team.slug, season.slug]))

    def test_post_invalid_season_data_shows_errors(self):
        """Invalid submission re-renders the form with errors."""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'start_date', 'This field is required.')
        self.assertFormError(response, 'form', 'end_date', 'This field is required.')

    def test_login_required_to_create_season(self):
        """Unauthenticated users are redirected to login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

