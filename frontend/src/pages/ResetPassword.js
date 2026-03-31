import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default function ResetPassword() {
  const navigate      = useNavigate();
  const [params]      = useSearchParams();
  const token         = params.get('token') || '';

  const [password, setPassword]   = useState('');
  const [confirm,  setConfirm]    = useState('');
  const [showPwd,  setShowPwd]    = useState(false);
  const [loading,  setLoading]    = useState(false);
  const [error,    setError]      = useState('');
  const [success,  setSuccess]    = useState(false);

  if (!token) {
    return (
      <div className="auth-page">
        <div className="auth-logo"><div className="logo-box">☁</div><h1>CloudProof</h1></div>
        <div className="auth-card" style={{ padding: 28 }}>
          <div className="auth-error">Invalid or missing reset token. <button className="auth-link" onClick={() => navigate('/login')}>Go to login</button></div>
        </div>
      </div>
    );
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (password !== confirm)   { setError("Passwords don't match."); return; }
    if (password.length < 8)    { setError('Password must be at least 8 characters.'); return; }
    setLoading(true);
    try {
      await axios.post(`${API}/api/auth/reset-password`, { token, password });
      setSuccess(true);
      setTimeout(() => navigate('/login'), 2500);
    } catch (err) {
      setError(err.response?.data?.error || 'Reset failed. The link may have expired.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-logo">
        <div className="logo-box">☁</div>
        <h1>CloudProof</h1>
        <p>Set a new password</p>
      </div>

      <div className="auth-card">
        <div className="auth-body">
          {success ? (
            <div style={{ textAlign: 'center', padding: '12px 0' }}>
              <div style={{ fontSize: 36, marginBottom: 12 }}>✅</div>
              <div style={{ fontWeight: 600, marginBottom: 6 }}>Password updated!</div>
              <div style={{ color: 'var(--text-2)', fontSize: 13 }}>Redirecting to sign in…</div>
            </div>
          ) : (
            <>
              <h2 className="auth-section-title">Choose a new password</h2>
              <form onSubmit={handleSubmit} className="auth-form">
                <div className="auth-field">
                  <label>New password <span className="req">*</span></label>
                  <div className="auth-pwd-wrap">
                    <input
                      type={showPwd ? 'text' : 'password'}
                      value={password} onChange={e => setPassword(e.target.value)}
                      placeholder="At least 8 characters" required minLength={8}
                      autoFocus autoComplete="new-password"
                    />
                    <button type="button" className="auth-pwd-toggle" onClick={() => setShowPwd(v => !v)}>
                      {showPwd ? '🙈' : '👁'}
                    </button>
                  </div>
                </div>
                <div className="auth-field">
                  <label>Confirm password <span className="req">*</span></label>
                  <input type="password" value={confirm} onChange={e => setConfirm(e.target.value)}
                    placeholder="Repeat your password" required autoComplete="new-password" />
                  {confirm && confirm !== password && <p className="auth-field-err">Passwords don't match.</p>}
                </div>
                {error && <div className="auth-error">{error}</div>}
                <button type="submit" className="auth-submit" disabled={loading}>
                  {loading ? 'Updating…' : 'Set new password →'}
                </button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
