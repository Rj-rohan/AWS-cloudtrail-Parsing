# CloudProof

## Project Overview
CloudProof is an AWS hands-on activity tracker. It ingests CloudTrail logs (local files or S3), scores each AWS action by impact tier, and visualises the results as a GitHub-style contribution heatmap per user.

## Tech Stack
- Backend: Python 3.11+, Flask 3, psycopg2, boto3, python-dotenv, schedule
- Frontend: React 18, react-calendar-heatmap, react-router-dom, axios
- Database: SQLite (default, zero-config) or PostgreSQL (set `DB_ENGINE=postgres`)
- Infrastructure: IAM role + trust policy JSON in `infrastructure/`

## Key Directories

| Path | Purpose |
|---|---|
| `backend/` | Flask REST API, ingestion pipeline, scoring engine |
| `backend/sample_logs/` | Local CloudTrail JSON fixtures for dev/testing |
| `frontend/src/` | React SPA – heatmap, dashboard, visual, resources views |
| `infrastructure/` | IAM policy and trust policy for AWS role assumption |

### Backend files
- `app.py` – Flask routes (users CRUD, activity, dashboard, resources, log triggers)
- `database.py` – dual-engine DB abstraction (SQLite / PostgreSQL), `execute_query()`
- `ingestion.py` – CloudTrail log parsing from local files or S3, applies scoring caps
- `scoring.py` – `SCORING_RULES` dict + `calculate_score(service, action)`
- `scheduler.py` – periodic ingestion job via `schedule`
- `schema.sql` – PostgreSQL DDL (SQLite schema lives inline in `database.py:SQLITE_SCHEMA`)

### Frontend files
- `src/App.js` – root component, heatmap view, streak calculation
- `src/Dashboard.js` – daily breakdown view
- `src/Visual.js` – chart/visual view
- `src/Resources.js` – AWS resource state view

## Essential Commands

### Backend
```cmd
cd backend
pip install -r requirements.txt
python app.py          # starts on http://localhost:5000
```

### Frontend
```cmd
cd frontend
npm install
npm start              # starts on http://localhost:3000
npm run build
```

### Database setup (PostgreSQL only)
```cmd
createdb -U postgres cloudproof
psql -U postgres -d cloudproof -f backend\schema.sql
```
SQLite requires no setup — `cloudproof.db` is created automatically on first run.

### Sample data
```cmd
cd backend
python generate_sample_data.py
# or trigger via API:
curl -X POST http://localhost:5000/api/process-sample-logs
```

### Health check
```cmd
curl http://localhost:5000/api/health
```

## Environment Variables (`backend/.env`)
See `backend/.env.example`. Key vars:
- `DB_ENGINE` – `sqlite` (default) or `postgres`
- `DB_HOST / DB_PORT / DB_NAME / DB_USER / DB_PASSWORD` – PostgreSQL connection
- `LOCAL_CLOUDTRAIL_USER_ID` – user id used when ingesting local/S3 logs (default `1`)
- `PROCESS_LOCAL_CLOUDTRAIL_LOGS_ON_START` – set to `true` to auto-ingest on startup

## Additional Documentation
- `.claude/docs/architectural_patterns.md` – API design, DB abstraction, scoring system, ingestion pipeline patterns
