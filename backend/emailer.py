"""
Email delivery via SMTP.
Set SMTP_HOST/SMTP_USER/SMTP_PASS in .env for production.
In dev (no SMTP config), emails are logged to console only.
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger      = logging.getLogger(__name__)
SMTP_HOST   = os.getenv('SMTP_HOST', '')
SMTP_PORT   = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER   = os.getenv('SMTP_USER', '')
SMTP_PASS   = os.getenv('SMTP_PASS', '')
FROM_EMAIL  = os.getenv('FROM_EMAIL', SMTP_USER or 'noreply@cloudproof.dev')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')


def _smtp_configured() -> bool:
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASS)


def send_email(to: str, subject: str, html: str) -> bool:
    if not _smtp_configured():
        logger.info(f"\n{'='*60}\n[DEV EMAIL — configure SMTP to send real emails]\nTo: {to}\nSubject: {subject}\n{'='*60}")
        return False
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = f'CloudProof <{FROM_EMAIL}>'
    msg['To']      = to
    msg.attach(MIMEText(html, 'html'))
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(SMTP_USER, SMTP_PASS)
            srv.sendmail(FROM_EMAIL, to, msg.as_string())
        logger.info(f"Email sent → {to}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Email failed → {to}: {e}")
        return False


# ── Email templates (dark-theme, on-brand) ───────────────────────────────────

_WRAP = """
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
     max-width:460px;margin:40px auto;background:#0d1117;color:#e6edf3;
     padding:36px;border-radius:12px;border:1px solid #30363d;">
  <div style="font-size:22px;font-weight:700;color:#e6edf3;margin-bottom:4px;">
    ☁ CloudProof
  </div>
  <div style="height:1px;background:#30363d;margin:16px 0 24px;"></div>
  {body}
  <div style="height:1px;background:#21262d;margin:28px 0 16px;"></div>
  <p style="color:#484f58;font-size:12px;margin:0;">{footer}</p>
</div>
"""

_BTN = '<a href="{url}" style="display:inline-block;background:#238636;color:#fff;padding:11px 22px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">{label}</a>'


def send_verification_email(to: str, token: str) -> bool:
    url  = f"{FRONTEND_URL}/verify-email?token={token}"
    body = f"""
      <h1 style="font-size:20px;font-weight:700;margin:0 0 8px;">Verify your email address</h1>
      <p style="color:#8b949e;margin:0 0 24px;line-height:1.6;">
        Thanks for signing up for CloudProof — your AWS activity tracker.<br>
        Click the button below to verify your email and activate your account.
      </p>
      {_BTN.format(url=url, label='Verify Email →')}
    """
    footer = "This link expires in 24 hours. If you didn't sign up for CloudProof, you can safely ignore this email."
    return send_email(to, 'Verify your CloudProof email', _WRAP.format(body=body, footer=footer))


def send_reset_email(to: str, token: str) -> bool:
    url  = f"{FRONTEND_URL}/reset-password?token={token}"
    body = f"""
      <h1 style="font-size:20px;font-weight:700;margin:0 0 8px;">Reset your password</h1>
      <p style="color:#8b949e;margin:0 0 24px;line-height:1.6;">
        We received a request to reset your CloudProof password.<br>
        Click the button below to set a new password. This link expires in <strong>1 hour</strong>.
      </p>
      {_BTN.format(url=url, label='Reset Password →')}
    """
    footer = "If you didn't request a password reset, your password remains unchanged."
    return send_email(to, 'Reset your CloudProof password', _WRAP.format(body=body, footer=footer))
