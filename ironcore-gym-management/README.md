# IronCore — Gym Management System

A responsive full-stack Gym Management System built with **Python, Flask, SQLite, HTML, CSS and JavaScript**. It includes an admin dashboard and CRUD workflows for members, trainers, membership plans and memberships.

## Features

- Dashboard cards for total members, active members, trainers and plans
- Member management: create, search, edit, delete and activate/deactivate
- Trainer directory with specialty and contact details
- Membership plan management with duration and price
- Assign memberships to active members and track dates/payment status
- SQLite database is created automatically on first run
- Sample data is seeded automatically for an immediate demo
- Responsive layout for desktop, tablet and mobile
- Flash messages, delete confirmations, basic form validation
- Parameterized SQL queries and foreign-key constraints

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript, Jinja templates |
| Development server | Flask |

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ironcore-gym-management.git
cd ironcore-gym-management
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
```

**Windows (Git Bash):**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser. The SQLite database is created automatically in the project root, along with example records.

## Project structure

```text
ironcore-gym-management/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── app/
    ├── __init__.py
    ├── db.py
    ├── routes.py
    ├── templates/
    │   ├── base.html
    │   ├── dashboard.html
    │   ├── members.html
    │   ├── member_form.html
    │   ├── trainers.html
    │   ├── plans.html
    │   ├── memberships.html
    │   └── 404.html
    └── static/
        ├── css/style.css
        └── js/app.js
```

## Routes

| Route | Purpose |
|---|---|
| `/` | Dashboard |
| `/members` | Search and manage members |
| `/members/<id>/edit` | Edit member profile |
| `/trainers` | Manage trainers |
| `/plans` | Manage membership plans |
| `/memberships` | Assign and track memberships |

## Database model

- `members`: member profile, contact details and status
- `trainers`: trainer profile and specialty
- `plans`: duration, price and description
- `memberships`: member/plan relationship, dates and payment status

Membership dates are calculated using a simple 30-day-per-month approximation. For a production billing system, use calendar-aware month arithmetic and define renewal, cancellation, and payment workflows explicitly.

## GitHub publishing

1. Create a new empty GitHub repository.
2. Extract this ZIP and open a terminal inside the extracted folder.
3. Run:

```bash
git init
git add .
git commit -m "Build IronCore gym management system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ironcore-gym-management.git
git push -u origin main
```

Replace `YOUR-USERNAME` and the repository URL with your own details.

## Production notes

This is a portfolio/demo application, not a finished production deployment. Before deploying publicly, configure a strong secret key, add authentication and role-based authorization, enable CSRF protection, validate all input server-side, add automated tests, and use a production WSGI server. Do not store real member data in a public demo.

## License

MIT — see `LICENSE`.
