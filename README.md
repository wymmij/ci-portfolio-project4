# ⚽ SeasonWatch

A football season tracking app for fans who love data.

SeasonWatch allows users to record and explore season-by-season data for their favourite football team. It is designed for individual contributors to build their own record of matches, goals, players, and lineups, with the possibility of making that data publicly viewable. The project was developed using the Django web framework and is deployed to Heroku with a PostgreSQL backend.

---

## 📖 Table of Contents

- [⚽ SeasonWatch](#-seasonwatch)
  - [📖 Table of Contents](#-table-of-contents)
  - [🧭 UX Strategy](#-ux-strategy)
  - [👥 User Stories](#-user-stories)
  - [✨ Features](#-features)
    - [Implemented in MVP](#implemented-in-mvp)
    - [Planned for Future Iterations (Post-MVP)](#planned-for-future-iterations-post-mvp)
  - [🗃️ Data Models](#️-data-models)
    - [Team](#team)
    - [Season](#season)
    - [Match](#match)
  - [🧪 Testing](#-testing)
  - [📈 Agile Process](#-agile-process)
  - [🛠️ Technologies Used](#️-technologies-used)
  - [🚀 Deployment](#-deployment)
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

---

## 👥 User Stories

User stories were created at the start of the project and tracked via GitHub Issues and a Kanban-style Project board. Each story was assigned a MoSCoW priority, with 8 forming the MVP.

Sample user stories:

- As a **Contributor**, I can create a season for my team so that I can track all matches played that year.
- As a **Contributor**, I can record match results and scorers so that I can build a complete season overview.
- As a **Fan**, I can view all matches in a season so that I can see how my team performed over time.

Each story includes acceptance criteria and developer-facing tasks.

---

## ✨ Features

### Implemented in MVP

- Secure login/logout via Django AllAuth
- Team selection with option to keep data public or private
- Season creation (start/end dates, competition list)
- Match creation with basic metadata (date, opponent, result, competition)
- Season dashboard view listing all recorded seasons
- Season detail view with list of matches played
- Form validation and success messaging
- Fully styled frontend using Bootstrap 5 and crispy-forms

### Planned for Future Iterations (Post-MVP)

- Lineups and goal scorer tracking
- Player profiles and match appearances
- Data import via CSV/TSV
- Aggregate stats per season (e.g. win/loss record)
- Public-facing URLs for shared data

---

## 🗃️ Data Models

The following models form the core of the application:

### Team

- name (unique per contributor)
- city, country
- contributor (FK to User)
- slug (auto-generated from name)

### Season

- team (FK)
- start_date, end_date
- competition_list (comma-separated)
- contributor (FK)
- slug (auto-generated from date range)

### Match

- season (FK)
- date, time
- opponent, is_home
- competition, round
- team_score, opponent_score
- attendance (optional)

Further models (e.g. Player, Goal, Lineup) are scaffolded but not implemented in the MVP.

---

## 🧪 Testing

Testing was conducted using Django's `TestCase`, structured around:

- **Forms**: Valid/invalid inputs for Team, Season, and Match forms
- **Views**: GET and POST requests for each core route
- **Redirect logic** and login gating verified
- Tests are grouped in `tests/` directory under each app
- TDD was used where feasible

Tests directly align with MVP user story acceptance criteria.

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

Deployed to Heroku with settings managed via `env.py` and Heroku Config Vars.

- Static files served via WhiteNoise
- Local development uses SQLite; production uses PostgreSQL
- Deployment checklist included in README

---

## 📝 Credits

- Code Institute walkthroughs and Django module
- Bootstrap documentation
- GitHub Copilot and ChatGPT for rapid problem-solving
- Project scaffolding inspired by Code Institute's blog project
