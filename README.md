# SeasonWatch

SeasonWatch is a web application for football fans who want to build a structured, personal record of their favourite club’s historical performance. The system supports logging of seasons, matches, players, and detailed appearances, all from a clean and user-friendly interface.

This version of SeasonWatch is seeded with data from Sheffield Wednesday FC, but supports any club a user wishes to document.

---

## 🎯 Project Goals

- Demonstrate practical application of Django within a Full-Stack project
- Solve a real user problem: structured long-term tracking of football club history
- Showcase agile development principles, front-end CRUD, custom models, and robust testing
- Deliver a user-friendly, accessible, and well-documented interface

---

## 👥 User Stories

---

## 🗃️ Models

| Model        | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `Season`     | Represents one season of club history (year, manager, goals, league result) |
| `Match`      | A specific game: opponent, score, competition, location                     |
| `Player`     | Basic player info including position and career timeline                    |
| `Appearance` | A many-to-many model linking players to specific matches, with match stats  |
| `Manager`    | Manager name and dates (optional relational model)                          |

All models are original and reflect domain-specific design.

---

## 🛠️ Technologies Used

- Django
- HTML / CSS
- PostgreSQL
- JavaScript (vanilla and jQuery)
- GitHub Projects (Agile planning)
- Django’s built-in testing framework

---

## 🧪 Testing

This project includes:

- Unit tests for all custom models
- View tests to check access control and expected behavior
- Form validation tests
- Manual testing notes and user flow validation

Test coverage targets key CRUD operations and user workflows. Tests are written using Django’s `TestCase` framework and can be found in `tracker/tests/`.

---

## 🚀 Deployment

This project is deployed on Heroku. The live version is accessible at:

[👉 Deployed Link Here]

The database is hosted via PostgreSQL, and all secret keys and credentials are stored securely in environment variables.

---

## 📈 Agile Methodology

This project was developed using Agile principles:

- A GitHub Project board was used to track tasks and user stories
- Issues were broken down into discrete, manageable chunks
- Regular commits reflect story-based development
- The board is [publicly visible here](https://github.com/wymmij/ci-portfolio-project4/projects/1)

---

## 📁 Project Structure

---

## 📝 Credits

- Sheffield Wednesday FC historical data provided by the author
- Course guidance and structure by Code Institute
