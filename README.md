# MMA Dissected

A full-stack web application for UFC fight analysis and predictions. Displays upcoming UFC event cards with fight predictions, deep fighter statistics, vulnerability detection, and betting analytics.

Supports **English**, **French**, and **Arabic** (with full RTL layout).

## Live Demo

- **Frontend**: [frontend-ten-iota-12.vercel.app](https://frontend-ten-iota-12.vercel.app)
- **API**: [backend-production-5dd7.up.railway.app/api/events/](https://backend-production-5dd7.up.railway.app/api/events/)

## Features

- **UFC Event Cards**: Full card display — Main Card, Prelims, Early Prelims
- **Fight Predictions**: Winner prediction with confidence percentage and method probabilities (KO/TKO, Submission, Decision)
- **Vulnerability Detection**: Cross-references how fighters win against how opponents have lost — flags stylistic mismatches and potential upsets
- **Fighter Stats**: Sig. strikes/min, strike accuracy, takedown averages, defense rates, submission attempts
- **Betting Insights**: Value bet detection based on method probability analysis
- **Auto-Sync**: Daily automatic card data updates via ufcstats.com scraper
- **Multilingual**: EN / FR / AR with RTL support for Arabic
- **CI/CD**: GitHub Actions pipeline with backend tests and frontend build checks

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 + Django REST Framework |
| Frontend | Vue 3 + Vite + Pinia + Vue Router |
| Styling | Tailwind CSS (dark theme) |
| i18n | vue-i18n v9 |
| Charts | Chart.js via vue-chartjs |
| Predictions | Stats-based engine with vulnerability cross-referencing |
| Live Data | ufcstats.com scraper (BeautifulSoup4 + lxml) |
| Scheduler | APScheduler |
| Database | SQLite (dev) / PostgreSQL (prod) |

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose (optional, for containerized setup)

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/oussama-cherif/mma-dissected.git
cd mma-dissected

# Copy environment variables
cp .env.example .env

# Start all services (backend + PostgreSQL + frontend)
# Migrations and seed data run automatically on first start
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- Admin: http://localhost:8000/admin

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py sync_events  # fetch real UFC data from ufcstats.com
python manage.py createsuperuser  # optional, for admin panel
python manage.py runserver
```

**Frontend (separate terminal):**
```bash
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/health/

### Environment Variables

Copy `.env.example` to `.env`:

| Variable | Required | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | Yes | Django secret key (any random string for dev) |
| `ANTHROPIC_API_KEY` | No | Anthropic Claude API key (for AI-powered predictions) |
| `SPORTRADAR_API_KEY` | No | Not used — data comes from ufcstats.com scraper |
| `VITE_API_BASE_URL` | No | Backend API URL (default: http://localhost:8000/api) |
| `DATABASE_URL` | No | PostgreSQL connection string (uses SQLite if empty) |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/events/` | All events, newest first |
| GET | `/api/events/:id/` | Event detail with all fights and predictions |
| GET | `/api/events/next/` | Next upcoming event |
| GET | `/api/fights/:id/` | Fight detail with full fighter stats |
| GET | `/api/fighters/` | All fighters |
| GET | `/api/fighters/:id/` | Fighter profile with full stats |
| GET | `/api/predictions/fights/:id/prediction/` | Get prediction for a fight |
| POST | `/api/predictions/fights/:id/predict/` | Generate/regenerate prediction |
| POST | `/api/sync/card/` | Trigger manual data sync from ufcstats.com |
| GET | `/api/health/` | Health check |

## Project Structure

```
mma-dissected/
├── backend/
│   ├── config/          # Django settings, URLs, WSGI
│   ├── fighters/        # Fighter model, serializers, API views
│   ├── events/          # Event + Fight models, serializers, API views
│   ├── predictions/     # Prediction model, stats-based prediction engine
│   ├── scraper/         # ufcstats.com scraper, APScheduler tasks
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/  # FightCard, FighterStats, PredictionPanel, etc.
│       ├── views/       # Home, Events, Event detail, Fight detail
│       ├── stores/      # Pinia stores (events, predictions)
│       ├── locales/     # i18n files (en.json, fr.json, ar.json)
│       └── router/      # Vue Router config
├── docker-compose.yml   # Docker setup (backend + PostgreSQL + frontend)
└── .env.example         # Environment variable template
```

## Deployment

| Service | Platform |
|---|---|
| Frontend | [Vercel](https://vercel.com) |
| Backend | [Railway](https://railway.com) |
| Database | PostgreSQL (Railway) |

**Redeploy:**
```bash
# Frontend
cd frontend && vercel --prod

# Backend (from repo root)
railway up --detach
```

## License

MIT
