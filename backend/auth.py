"""
Authentication module.
  - Password hashing / verification
  - JWT generation / decoding
  - require_auth route decorator
  - Email-verification token helpers
  - Password-reset token helpers
"""

import os
import secrets
import functools
import logging
from datetime import datetime, timedelta, timezone

import jwt
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


# ── Password ──────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return generate_password_hash(password, method='scrypt')


def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)


# ── JWT ───────────────────────────────────────────────────────────────────────

def _secret() -> str:
    key = os.getenv('SECRET_KEY', 'cloudproof-dev-secret-change-in-production')
    if key == 'cloudproof-dev-secret-change-in-production':
        logger.warning('SECRET_KEY is default — set it in .env before production.')
    return key


def generate_token(user_id: int, expires_hours: int = 24) -> str:
    payload = {
        'user_id': user_id,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=expires_hours),
    }
    return jwt.encode(payload, _secret(), algorithm='HS256')


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, _secret(), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(f):
    """
    Route decorator — extracts Bearer token, injects user_id kwarg.

    Usage:
        @app.route('/api/protected')
        @require_auth
        def route(user_id):
            ...
    """
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Authorization header missing or not Bearer.'}), 401
        payload = decode_token(auth[7:])
        if not payload:
            return jsonify({'error': 'Token is invalid or expired. Please sign in again.'}), 401
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'error': 'Token missing user_id.'}), 401
        return f(*args, user_id=user_id, **kwargs)
    return wrapped


# ── Email verification tokens ────────────────────────────────────────────────

def generate_verification_token(user_id: int) -> str:
    """
    Create a 32-byte random hex token, store it in email_verification_tokens,
    and return the token string.  Expires in 24 hours.
    """
    from database import execute_query
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=24)
    # Remove any previous unused tokens for this user
    execute_query(
        "DELETE FROM email_verification_tokens WHERE user_id = %s AND used = 0",
        (user_id,)
    )
    execute_query(
        "INSERT INTO email_verification_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
        (user_id, token, expires)
    )
    return token


def verify_email_token(token: str) -> int | None:
    """
    Validate the token. If valid, mark it used, mark the user's email as verified,
    and return the user_id. Returns None if invalid or expired.
    """
    from database import execute_query
    rows = execute_query(
        "SELECT id, user_id, expires_at, used FROM email_verification_tokens WHERE token = %s",
        (token,), fetch=True
    )
    if not rows:
        return None
    row = rows[0]
    if row['used']:
        return None
    exp = row['expires_at']
    if isinstance(exp, str):
        exp = datetime.fromisoformat(exp)
    if exp.replace(tzinfo=None) < datetime.utcnow():
        return None
    user_id = row['user_id']
    execute_query("UPDATE email_verification_tokens SET used = 1 WHERE id = %s", (row['id'],))
    execute_query("UPDATE users SET email_verified = 1 WHERE id = %s", (user_id,))
    return user_id


# ── Password reset tokens ────────────────────────────────────────────────────

def generate_reset_token(user_id: int) -> str:
    """
    Create a 32-byte random hex reset token, store it, and return it.
    Expires in 1 hour.
    """
    from database import execute_query
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=1)
    execute_query(
        "DELETE FROM password_reset_tokens WHERE user_id = %s AND used = 0",
        (user_id,)
    )
    execute_query(
        "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
        (user_id, token, expires)
    )
    return token


def verify_reset_token(token: str) -> int | None:
    """
    Validate reset token. Returns user_id if valid, else None.
    Does NOT consume the token — call consume_reset_token() after the password is set.
    """
    from database import execute_query
    rows = execute_query(
        "SELECT id, user_id, expires_at, used FROM password_reset_tokens WHERE token = %s",
        (token,), fetch=True
    )
    if not rows:
        return None
    row = rows[0]
    if row['used']:
        return None
    exp = row['expires_at']
    if isinstance(exp, str):
        exp = datetime.fromisoformat(exp)
    if exp.replace(tzinfo=None) < datetime.utcnow():
        return None
    return row['user_id']


def consume_reset_token(token: str) -> None:
    from database import execute_query
    execute_query("UPDATE password_reset_tokens SET used = 1 WHERE token = %s", (token,))
