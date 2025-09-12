# ⚽ SeasonWatch

A football season tracking app for fans who love data.

SeasonWatch allows users to record and explore season-by-season data for their favourite football team. It is designed for individual contributors to build their own record of matches, goals, players, and lineups, with the possibility of making that data publicly viewable. The project was developed using the Django web framework and is deployed to Heroku with a PostgreSQL backend.

---

## 📖 Table of Contents

- [⚽ SeasonWatch](#-seasonwatch)
  - [📖 Table of Contents](#-table-of-contents)
  - [🧭 UX Strategy](#-ux-strategy)
    - [📂 Sample Data](#-sample-data)
  - [👥 User Stories](#-user-stories)
    - [Contributor Features](#contributor-features)
    - [Admin Features](#admin-features)
  - [Screenshots](#screenshots)
  - [🗃️ Data Models](#️-data-models)
    - [Team](#team)
    - [Season](#season)
    - [Match](#match)
    - [Entity Relationship Summary](#entity-relationship-summary)
  - [🧪 Manual Testing](#-manual-testing)
    - [Authentication and Navigation](#authentication-and-navigation)
    - [CRUD Functionality](#crud-functionality)
    - [TSV Import Functionality](#tsv-import-functionality)
    - [UI Behavior](#ui-behavior)
    - [HTML \& Code Validation](#html--code-validation)
    - [Admin Dashboard Testing](#admin-dashboard-testing)
  - [Automated Testing](#automated-testing)
    - [Components Covered by Tests](#components-covered-by-tests)
  - [📈 Agile Process](#-agile-process)
  - [🛠️ Technologies Used](#️-technologies-used)
  - [🚀 Deployment](#-deployment)
    - [Local Development Setup](#local-development-setup)
      - [Prerequisites](#prerequisites)
      - [Database Requirements](#database-requirements)
      - [Get the source code](#get-the-source-code)
      - [Create and Activate Virtual Environment](#create-and-activate-virtual-environment)
      - [Install Dependencies](#install-dependencies)
      - [Configure Local Environment](#configure-local-environment)
      - [Run Migrations and Create Superuser](#run-migrations-and-create-superuser)
      - [Start the Development Server](#start-the-development-server)
    - [Production Deployment (Heroku)](#production-deployment-heroku)
      - [Method A - Heroku Web UI](#method-a---heroku-web-ui)
      - [Method B — Heroku CLI](#method-b--heroku-cli)
  - [📝 Credits](#-credits)

---

## 🧭 UX Strategy

This app is designed for football fans who want a personal and editable season log. Many fans keep informal spreadsheets of club stats; SeasonWatch offers a structured, scalable alternative.

> "It’s not just about the data, but about the process of recording it."

- Fans can track their favourite team's matches
- Contributors can create and manage season data
- Data can be optionally made public

The UX prioritises:

- Clean, readable layout
- Familiar, form-based data entry
- Logical URL patterns and routes per user/team/season

> After creating an account, you can upload sample match data using the TSV import feature and the provided file in the (data/) folder.

### 📂 Sample Data

A sample TSV file is included in the data/ directory of the project repository. After registering an account and logging in, you can upload this file via the Import Matches interface to populate the system with sample season data. This is a quick way to explore the application's functionality without manually entering matches.

---

## 👥 User Stories

This project was developed using Agile principles. [Full user stories are documented](https://github.com/users/wymmij/projects/3/views/1) . Below is a summary of MVP features:

### Contributor Features

- Register and authenticate securely
- Create, edit, and delete:
  - Seasons
  - Matches
  - Individual match details
- TSV import for bulk match entry
- Filter dashboard to show only own data
- View season and match details (read-only access for own content)

### Admin Features

- Access all contributor data through the Django admin dashboard
- View, search, and filter all user-submitted content
- Identify which user created each entry
- Admin-only access secured via Django’s permissions system

Post-MVP plans include lineup tracking, substitutions, enhanced match analytics, and CSV export/import functionality.

---

## Screenshots

![User dashboard](docs/dashboard.png)

![New season dialogue](docs/new_season_dialog.png)

![Season detail view](docs/season_detail.png)

## 🗃️ Data Models

The application's data model consists of three core entities: `Team`, `Season`, and `Match`, all linked to a `User` from Django's built-in authentication system. These models form a relational structure supporting the full tracking of team performance across seasons and matches. A simplified ERD is shown below.

![Entity Relationship Diagram](docs/erd.png)

### Team

Represents a football team contributed by a registered user.

- **Fields**:
  - `name`: Full name of the team (unique)
  - `short_name`: Optional abbreviation for display
  - `city`, `country`: Location data
  - `slug`: URL-safe identifier
  - `contributor`: Foreign key to `User`
  - `is_public`: Visibility toggle
- **Relationships**:
  - One `User` can create multiple `Teams`
  - A `Team` can have many `Seasons`

### Season

Encapsulates a single season for a given team.

- **Fields**:
  - `start_date`, `end_date`: Temporal range
  - `competition_list`: Comma-separated list of entered competitions
  - `slug`: Year-based slug (e.g., `23-24`)
  - `contributor`: Redundant foreign key for filtering and permission control
- **Relationships**:
  - A `Team` has many `Seasons`
  - A `Season` has many `Matches`

### Match

Represents an individual football match within a given season.

- **Fields**:
  - `date`, `time`: Scheduling information
  - `opponent`, `competition`, `round`: Metadata
  - `is_home`: Home or away flag
  - `attendance`: Optional integer
  - `team_score`, `opponent_score`: Optional integers
  - `goals`: Free-text goal description
- **Derived Data**:
  - Outcome (`W`, `D`, `L`) inferred from scores
  - Dynamic rendering of team names and scorelines

---

### Entity Relationship Summary

```plaintext
User
 └───┬───> Team
     └───┬───> Season
         └───> Match
```

- Each **User** owns one or more **Teams**
- Each **Team** can have multiple **Seasons**
- Each **Season** can include many **Matches**

---

## 🧪 Manual Testing

Throughout the development of the project, extensive manual testing was performed to ensure that core functionality behaved as expected. Testing was done iteratively, with each new feature verified both through the web interface and directly via the PostgreSQL database using command-line queries. This approach confirmed that data was being handled correctly at every stage.

### Authentication and Navigation

- ✅ Verified user registration, login, and logout workflows.
- ✅ Confirmed redirection behavior (e.g., post-login redirect to dashboard).
- ✅ Checked access control: contributors cannot access or modify data belonging to others.

### CRUD Functionality

- ✅ Created, updated, and deleted Seasons and Matches via the UI.
- ✅ Verified results directly in the database to ensure entries were correctly added or removed.
- ✅ Ensured form submissions with invalid or incomplete data did not create database entries.
- ✅ Checked that deleting a Season cascaded to remove associated Matches as expected.

### TSV Import Functionality

- ✅ Uploaded TSV files to create matches in bulk.
- ✅ Tested import with fully correct data — confirmed all rows were added.
- ✅ Tested import with partially malformed data — confirmed valid rows were added and invalid ones were ignored.
- ⚠️ **Known limitation**: The current import process does not display an error message when malformed rows are skipped. Enhancements are planned post-MVP to provide user feedback on parsing errors.

### UI Behavior

- ✅ Confirmed all views load as expected across multiple test scenarios.
- ✅ Used browser-based testing to ensure forms retain input values on error and redirect appropriately on success.
- ✅ Performed visual checks to confirm layout consistency and responsiveness (limited to desktop view).

### HTML & Code Validation

- ✅ **HTML**: All key templates were validated using the W3C HTML Validator. Pages passed with only minor, non-critical warnings (e.g., self-closing tags).
- ✅ **Python**: Code was linted using **Flake8** with a project-level configuration (`.flake8`).

  - Issues originally flagged (e.g., long lines, unused imports in placeholder files) have been resolved.
  - Auto-formatting (via Black) and manual adjustments (string splitting, removal of unused imports) brought all Python files into compliance.
  - Virtual environment and auto-generated Django migration files were excluded from checks.
- ✅ All project code now passes linting without errors.

### Admin Dashboard Testing

- ✅ Used the Django admin interface extensively during early development to inspect, add, and delete model instances before front-end forms were fully implemented.
- ✅ Verified that all major models (Team, Season, Match, Player, Goal) were properly registered in `admin.py`.
- ✅ Confirmed that each model includes contributor information, enabling attribution and filtering by user.
- ✅ Tested that list display fields, search functionality, and filters were correctly configured for each model.
- ✅ Verified that only superusers (admin accounts) could access the admin interface.
- ✅ Confirmed successful deletion of items via the admin dashboard and verified database changes via command-line PostgreSQL queries.
- ✅ Ensured relational integrity: for example, deleting a season or team did not leave behind orphaned matches or goals.

> Manual testing was conducted continuously throughout the project, not as a discrete phase but as an integral part of the development cycle. This helped ensure stability, catch edge cases early, and confirm that each new feature behaved exactly as expected in realistic usage scenarios.

---

## Automated Testing

The project followed a test-driven development (TDD) approach wherever feasible. While this required deliberate effort and discipline, the payoff became particularly evident during those phases of development where the precise feature requirements were still being clarified. Writing tests first helped define expectations more clearly and reduced the risk of building unnecessary or brittle logic.

That said, adhering to TDD was more challenging when the feature seemed obvious from the outset — a common pitfall for novice developers is to prematurely assume the correct structure, only to find later that tests would have uncovered weaknesses earlier. Nonetheless, the project settled into a productive rhythm of building out features and their corresponding tests in tandem. This workflow made it easier to catch regressions early, as newly introduced features could be immediately tested against previously working functionality.

Efforts were also made to ensure that testing was closely aligned with the defined User Stories. Many stories explicitly required testing as part of their **Acceptance Criteria**, and the development process was shaped accordingly to ensure each user-facing feature was properly validated through tests.

The `coverage` Python package was used throughout development to ensure a high level of test completeness. Effort was made to maintain **100% test coverage** for all code within the MVP scope.

### Components Covered by Tests

- User registration and authentication
- Contributor access control and permissions
- Creation and update of:
  - Seasons
  - Matches
  - Players
  - Goals
- Match detail views and season overviews
- TSV import logic (including edge cases)
- Visibility filtering by contributor
- Access restrictions for non-owners
- Admin dashboard model registration

To run the full suite of tests and display a coverage report:

```bash
coverage run --source='.' manage.py test
coverage report
```

Alternatively, to generate a browsable HTML report:

```bash
coverage html
```

---

## 📈 Agile Process

The project followed Agile methodology:

- GitHub Project board used to manage tasks
- User stories defined and tracked via issues
- MoSCoW priorities assigned (Must, Should, Could, Won't)
- One milestone used for the MVP Sprint
- Daily check-ins used to reassess scope and update tasks
- README updated incrementally alongside code

---

## 🛠️ Technologies Used

- Python 3.13
- Django 4.2.20
- PostgreSQL (Neon DB hosted via Code Institute)
- Heroku for deployment
- Bootstrap 5 + crispy-bootstrap5 for UI
- Cloudinary (planned, not implemented in MVP)
- Git & GitHub for version control and project planning

---

## 🚀 Deployment

There are multiple valid ways to deploy a Django project, depending on the tools and hosting services chosen (e.g. different cloud platforms, database backends, or deployment methods).
For this project, I describe the exact process used:

- Local development with Python 3
- Deployment to Heroku using the **GitHub integration** method
- A Postgres database provided via a cloud provider

---

### Local Development Setup

#### Prerequisites

- Python (tested with **3.13.7**; Django 4.x officially supports Python ≥3.8)
- Git

> [!NOTE]
> You may use any code editor or IDE for development. The steps below are editor-agnostic and assume only that you have Git and Python installed locally.

---

#### Database Requirements

This project requires a **Postgres database**, configured via the `DATABASE_URL` environment variable.

- The connection string must follow the standard format:

  ```conf
  postgres://USER:PASSWORD@HOST:PORT/DBNAME
  ```

- In production (e.g. on Heroku), this variable is typically set automatically when you provision a Postgres add-on or other managed database service.
- For local development, you may either:

  - Run a local Postgres server, or
  - Point `DATABASE_URL` to any accessible Postgres instance (e.g. on a cloud provider).

Postgres is required for deployment. SQLite may work for experimentation but is not supported here.

---

#### Get the source code

To deploy this project using **Heroku GitHub integration**, you must have a GitHub account and a repository under your own account (Heroku can only connect to repositories you control).

1. **Fork this repository** on GitHub. This creates a copy of the project under your own GitHub account. Forking is required because Heroku GitHub integration can only connect to repositories you own.
2. **Clone your fork locally** to your development machine:

   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

This ensures you both:

- have a local copy for development and testing, and
- have a GitHub-hosted repository you own, which Heroku can connect to for deployment.

---

#### Create and Activate Virtual Environment

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1
```

(Other tools such as Pipenv or Poetry can be used, but `venv` is sufficient here.)

---

#### Install Dependencies

```bash
pip install -r requirements.txt
```

---

#### Configure Local Environment

Create a file called **`env.py`** at the project root with the following content:

```python
import os

os.environ.setdefault("DATABASE_URL", "postgres://USER:PASSWORD@HOST:PORT/DBNAME")
os.environ.setdefault("SECRET_KEY", "your-secret-key")
os.environ.setdefault("DEBUG", "True")
```

- **SECRET\_KEY:** a random string used for cryptographic signing in Django.
  To generate one quickly:

  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```

- **DEBUG:** should be `"True"` only in local development. In production, always set `"False"`.

Ensure your `settings.py` reads `DEBUG` as:

```python
DEBUG = os.environ.get("DEBUG", "False") == "True"
```

If `DEBUG` is not set, it defaults to `False`, which is correct for production (e.g. on Heroku).

---

#### Run Migrations and Create Superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

> [!NOTE]
> All required migration files are included in the repository; you only need to apply them with migrate.

---

#### Start the Development Server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and log into `/admin/` with your superuser.

---

### Production Deployment (Heroku)

This application is hosted on [Heroku](https://www.heroku.com), a cloud-based platform-as-a-service. Deployment can be done via the **Heroku Web UI** or the **Heroku CLI**. Both of the following methods assume you already have a Heroku account. Each results in the app being deployed to Heroku and connected to a Postgres database specified by `DATABASE_URL`.

---

#### Method A - Heroku Web UI

1. Log in to your Heroku account.
2. Click **New** → **Create new app**.
3. Choose a unique app name and region, then **Create app**.
4. Go to the **Settings** tab → **Reveal Config Vars**.

   - Add `SECRET_KEY` with a new random value.
   - Add `DATABASE_URL` with the connection string to your Postgres database (if using Heroku Postgres, this is auto-added).
5. Go to the **Deploy** tab.

   - In **Deployment method**, select **GitHub**.
   - Under **Connect to GitHub**, link your repository.
   - In **Manual Deploy**, choose the branch (e.g. `main`) and click **Deploy Branch**.
6. Once deployed, if this app is pointing to a new or empty database, initialize it via **More → Run Console**:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. Click **Open App**.

---

#### Method B — Heroku CLI

```bash
# Log in
heroku login

# Create an app (choose a unique name)
heroku create <your-heroku-app> --region eu

# Set config vars
heroku config:set SECRET_KEY=<random> DATABASE_URL=<your-database-url> -a <your-heroku-app>

# Connect the GitHub repo to this app (so pushes go to Heroku)
heroku git:remote -a <your-heroku-app>

# Deploy (push code to Heroku)
git push heroku main

# (Optional) Run migrations, only if this app is pointing to a new or empty DB
# heroku run python manage.py migrate -a <your-heroku-app>
# heroku run python manage.py createsuperuser -a <your-heroku-app>

# Open the app in the browser
heroku open -a <your-heroku-app>
```

> [!NOTE]
>
> - If your development and production environments share the same Postgres instance, the schema will already exist and no migrations are needed at deploy time.
> - If you point the Heroku app at a fresh Postgres database, you must run `migrate` and create a superuser there.

---

## 📝 Credits

- [Code Institute](https://codeinstitute.net/) walkthroughs and Django module
- Project scaffolding inspired by Code Institute's blog project
- [Bootstrap documentation](https://getbootstrap.com/docs/4.6/getting-started/introduction/)
- Icons by [Font Awesome](https://fontawesome.com/)
- ChatGPT for generation of the ERD
- Sheffield Wednesday FC for historical data, WAWAW!
