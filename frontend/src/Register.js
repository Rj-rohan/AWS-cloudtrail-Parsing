import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const REGIONS = [
  'us-east-1','us-east-2','us-west-1','us-west-2',
  'ap-south-1','ap-northeast-1','ap-southeast-1','ap-southeast-2',
  'eu-west-1','eu-central-1','ca-central-1','sa-east-1',
];

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: '', name: '', email: '',
    s3_bucket: '', s3_prefix: '', aws_region: 'us-east-1',
    sync_pin: '', confirm_pin: '',
  });
  const [errs,       setErrs]       = useState({});
  const [apiErr,     setApiErr]     = useState('');
  const [submitting, setSubmitting] = useState(false);

  const set = (k, v) => {
    setForm(f => ({ ...f, [k]: v }));
    setErrs(e => ({ ...e, [k]: '' }));
    setApiErr('');
  };

  const validate = () => {
    const e = {};
    if (!form.username.trim())
      e.username = 'Required.';
    else if (!/^[a-z0-9_-]{3,30}$/.test(form.username))
      e.username = 'Lowercase letters, numbers, hyphens, underscores — 3 to 30 chars.';

    if (!form.name.trim())   e.name  = 'Required.';
    if (!form.email.trim())  e.email = 'Required.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) e.email = 'Enter a valid email.';
    if (!form.s3_bucket.trim()) e.s3_bucket = 'Required.';

    if (!form.sync_pin)          e.sync_pin = 'Required.';
    else if (form.sync_pin.length < 4) e.sync_pin = 'Minimum 4 characters.';
    if (form.sync_pin !== form.confirm_pin) e.confirm_pin = 'Passwords do not match.';

    setErrs(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = async e => {
    e.preventDefault();
    if (!validate()) return;
    setSubmitting(true);
    setApiErr('');
    try {
      await axios.post(`${API}/api/register`, {
        username:   form.username.trim().toLowerCase(),
        name:       form.name.trim(),
        email:      form.email.trim(),
        s3_bucket:  form.s3_bucket.trim(),
        s3_prefix:  form.s3_prefix.trim(),
        aws_region: form.aws_region || 'us-east-1',
        sync_pin:   form.sync_pin,
      });
      // Mark this browser as the owner so the Sync / Test buttons are shown
      localStorage.setItem(`cloudproof_owner_${form.username.trim().toLowerCase()}`, 'true');
      navigate(`/${form.username.trim().toLowerCase()}`);
    } catch (err) {
      setApiErr(err.response?.data?.error || 'Something went wrong. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="reg-page">
      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <div className="reg-top">
        <div className="reg-logo">
          <div className="logo-box">☁</div>
          CloudProof
        </div>
        <h1>Verify Your AWS Experience</h1>
        <p>
          Create a public profile backed by real CloudTrail activity — not just claims.
          Share it with recruiters like a LeetCode profile.
        </p>
        <div className="pills">
          <span className="pill">📊 CloudTrail-backed scores</span>
          <span className="pill">🗓 GitHub-style heatmap</span>
          <span className="pill">🔗 Shareable public profile</span>
          <span className="pill">🛡 Raw logs never stored</span>
        </div>
      </div>

      {/* ── Form ─────────────────────────────────────────────────────────── */}
      <div className="reg-body">
        <form onSubmit={handleSubmit}>
          <div className="reg-card">

            {/* Identity */}
            <div className="reg-section">
              <div className="reg-section-lbl">👤 Identity</div>

              <div className="fg">
                <label className="fl">Username <span style={{color:'var(--red)'}}>*</span></label>
                <div className={`username-wrap${errs.username ? ' err' : ''}`}>
                  <span className="username-prefix">{window.location.host}/</span>
                  <input
                    className="fi"
                    type="text"
                    placeholder="john-doe"
                    value={form.username}
                    onChange={e => set('username', e.target.value.toLowerCase())}
                    autoComplete="off"
                    spellCheck={false}
                  />
                </div>
                {errs.username
                  ? <div className="ferr">{errs.username}</div>
                  : <div className="fhint">Your public URL: <strong style={{color:'var(--blue)'}}>{window.location.host}/{form.username || 'username'}</strong></div>
                }
              </div>

              <div className="fg">
                <label className="fl">Display Name <span style={{color:'var(--red)'}}>*</span></label>
                <input
                  className={`fi${errs.name?' err':''}`}
                  type="text" placeholder="John Doe"
                  value={form.name} onChange={e => set('name', e.target.value)}
                />
                {errs.name && <div className="ferr">{errs.name}</div>}
              </div>

              <div className="fg" style={{marginBottom:0}}>
                <label className="fl">Email <span style={{color:'var(--red)'}}>*</span></label>
                <input
                  className={`fi${errs.email?' err':''}`}
                  type="email" placeholder="you@example.com"
                  value={form.email} onChange={e => set('email', e.target.value)}
                />
                {errs.email && <div className="ferr">{errs.email}</div>}
              </div>
            </div>

            {/* AWS Config */}
            <div className="reg-section">
              <div className="reg-section-lbl">☁ AWS S3 Configuration</div>
              <div className="alert alert-info">
                Enable CloudTrail in your AWS account and configure it to deliver logs to an S3 bucket.
                Enter that bucket name below.
              </div>

              <div className="fg">
                <label className="fl">S3 Bucket Name <span style={{color:'var(--red)'}}>*</span></label>
                <input
                  className={`fi${errs.s3_bucket?' err':''}`}
                  type="text" placeholder="my-cloudtrail-logs-bucket"
                  value={form.s3_bucket} onChange={e => set('s3_bucket', e.target.value)}
                />
                {errs.s3_bucket
                  ? <div className="ferr">{errs.s3_bucket}</div>
                  : <div className="fhint">The S3 bucket where CloudTrail delivers your logs.</div>
                }
              </div>

              <div className="fg">
                <label className="fl">S3 Prefix <span style={{color:'var(--text-3)',fontWeight:400,textTransform:'none',letterSpacing:0}}>(optional)</span></label>
                <input
                  className="fi"
                  type="text" placeholder="AWSLogs/123456789/"
                  value={form.s3_prefix} onChange={e => set('s3_prefix', e.target.value)}
                />
                <div className="fhint">Folder path inside the bucket. Leave blank to scan the whole bucket.</div>
              </div>

              <div className="fg" style={{marginBottom:0}}>
                <label className="fl">AWS Region</label>
                <select className="fsel" value={form.aws_region} onChange={e => set('aws_region', e.target.value)}>
                  {REGIONS.map(r => <option key={r} value={r}>{r}</option>)}
                </select>
              </div>
            </div>

            {/* Security */}
            <div className="reg-section">
              <div className="reg-section-lbl">🔐 Security</div>
              <div className="alert alert-info">
                This password protects your Sync button — only you can trigger syncs.
                It is NOT your AWS password. Save it somewhere safe.
              </div>

              <div className="fg">
                <label className="fl">Sync Password <span style={{color:'var(--red)'}}>*</span></label>
                <input
                  className={`fi${errs.sync_pin?' err':''}`}
                  type="password" placeholder="Min 4 characters"
                  value={form.sync_pin} onChange={e => set('sync_pin', e.target.value)}
                  autoComplete="new-password"
                />
                {errs.sync_pin && <div className="ferr">{errs.sync_pin}</div>}
              </div>

              <div className="fg" style={{marginBottom:0}}>
                <label className="fl">Confirm Password <span style={{color:'var(--red)'}}>*</span></label>
                <input
                  className={`fi${errs.confirm_pin?' err':''}`}
                  type="password" placeholder="Repeat your password"
                  value={form.confirm_pin} onChange={e => set('confirm_pin', e.target.value)}
                />
                {errs.confirm_pin && <div className="ferr">{errs.confirm_pin}</div>}
              </div>
            </div>

            {/* Footer */}
            <div className="reg-footer">
              {apiErr
                ? <div className="alert alert-error" style={{marginBottom:0,flex:1}}>{apiErr}</div>
                : <div className="reg-terms">Your raw logs are never stored — only activity scores and counts.</div>
              }
              <button type="submit" className="btn btn-primary btn-lg" disabled={submitting}>
                {submitting ? <><span className="spinner" />Creating…</> : 'Create Profile →'}
              </button>
            </div>

          </div>
        </form>
      </div>
    </div>
  );
}
