# 🚗 KHABIR V2 — Complete Rebuild Plan

> **Goal**: Production-ready, portfolio-grade accident analysis platform.  
> **AI**: Google Gemini 1.5 Flash (free tier, multimodal — replaces Ollama + Roboflow).  
> **Principle**: Clean architecture, zero bloat, deployable in one command.

---

## Table of Contents

1. [Why Rebuild?](#1-why-rebuild)
2. [Tech Stack Decisions](#2-tech-stack-decisions)
3. [Folder Structure](#3-folder-structure)
4. [System Design](#4-system-design)
5. [Database Design](#5-database-design)
6. [API Design](#6-api-design)
7. [Authentication — JWT Flow](#7-authentication--jwt-flow)
8. [AI Integration — Gemini 1.5 Flash](#8-ai-integration--gemini-15-flash)
9. [Frontend Plan](#9-frontend-plan)
10. [Build Order (Phases)](#10-build-order-phases)
11. [Free Deployment Plan](#11-free-deployment-plan)
12. [Environment Variables](#12-environment-variables)
13. [What to Drop from V1](#13-what-to-drop-from-v1)

---

## 1. Why Rebuild?

| Problem in V1 | Fix in V2 |
|---|---|
| Auth in localStorage (critical vuln) | JWT in HttpOnly cookies |
| Routes + business logic mixed together | Service layer pattern |
| Ollama (local only, heavy) | Gemini 1.5 Flash API (free, cloud) |
| Roboflow (paid after limit) | Gemini Vision handles damage detection |
| No request validation | Marshmallow schemas on every endpoint |
| No tests | Pytest suite with fixtures |
| No Docker | Dockerfile + docker-compose |
| Flat utils/ folder | Proper services/, schemas/, repositories/ |
| Empty requirements.txt | Pinned deps, split dev/prod |
| No rate limiting | Flask-Limiter on auth + upload endpoints |

---

## 2. Tech Stack Decisions

### Backend
| Layer | Choice | Why |
|---|---|---|
| Framework | **Flask 3** | Lightweight, you know it, portfolio-friendly |
| ORM | **SQLAlchemy 2 + Flask-Migrate** | Keep from v1, works well |
| Auth | **PyJWT** (JWT) | Stateless, works with mobile + web |
| Validation | **Marshmallow** | Schema-based, clean error messages |
| Rate limiting | **Flask-Limiter** | Free, prevents abuse |
| Image processing | **Pillow + OpenCV** | Keep from v1 |
| Vector search | **FAISS** | Keep from v1 (free, fast) |
| Embeddings | **Sentence Transformers** | Keep (runs locally, small model) |

### AI (100% Free)
| Feature | Tool | Free Tier |
|---|---|---|
| Image analysis + damage detection | **Google Gemini 1.5 Flash** | 15 RPM, 1M tokens/day |
| Accident reasoning / chat | **Google Gemini 1.5 Flash** | Same quota |
| Text embeddings | `all-MiniLM-L6-v2` (local) | Free, runs in RAM |

> **Why Gemini 1.5 Flash over Ollama?**  
> Ollama requires 8GB+ RAM and can't run on free hosting.  
> Gemini 1.5 Flash is multimodal — it can look at the accident image directly AND reason about it. One model replaces both Ollama and Roboflow. Free tier is generous enough for a portfolio project.

### Database
| Env | Database |
|---|---|
| Development | SQLite (zero setup) |
| Production | PostgreSQL (free on Railway/Neon) |

### Frontend
| Choice | Details |
|---|---|
| **Jinja2 + Alpine.js + HTMX** | No build step, fast, modern feel |
| Tailwind CSS (CDN) | Utility classes, no npm required |
| No React/Vue | Reduces complexity; HTMX covers 90% of interactivity needs |

### Deployment (Free)
| Service | What it hosts |
|---|---|
| **Railway** (free tier) | Flask app + PostgreSQL |
| **Cloudflare R2** (free 10GB) | Uploaded images + annotated results |

---

## 3. Folder Structure

```
khabir-v2/
│
├── backend/
│   ├── api/                        # Route handlers only (thin controllers)
│   │   ├── __init__.py
│   │   ├── auth.py                 # /api/auth/*
│   │   ├── cases.py                # /api/cases/*
│   │   ├── admin.py                # /api/admin/*
│   │   └── health.py               # /api/health
│   │
│   ├── core/                       # App wiring, no business logic
│   │   ├── __init__.py
│   │   ├── config.py               # All settings (dev/prod/test)
│   │   ├── extensions.py           # db, migrate, limiter, cors instances
│   │   └── exceptions.py           # Custom exception classes + handlers
│   │
│   ├── models/                     # SQLAlchemy models only
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── case.py
│   │
│   ├── schemas/                    # Marshmallow schemas (validation + serialization)
│   │   ├── __init__.py
│   │   ├── auth_schemas.py
│   │   └── case_schemas.py
│   │
│   ├── services/                   # All business logic lives here
│   │   ├── __init__.py
│   │   ├── auth_service.py         # signup, login, token refresh
│   │   ├── case_service.py         # create, get, delete cases
│   │   ├── analysis_service.py     # orchestrates the full analysis pipeline
│   │   ├── gemini_service.py       # all Gemini API calls
│   │   ├── vision_service.py       # image preprocessing (OpenCV/Pillow)
│   │   └── similarity_service.py   # FAISS index + search
│   │
│   ├── repositories/               # Database queries (no logic, just queries)
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   └── case_repo.py
│   │
│   ├── utils/                      # Stateless helpers
│   │   ├── __init__.py
│   │   ├── jwt_utils.py            # encode/decode tokens
│   │   ├── file_utils.py           # save/delete files, hash
│   │   └── decorators.py           # @login_required, @admin_required
│   │
│   ├── templates/                  # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── result.html
│   │   ├── dashboard.html
│   │   └── partials/               # HTMX partial templates
│   │       ├── case_row.html
│   │       └── chat_message.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── app.css
│   │   ├── js/
│   │   │   └── app.js
│   │   └── icons/
│   │
│   ├── migrations/                 # Alembic (keep from v1)
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_cases.py
│   │   └── test_analysis.py
│   │
│   ├── data/
│   │   └── accident_summaries.csv  # Historical cases seed data
│   │
│   └── app.py                      # Application factory
│
├── .env.example
├── .env                            # git-ignored
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt                # Production deps
├── requirements-dev.txt            # Dev-only deps (pytest, etc.)
├── Makefile                        # make run, make test, make migrate
└── README.md
```

---

## 4. System Design

### The Analysis Pipeline (V2)

```
User uploads image + form data
        │
        ▼
[1] FileUtils: validate extension, compute MD5 hash, save to /static/uploads/
        │
        ▼
[2] CaseService: create AccidentCase row (status=uploaded)
        │
        ▼
[3] VisionService: resize + preprocess image with OpenCV
        │
        ▼
[4] GeminiService.analyze_image(image_bytes, user_context)
    ├── Prompt: "Analyze this accident image. Identify vehicles, damage type,
    │           damage location, severity. Return structured JSON."
    └── Returns: { vehicles: [...], damage: {...}, severity: "...", confidence: 0.9 }
        │
        ▼
[5] GeminiService.generate_analysis(structured_data, user_context)
    ├── Prompt: "Based on detected data + user role/observations, determine
    │           likely cause, fault, and recommended actions."
    └── Returns: narrative analysis string
        │
        ▼
[6] SentenceTransformer: embed the narrative → 384-dim float32 vector
        │
        ▼
[7] SimilarityService: search FAISS index → top 3 similar historical cases
        │
        ▼
[8] CaseService: update case row (status=analyzed, all fields populated)
        │
        ▼
[9] Return JSON to frontend
```

### Auth Flow (JWT)

```
POST /api/auth/login
        │
        ▼
[1] Validate credentials → issue access_token (15min) + refresh_token (7d)
[2] access_token → JSON response body (stored in memory/Alpine state)
[3] refresh_token → HttpOnly cookie (cannot be read by JS)
        │
Protected request:
        ▼
Authorization: Bearer <access_token>
        │
[4] @login_required decorator decodes token
[5] Injects current_user into route
        │
Token expired:
        ▼
POST /api/auth/refresh  (refresh_token sent automatically via cookie)
→ New access_token issued
```

### Separation of Concerns

```
api/cases.py          ← HTTP only: parse request, call service, return response
    │
    ▼
services/case_service.py   ← Business logic: validate, orchestrate, handle errors
    │
    ▼
repositories/case_repo.py  ← DB only: SQLAlchemy queries, no logic
    │
    ▼
models/case.py             ← Schema definition only
```

---

## 5. Database Design

### User Model
```python
class User(db.Model):
    id           = Integer, PK
    username     = String(80), unique, not null
    email        = String(120), unique, not null       # new in v2
    password_hash = String(256), not null
    is_admin     = Boolean, default=False
    is_active    = Boolean, default=True               # new: soft disable
    created_at   = DateTime, default=utcnow
    cases        → relationship to AccidentCase
```

### AccidentCase Model
```python
class AccidentCase(db.Model):
    id                  = Integer, PK
    user_id             = Integer, FK(user.id)
    
    # File info
    image_path          = String(255)
    image_hash          = String(64), indexed          # duplicate detection
    annotated_image     = String(255)
    video_path          = String(255)
    
    # Status
    status              = Enum('uploaded','analyzing','analyzed','failed')
    
    # User-provided context
    user_role           = String(50)                   # witness/driver/expert
    vehicle_type        = String(50)
    vehicle_color       = String(50)
    damage_location     = String(100)
    damage_details      = Text
    witness_observation = Text
    expert_notes        = Text
    number_of_vehicles  = String(20)
    saw_collision       = Boolean
    
    # AI outputs
    gemini_raw_json     = JSON                         # raw structured output
    analysis_result     = Text                         # narrative
    cross_analysis_result = Text
    detection_summary   = Text
    
    # Similarity
    embedding           = BLOB
    
    # Timestamps
    created_at          = DateTime, default=utcnow
    analyzed_at         = DateTime
```

---

## 6. API Design

All endpoints under `/api/` prefix. All responses are JSON.

### Auth
```
POST   /api/auth/signup        → { user_id, username }
POST   /api/auth/login         → { access_token, user_id, username, is_admin }
POST   /api/auth/logout        → { success }
POST   /api/auth/refresh       → { access_token }
GET    /api/auth/me            → { user_id, username, is_admin }
```

### Cases
```
POST   /api/cases/upload       → { case_id, status }           @login_required
POST   /api/cases/:id/analyze  → { analysis, vehicles, ... }   @login_required
GET    /api/cases/:id          → { case object }               @login_required
GET    /api/cases/:id/similar  → [ { case_id, score } ]        @login_required
DELETE /api/cases/:id          → { success }                   @login_required
```

### Chat
```
POST   /api/cases/:id/chat     → { reply }                     @login_required
```

### Admin
```
GET    /api/admin/cases        → [ all cases ]                 @admin_required
GET    /api/admin/stats        → { total, analyzed, pending }  @admin_required
DELETE /api/admin/cases/:id    → { success }                   @admin_required
DELETE /api/admin/cases        → { deleted_count }             @admin_required
```

### Health
```
GET    /api/health             → { status: "ok", version: "2.0" }
```

---

## 7. Authentication — JWT Flow

### `utils/jwt_utils.py`
```python
# Two tokens:
# access_token  — short-lived (15 min), sent in response body
# refresh_token — long-lived (7 days), sent in HttpOnly cookie

def create_access_token(user_id: int) -> str
def create_refresh_token(user_id: int) -> str
def decode_token(token: str) -> dict
```

### `utils/decorators.py`
```python
@login_required   # reads Bearer token from Authorization header
@admin_required   # login_required + checks user.is_admin from DB
```

### Why JWT over Sessions (v1)
- Sessions require sticky sessions if you scale (multiple servers)
- JWT is stateless — works with mobile apps too
- refresh_token in HttpOnly cookie = safe from XSS

---

## 8. AI Integration — Gemini 1.5 Flash

### Why Gemini replaces both Ollama + Roboflow

| V1 Tool | Problem | V2 Replacement |
|---|---|---|
| Ollama/Llama3 | Local only, 8GB RAM, can't deploy free | Gemini 1.5 Flash API |
| Roboflow | Paid after 1000 calls/month | Gemini Vision (image analysis) |
| Sentence Transformers | Keep (runs in 512MB RAM) | Sentence Transformers (no change) |

### Free Tier Limits (Gemini 1.5 Flash)
- 15 requests/minute
- 1,000,000 tokens/day
- Completely free, no credit card

### `services/gemini_service.py` — Key Methods

```python
class GeminiService:

    def analyze_accident_image(self, image_bytes: bytes, user_context: dict) -> dict:
        """
        Send image to Gemini Vision.
        Returns structured JSON:
        {
          "vehicles": [
            { "type": "car", "color": "white", "damage": "front-end", "severity": "high" }
          ],
          "estimated_cause": "...",
          "road_conditions": "...",
          "number_of_vehicles": 2
        }
        """
        prompt = """
        Analyze this accident image carefully. Return ONLY valid JSON (no markdown):
        {
          "vehicles": [{"type": str, "color": str, "damage_location": str, 
                        "damage_severity": "none|minor|moderate|severe", 
                        "is_damaged": bool}],
          "scene": {"road_type": str, "weather_condition": str, "lighting": str},
          "estimated_vehicle_count": int,
          "visible_damage_summary": str
        }
        """

    def generate_analysis_narrative(self, image_data: dict, user_context: dict) -> str:
        """Generate human-readable accident analysis using Gemini text."""

    def chat_about_case(self, case_context: dict, user_message: str) -> str:
        """Single-turn Q&A about a specific case."""
```

### Gemini API Setup (Free)
```bash
# 1. Go to: https://aistudio.google.com/app/apikey
# 2. Create API key (no billing required)
# 3. Add to .env:
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-1.5-flash
```

```python
# Install
pip install google-generativeai
```

---

## 9. Frontend Plan

### Philosophy
- **No npm/build step** — Tailwind CDN + Alpine.js + HTMX
- **HTMX** handles dynamic updates without writing fetch() calls
- **Alpine.js** handles local state (modals, form steps)
- Clean, dark, professional look

### Key Pages
```
/               → Landing + upload form (chat-style multi-step)
/result/<id>    → Analysis result, similar cases, chat
/dashboard      → Admin dashboard (HTMX table, live stats)
/login          → Login page (not modal — dedicated page)
```

### HTMX Usage Examples
```html
<!-- Submit upload form, swap result section -->
<form hx-post="/api/cases/upload"
      hx-target="#result-panel"
      hx-swap="innerHTML"
      hx-indicator="#spinner">

<!-- Chat: append new messages -->
<form hx-post="/api/cases/{{ id }}/chat"
      hx-target="#chat-box"
      hx-swap="beforeend">

<!-- Admin: delete row inline -->
<button hx-delete="/api/admin/cases/{{ id }}"
        hx-target="#row-{{ id }}"
        hx-swap="outerHTML swap:0.3s">
```

---

## 10. Build Order (Phases)

### Phase 1 — Core Backend (Week 1)
```
□ Setup project structure + venv
□ core/config.py (dev/prod/test configs)
□ core/extensions.py (db, migrate, cors, limiter)
□ models/user.py + models/case.py
□ Flask-Migrate initial migration
□ schemas/auth_schemas.py (Marshmallow)
□ repositories/user_repo.py
□ services/auth_service.py (signup, login, hash password)
□ utils/jwt_utils.py (create + decode tokens)
□ utils/decorators.py (@login_required, @admin_required)
□ api/auth.py (POST /signup, /login, /logout, /me, /refresh)
□ api/health.py
□ Test auth endpoints with curl/Postman
```

### Phase 2 — Upload + Gemini Analysis (Week 2)
```
□ utils/file_utils.py (save, hash, validate extension)
□ services/gemini_service.py (analyze_accident_image)
□ services/vision_service.py (preprocess with OpenCV)
□ services/analysis_service.py (orchestrate the pipeline)
□ repositories/case_repo.py
□ services/case_service.py
□ schemas/case_schemas.py
□ api/cases.py (POST /upload, POST /:id/analyze, GET /:id)
□ Test: upload image → get Gemini analysis back
```

### Phase 3 — Similarity + Chat (Week 3)
```
□ services/similarity_service.py (build FAISS index, search)
□ Seed historical cases from CSV
□ GET /api/cases/:id/similar
□ services/gemini_service.py → chat_about_case()
□ POST /api/cases/:id/chat
□ api/admin.py (all admin endpoints)
```

### Phase 4 — Frontend (Week 4)
```
□ templates/base.html (navbar, footer, Alpine + HTMX + Tailwind)
□ templates/index.html (landing + upload flow)
□ templates/result.html (analysis display + chat)
□ templates/dashboard.html (HTMX admin table)
□ static/css/app.css (custom styles on top of Tailwind)
□ static/js/app.js (minimal JS, Alpine handles the rest)
□ Connect frontend to all API endpoints
```

### Phase 5 — Production Hardening (Week 5)
```
□ Write tests (conftest.py, test_auth.py, test_cases.py)
□ Add Flask-Limiter rules (10/min on /login, 5/min on /upload)
□ Dockerfile + docker-compose.yml
□ Environment separation (dev SQLite → prod PostgreSQL)
□ Makefile (make run, make test, make migrate, make seed)
□ README with setup instructions + screenshots
□ Deploy to Railway
```

---

## 11. Free Deployment Plan

### Option A: Railway (Recommended)
```
Free tier: 5$/month credit (covers small Flask app + PostgreSQL)
Steps:
1. Push to GitHub
2. Connect Railway to repo
3. Add environment variables in Railway dashboard
4. PostgreSQL plugin: one click, connection string auto-injected
5. Auto-deploys on git push
```

### Option B: Render
```
Free tier: 750 hours/month (web service sleeps after 15min inactivity)
Good for: Portfolio demos (acceptable cold start for reviewers)
Steps: same as Railway, slightly slower
```

### File Storage (Images)
```
Option A: Store in /static/ (simplest, works on Railway with persistent disk)
Option B: Cloudflare R2 (free 10GB, S3-compatible) — recommended for prod
```

---

## 12. Environment Variables

```bash
# .env.example

# App
FLASK_ENV=development
SECRET_KEY=generate-with: python -c "import secrets; print(secrets.token_hex(32))"

# Database
DATABASE_URL=sqlite:///khabir.db          # dev
# DATABASE_URL=postgresql://...           # prod (Railway injects this automatically)

# AI
GEMINI_API_KEY=your_key_from_aistudio
GEMINI_MODEL=gemini-1.5-flash

# JWT
JWT_SECRET_KEY=another-random-32-hex-key
JWT_ACCESS_TOKEN_EXPIRES=900             # 15 minutes in seconds
JWT_REFRESH_TOKEN_EXPIRES=604800         # 7 days in seconds

# File Upload
UPLOAD_FOLDER=backend/static/uploads
MAX_CONTENT_LENGTH=16777216              # 16MB

# Rate Limiting
RATELIMIT_DEFAULT=200/day;50/hour
```

---

## 13. What to Drop from V1

| V1 Feature | V2 Decision | Reason |
|---|---|---|
| Ollama/Llama3 (local) | ❌ Drop → Gemini API | Can't run on free hosting |
| Roboflow API | ❌ Drop → Gemini Vision | Paid after limit |
| LiveReload server | ❌ Drop | Use `flask run --debug` |
| Flask-Login | ❌ Drop → PyJWT | Sessions don't scale |
| Server-side sessions | ❌ Drop → JWT | Stateless is better |
| `localStorage` auth | ❌ Already fixed in v1.1 | JWT removes this entirely |
| `generate_simulation_video.py` | ⚠️ Optional phase 6 | Nice-to-have |
| FAISS external files | ✅ Keep | Works well |
| Sentence Transformers | ✅ Keep | Free, small footprint |
| Flask-Migrate / Alembic | ✅ Keep | Works well |
| OpenCV preprocessing | ✅ Keep | Still needed |

---

## Quick Start Template

```bash
# 1. Create project
mkdir khabir-v2 && cd khabir-v2
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install core deps first
pip install flask flask-sqlalchemy flask-migrate flask-cors flask-limiter \
            marshmallow pyjwt python-dotenv google-generativeai \
            sentence-transformers faiss-cpu opencv-python pillow numpy

# 3. Set up .env
cp .env.example .env
# → Add your GEMINI_API_KEY from https://aistudio.google.com/app/apikey

# 4. Init DB
flask db init && flask db migrate -m "initial" && flask db upgrade

# 5. Run
flask run --debug
```

---

## Makefile

```makefile
run:
	flask run --debug

test:
	pytest backend/tests/ -v

migrate:
	flask db migrate -m "$(msg)"

upgrade:
	flask db upgrade

seed:
	python backend/services/similarity_service.py --seed

docker:
	docker-compose up --build

lint:
	flake8 backend/ --max-line-length 100
```

---

*Khabir V2 — Built clean. Deployed free. Portfolio-ready.*