/**
 * /auth/callback
 * Backend redirects here after OAuth success with ?token=…&username=…&has_bucket=…
 * Stores credentials and routes to setup or profile.
 */
import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

export default function AuthCallback() {
  const navigate     = useNavigate();
  const [params]     = useSearchParams();
  const [error, setError] = useState('');

  useEffect(() => {
    const token      = params.get('token');
    const username   = params.get('username');
    const hasBucket  = params.get('has_bucket') === '1';
    const oauthError = params.get('error');

    if (oauthError) {
      setError(decodeURIComponent(oauthError));
      setTimeout(() => navigate('/login'), 3000);
      return;
    }

    if (!token || !username) {
      setError('Auth failed — missing token. Redirecting to login…');
      setTimeout(() => navigate('/login'), 2500);
      return;
    }

    localStorage.setItem('cloudproof_token', token);
    localStorage.setItem('cloudproof_user', JSON.stringify({ username, has_bucket: hasBucket }));

    if (!hasBucket) navigate('/setup');
    else            navigate(`/${username}`);
  }, [params, navigate]);

  return (
    <div className="auth-page">
      <div className="auth-logo">
        <div className="logo-box">☁</div>
        <h1>CloudProof</h1>
      </div>
      {error
        ? <div className="auth-card" style={{ padding: 28, textAlign: 'center' }}>
            <div className="auth-error">{error}</div>
          </div>
        : <div className="auth-card" style={{ padding: 28, textAlign: 'center', color: 'var(--text-2)' }}>
            <span className="spinner" style={{ marginRight: 8 }} />
            Signing you in…
          </div>
      }
    </div>
  );
}
