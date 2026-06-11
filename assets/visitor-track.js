/**
 * CEC English Camp — Visit Analytics v2
 * visitor-track.js
 *
 * Features:
 *  - URL normalization (strips origin, query, /index.html → /)
 *  - visitor_id (localStorage, persists across sessions)
 *  - session_id (sessionStorage, per-tab session)
 *  - Bot/admin detection
 *  - Dedup guard: same visitor+session+url within 10s → skip
 *  - Duration tracking (visibilitychange + beforeunload)
 *  - CTA click tracking via data-track-event attributes
 *  - Writes to: visit_events (Supabase)
 */
(function () {
  'use strict';

  // ── Guard: prevent double-execution ──────────────────
  if (window.__CEC_TRACKING_LOADED) return;
  window.__CEC_TRACKING_LOADED = true;

  // ── Config ────────────────────────────────────────────
  var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
  var ENDPOINT     = SUPABASE_URL + '/rest/v1/visit_events';

  // ── Bot user-agent patterns ───────────────────────────
  var BOT_PATTERNS = [
    'bot', 'crawler', 'spider', 'preview',
    'facebookexternalhit', 'slackbot', 'discordbot',
    'whatsapp', 'telegrambot', 'googlebot', 'bingbot',
    'ahrefsbot', 'semrushbot', 'bytespider', 'applebot',
    'duckduckbot', 'yandexbot', 'baiduspider', 'screaming'
  ];

  var ua = (navigator.userAgent || '').toLowerCase();
  var IS_BOT = BOT_PATTERNS.some(function (p) { return ua.indexOf(p) !== -1; });

  var IS_ADMIN = (function () {
    try { return localStorage.getItem('cec_admin') === 'true'; } catch (_) { return false; }
  })();

  // ── URL normalization ─────────────────────────────────
  function normalizeUrl(href) {
    try {
      var u = new URL(href, window.location.origin);
      // strip origin, keep path only
      var path = u.pathname;
      // /index.html → /
      path = path.replace(/\/index\.html$/, '/');
      // ensure trailing slash on directories (no extension)
      if (path !== '/' && !/\.[a-z0-9]+$/i.test(path) && path.slice(-1) !== '/') {
        path += '/';
      }
      return path;
    } catch (_) {
      return href;
    }
  }

  // ── UTM extraction ────────────────────────────────────
  function extractUtm(href) {
    try {
      var u = new URL(href, window.location.origin);
      return {
        utm_source:   u.searchParams.get('utm_source')   || null,
        utm_medium:   u.searchParams.get('utm_medium')   || null,
        utm_campaign: u.searchParams.get('utm_campaign') || null
      };
    } catch (_) { return {}; }
  }

  // ── Visitor / Session IDs ─────────────────────────────
  function getOrCreate(storage, key) {
    try {
      var v = storage.getItem(key);
      if (!v) {
        v = crypto.randomUUID ? crypto.randomUUID() : (
          Math.random().toString(36).slice(2) + '-' +
          Math.random().toString(36).slice(2)
        );
        storage.setItem(key, v);
      }
      return v;
    } catch (_) { return 'unknown'; }
  }

  var VISITOR_ID = getOrCreate(localStorage,   'cec_visitor_id');
  var SESSION_ID = getOrCreate(sessionStorage,  'cec_session_id');

  // ── 10-second dedup guard ─────────────────────────────
  var DEDUP_KEY    = 'cec_last_pv';
  var DEDUP_WINDOW = 10000; // ms

  function isDuplicate(normUrl) {
    try {
      var raw = sessionStorage.getItem(DEDUP_KEY);
      if (!raw) return false;
      var rec = JSON.parse(raw);
      return (
        rec.url === normUrl &&
        rec.vid === VISITOR_ID &&
        rec.sid === SESSION_ID &&
        (Date.now() - rec.ts) < DEDUP_WINDOW
      );
    } catch (_) { return false; }
  }

  function stampDedup(normUrl) {
    try {
      sessionStorage.setItem(DEDUP_KEY, JSON.stringify({
        url: normUrl, vid: VISITOR_ID, sid: SESSION_ID, ts: Date.now()
      }));
    } catch (_) {}
  }

  // ── Core: send event to Supabase ──────────────────────
  function sendEvent(payload) {
    // Always fill common fields
    payload.visitor_id  = VISITOR_ID;
    payload.session_id  = SESSION_ID;
    payload.is_bot      = IS_BOT;
    payload.is_admin    = IS_ADMIN;
    payload.user_agent  = navigator.userAgent;
    if (!payload.created_at) payload.created_at = new Date().toISOString();

    fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey':        SUPABASE_KEY,
        'Authorization': 'Bearer ' + SUPABASE_KEY,
        'Prefer':        'return=minimal'
      },
      body: JSON.stringify(payload)
    }).catch(function () { /* tracking failure is non-fatal */ });
  }

  // ── Page view ─────────────────────────────────────────
  var normUrl   = normalizeUrl(window.location.href);
  var utm       = extractUtm(window.location.href);
  var startTime = Date.now();

  setTimeout(function () {
    if (isDuplicate(normUrl)) return;
    stampDedup(normUrl);

    sendEvent(Object.assign({
      event_type:     'page_view',
      url:            window.location.href,
      normalized_url: normUrl,
      page_title:     document.title || '',
      referrer:       document.referrer || ''
    }, utm));
  }, 2000);

  // ── Duration tracking (session_end) ──────────────────
  function sendDuration() {
    var seconds = Math.round((Date.now() - startTime) / 1000);
    if (seconds < 1) return;
    if (seconds > 1800) seconds = 1800;
    sendEvent({
      event_type:      'session_end',
      normalized_url:  normUrl,
      duration_seconds: seconds
    });
  }

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') sendDuration();
  });
  window.addEventListener('beforeunload', sendDuration);

  // ── CTA click tracking ────────────────────────────────
  // Attach to any element with data-track-event attribute.
  // Usage:
  //   <a data-track-event="cta_click"
  //      data-track-label="home_free_trial"
  //      data-track-destination="/free-trial/">…</a>
  document.addEventListener('click', function (e) {
    var el = e.target;
    // Walk up to 3 levels to find the data-track-event anchor/button
    for (var i = 0; i < 3; i++) {
      if (!el) break;
      var evType = el.getAttribute && el.getAttribute('data-track-event');
      if (evType) {
        sendEvent({
          event_type:     evType,
          normalized_url: normUrl,
          metadata: {
            label:       el.getAttribute('data-track-label') || '',
            destination: el.getAttribute('data-track-destination') || ''
          }
        });
        return;
      }
      el = el.parentElement;
    }
  });

  // ── Legacy visit_logs insert (backwards compat) ───────
  // Keep writing to visit_logs so existing views/dashboards don't break.
  setTimeout(function () {
    if (IS_BOT) return;
    var legacyData = {
      type:       'pageview',
      url:        window.location.href,
      referrer:   document.referrer || '',
      user_agent: navigator.userAgent,
      created_at: new Date().toISOString()
    };
    var trial = document.cookie.match(/(?:^|;\s*)cec_trial=([^;]+)/);
    if (trial) legacyData.trial_token = trial[1];

    // Only use supabase-js path if available (avoids re-auth overhead)
    if (typeof supabase !== 'undefined') {
      var sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
      sb.auth.getSession().then(function (result) {
        var session = result && result.data && result.data.session;
        if (session && session.user) {
          legacyData.type    = 'login';
          legacyData.email   = session.user.email || '';
          legacyData.user_id = session.user.id    || '';
          legacyData.name    = (session.user.user_metadata || {}).full_name ||
                               (session.user.user_metadata || {}).name || '';
        }
        sb.from('visit_logs').insert([legacyData]);
      });
    } else {
      fetch(SUPABASE_URL + '/rest/v1/visit_logs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey':        SUPABASE_KEY,
          'Authorization': 'Bearer ' + SUPABASE_KEY
        },
        body: JSON.stringify(legacyData)
      }).catch(function () {});
    }
  }, 3000);

})();
