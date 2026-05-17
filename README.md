# Khabir V2

AI-powered accident analysis web app scaffold built with Flask, SQLAlchemy, JWT auth, Marshmallow, and Gemini.

## First Run

1. Create virtual environment

   ```bash
   python -m venv venv
   ```

   Windows:

   ```bat
   venv\Scripts\activate
   ```

   Mac/Linux:

   ```bash
   source venv/bin/activate
   ```

2. Install dependencies

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Copy `.env.example` to `.env` and fill in secrets

   Windows:

   ```bat
   copy .env.example .env
   set FLASK_APP=backend.app
   ```

   Mac/Linux:

   ```bash
   cp .env.example .env
   export FLASK_APP=backend.app
   ```

   Fill in `SECRET_KEY`, `JWT_SECRET_KEY`, and `GEMINI_API_KEY`.

4. Initialize the database

   ```bash
   flask --app backend.app db init
   flask --app backend.app db migrate -m "initial"
   flask --app backend.app db upgrade
   ```

5. Run the development server

   ```bash
   flask --app backend.app run --debug
   ```

6. Run tests

   ```bash
   pytest backend/tests/ -v
   ```

7. Run with Docker (optional)

   ```bash
   docker-compose up --build
   ```

