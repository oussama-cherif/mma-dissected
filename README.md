# MMA Dissected

A full-stack web application for UFC fight analysis and predictions. Displays upcoming UFC event cards with fight predictions, deep fighter statistics, vulnerability detection, and betting analytics.

Supports **English**, **French**, and **Arabic** (with full RTL layout).

## Features

- **UFC Event Cards**: Full card display — Main Card, Prelims, Early Prelims
- **Fight Predictions**: Winner prediction with confidence percentage and method probabilities (KO/TKO, Submission, Decision)
- **Vulnerability Detection**: Cross-references how fighters win against how opponents have lost — flags stylistic mismatches and potential upsets
- **Fighter Stats**: Sig. strikes/min, strike accuracy, takedown averages, defense rates, submission attempts
- **Betting Insights**: Value bet detection based on method probability analysis
- **Auto-Sync**: Daily automatic card data updates via SportRadar API
- **Multilingual**: EN / FR / AR with RTL support for Arabic

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 + Django REST Framework |
| Frontend | Vue 3 + Vite + Pinia + Vue Router |
| Styling | Tailwind CSS (dark theme) |
| i18n | vue-i18n v9 |
| Charts | Chart.js via vue-chartjs |
| Predictions | Anthropic API |
| Live Data | SportRadar MMA API |
| Scheduler | APScheduler |
| Database | SQLite (dev) / PostgreSQL (prod) |

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose (optional)

### Option 1: Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/your-username/mma-dissected.git
cd mma-dissected

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Start all services
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
python manage.py createsuperuser
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `ANTHROPIC_API_KEY` | Anthropic API key for predictions |
| `SPORTRADAR_API_KEY` | SportRadar MMA API key |
| `VITE_API_BASE_URL` | Backend API URL (default: http://localhost:8000/api) |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/events/` | All events |
| GET | `/api/events/:id/` | Event detail with fights |
| GET | `/api/events/next/` | Next upcoming event |
| GET | `/api/fighters/` | All fighters |
| GET | `/api/fighters/:id/` | Fighter profile |
| GET | `/api/predictions/fights/:id/prediction/` | Get fight prediction |
| POST | `/api/predictions/fights/:id/predict/` | Generate prediction |
| POST | `/api/sync/card/` | Trigger manual data sync |
| GET | `/api/health/` | Health check |

## Project Structure

```
mma-dissected/
├── backend/
│   ├── config/          # Django settings, URLs, WSGI
│   ├── fighters/        # Fighter model, API views
│   ├── events/          # Event + Fight models, API views
│   ├── predictions/     # Prediction model, prediction engine
│   ├── scraper/         # SportRadar client, scheduler
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/  # Vue components
│       ├── views/       # Page views
│       ├── stores/      # Pinia state management
│       ├── locales/     # i18n translation files
│       └── router/      # Vue Router config
├── docker-compose.yml
└── .env.example
```

## License

MIT
