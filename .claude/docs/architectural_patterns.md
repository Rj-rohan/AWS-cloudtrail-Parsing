# Architectural Patterns

## 1. Dual-Engine Database Abstraction
`database.py` exposes a single `execute_query(query, params, fetch)` function that transparently handles both SQLite and PostgreSQL. The engine is selected at runtime via `DB_ENGINE` env var. All callers (`app.py`, `ingestion.py`, `scoring_auto.py`) use `%s` placeholders; the abstraction converts them to `?` for SQLite internally (`_convert_sqlite_placeholders`). SQLite schema is defined inline as `SQLITE_SCHEMA`; PostgreSQL schema lives in `schema.sql`.

## 2. REST API Pattern (Flask)
`app.py` follows a consistent route handler pattern:
1. Validate input / check resource existence with a `SELECT` query.
2. Return `404` if not found, `400` for bad input, `409` for conflicts.
3. Execute the mutation.
4. Return a JSON response with an appropriate 2xx status.
All errors are caught, logged via `logger.error`, and returned as `{'error': '...'}` JSON.

## 3. Tiered Scoring System
`scoring.py` defines `SCORING_RULES` — a nested dict keyed by service then action name — with integer scores 0–10 representing impact tiers. `calculate_score(service, action)` is the single entry point used by all ingestion paths. Read-only actions are filtered via `IGNORED_ACTIONS` prefix matching. Three caps are enforced per day: `DAILY_SCORE_CAP=100`, `SERVICE_DAILY_CAP=30`, `ACTION_DAILY_CAP=15`.

## 4. Ingestion Pipeline Pattern
Both `process_local_cloudtrail_logs()` and `process_s3_cloudtrail_logs()` in `ingestion.py` share identical logic:
1. Iterate log files (local dir or S3 paginator).
2. Parse each CloudTrail `Records[]` array.
3. Skip `readOnly` events.
4. Call `calculate_score(service, action)`.
5. Enforce the three daily caps using in-memory dicts (`daily_totals`, `daily_service_scores`, `daily_action_scores`).
6. Batch-collect `activities` list, then call `store_activities()`.
7. Update `processing_state` table to avoid reprocessing.

## 5. Frontend View-Switching Pattern
`App.js` manages a `view` state string (`'heatmap' | 'dashboard' | 'visual' | 'resources'`). Each view renders a separate component (`Dashboard`, `Visual`, `Resources`) or inline JSX. Data is fetched once per user load and passed down as props (`userId`).

## 6. AWS Role Assumption
`ingestion.py:assume_role()` uses STS to obtain temporary credentials before accessing S3. The `role_arn` is stored per-user in the `users` table and passed through the ingestion call chain.
