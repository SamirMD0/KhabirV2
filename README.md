# Khabir V2

AI-powered accident analysis platform.
Flask API (Python) + React frontend (Vite + Tailwind).

## Project Structure

| Folder | What it is |
|--------|-----------|
| `backend/` | Flask REST API - auth, cases, analysis, admin |
| `frontend/` | React + Vite SPA |
| `claude/` | Architecture plan and prompt history |

## Quick Start

### 1. Clone and set up environment

    git clone <repo>
    cd khabir-v2

    # Backend
    python -m venv venv
    source venv/bin/activate        # Windows: venv\Scripts\activate
    pip install -r requirements-dev.txt
    cp .env.example .env            # fill in SECRET_KEY, JWT_SECRET_KEY, GEMINI_API_KEY

    # Frontend
    cd frontend && npm install && cd ..

### 2. Generate secret keys

    python -c "import secrets; print(secrets.token_hex(32))"
    # Run twice - once for SECRET_KEY, once for JWT_SECRET_KEY

### 3. Get a free Gemini API key

    https://aistudio.google.com/app/apikey
    # Add to .env as GEMINI_API_KEY=...

### 4. Initialize the database

    flask --app backend.app db init
    flask --app backend.app db migrate -m "initial"
    flask --app backend.app db upgrade

### 5. Run both servers

    # Terminal 1 - Flask API on port 5000
    flask --app backend.app run --debug

    # Terminal 2 - React dev server on port 5173
    cd frontend && npm run dev

    # Or both at once:
    make dev

Visit: http://localhost:5173

## Deployment

| Service | What it hosts |
|---------|---------------|
| Railway | Flask API + PostgreSQL (free tier) |
| Vercel | React frontend (free tier) |

Set `VITE_API_URL=https://your-railway-app.up.railway.app` in Vercel env vars.
Set `CORS_ORIGINS=https://your-vercel-app.vercel.app` in Railway env vars.

## Run Tests

    pytest backend/tests/ -v

## Stack

Backend: Flask 3, SQLAlchemy 2, Flask-Migrate, PyJWT, Marshmallow, Flask-Limiter
Frontend: React 18, Vite 5, Tailwind CSS 3, React Router 6, Axios
AI: Google Gemini 1.5 Flash (free tier)
DB: SQLite (dev) / PostgreSQL (prod)
