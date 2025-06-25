from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from team.models import Team, Season, Match
import datetime


class TestTSVImportView(TestCase):
    """Tests for the TSV match import functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="importer", password="importpass"
        )
        self.client.login(username="importer", password="importpass")
        self.team = Team.objects.create(
            name="Charlton Athletic",
            country="England",
            city="London",
            contributor=self.user,
        )
        self.season = Season.objects.create(
            team=self.team,
            contributor=self.user,
            start_date=datetime.date(2024, 8, 1),
            end_date=datetime.date(2025, 5, 30),
        )
        self.url = reverse(
            "import_matches", args=[self.team.slug, self.season.slug]
        )

    def post_tsv(self, content: str):
        """Helper to simulate TSV file upload."""
        file = SimpleUploadedFile(
            "matches.tsv",
            content.encode("utf-8"),
            content_type="text/tab-separated-values",
        )
        return self.client.post(self.url, {"tsv_file": file})

    def test_valid_tsv_import(self):
        """A valid TSV file should create a new match entry."""
        tsv_data = "date\topponent\n2024-08-10\tWigan Athletic"
        response = self.post_tsv(tsv_data)
        self.assertEqual(Match.objects.count(), 1)
        match = Match.objects.first()
        self.assertEqual(match.opponent, "Wigan Athletic")
        self.assertRedirects(
            response,
            reverse("season_detail", args=[self.team.slug, self.season.slug]),
        )

    def test_missing_required_fields(self):
        """TSV upload missing required headers should fail."""
        tsv_data = "date\ttime\n2024-08-10\t15:00"
        response = self.post_tsv(tsv_data)
        self.assertEqual(Match.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(
            any("Missing required fields" in str(m) for m in messages)
        )

    def test_invalid_date_format(self):
        """TSV upload with invalid date should fail gracefully."""
        tsv_data = "date\topponent\n08/10/2024\tWigan Athletic"
        response = self.post_tsv(tsv_data)
        self.assertEqual(Match.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Import failed" in str(m) for m in messages))

    def test_is_home_field_variants(self):
        """TSV import accepts variants like 'H', 'home', '1' for is_home."""
        tsv_data = "date\topponent\tis_home\n2024-08-10\tWigan Athletic\tH"
        self.post_tsv(tsv_data)
        match = Match.objects.first()
        self.assertTrue(match.is_home)

        tsv_data = "date\topponent\tis_home\n2024-08-17\tLeeds United\tA"
        self.post_tsv(tsv_data)
        match = Match.objects.last()
        self.assertFalse(match.is_home)

    def test_optional_fields_parsed_correctly(self):
        """Optional fields like goals, round, attendance should be handled."""
        tsv_data = (
            "date\topponent\tgoals\tround\tattendance\n"
            "2024-08-10\tWigan Athletic\tSmith 45+2, Jones 83\tGroup Stage\t25000"
        )
        self.post_tsv(tsv_data)
        match = Match.objects.first()
        self.assertEqual(match.goals, "Smith 45+2, Jones 83")
        self.assertEqual(match.round, "Group Stage")
        self.assertEqual(match.attendance, 25000)

    def test_empty_tsv_file(self):
        """Empty TSV file returns error about missing headers."""
        tsv_data = ""
        response = self.post_tsv(tsv_data)
        self.assertEqual(Match.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(
            any("missing a header row" in str(m) for m in messages)
        )

    def test_malformed_time_is_handled_gracefully(self):
        """Malformed time input is caught and handled without crash."""
        tsv_data = (
            "date\topponent\ttime\n" "2024-08-10\tWigan Athletic\tinvalid-time"
        )
        response = self.post_tsv(tsv_data)
        self.assertEqual(Match.objects.count(), 1)
        match = Match.objects.first()
        self.assertIsNone(match.time)

    def test_get_request_renders_import_form(self):
        """GET request returns the TSV import form page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "team/import_matches.html")
        self.assertIn("form", response.context)
