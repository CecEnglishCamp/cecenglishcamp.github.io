/* CEC legacy Robo auth transport shim.
 * Adds the current Supabase access token only to the legacy CEC AI POST.
 * Public pages remain viewable and unauthenticated requests remain unauthenticated.
 */
(function () {
  'use strict';

  if (window.CECLegacyAuthShim) return;

  var LEGACY_ORIGIN = 'https://cec-robo.cecenglishcamp.workers.dev';
  var LEGACY_PATH = '/api/ai/chat/completions';
  var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
  var originalFetch = window.fetch.bind(window);
  var publicAuthClientPromise = null;

  function requestMethod(input, init) {
    if (init && typeof init.method === 'string') return init.method.toUpperCase();
    if (typeof Request !== 'undefined' && input instanceof Request) {
      return input.method.toUpperCase();
    }
    return 'GET';
  }

  function isLegacyAiRequest(input, init) {
    if (requestMethod(input, init) !== 'POST') return false;
    var rawUrl = typeof input === 'string' || input instanceof URL ? input : input && input.url;
    if (!rawUrl) return false;
    try {
      var url = new URL(rawUrl, window.location.href);
      return url.origin === LEGACY_ORIGIN && url.pathname === LEGACY_PATH;
    } catch (_error) {
      return false;
    }
  }

  function loadSupabase() {
    if (window.supabase && typeof window.supabase.createClient === 'function') {
      return Promise.resolve(window.supabase);
    }
    return new Promise(function (resolve, reject) {
      var existing = document.querySelector && document.querySelector(
        'script[data-cec-legacy-auth-supabase],script[src^="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"]'
      );
      var script = existing || document.createElement('script');
      function loaded() {
        if (window.supabase && typeof window.supabase.createClient === 'function') {
          resolve(window.supabase);
        } else {
          reject(new Error('AUTH_SDK_UNAVAILABLE'));
        }
      }
      script.addEventListener('load', loaded, { once: true });
      script.addEventListener('error', function () {
        reject(new Error('AUTH_SDK_UNAVAILABLE'));
      }, { once: true });
      if (!existing) {
        script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
        script.setAttribute('data-cec-legacy-auth-supabase', 'true');
        document.head.appendChild(script);
      }
    });
  }

  function getPublicAuthClient() {
    if (!publicAuthClientPromise) {
      publicAuthClientPromise = loadSupabase().then(function (supabase) {
        return supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
      });
    }
    return publicAuthClientPromise;
  }

  function getSession() {
    if (window.CECAuthSession && typeof window.CECAuthSession.getSession === 'function') {
      return window.CECAuthSession.getSession().catch(function () { return null; });
    }
    return getPublicAuthClient()
      .then(function (client) { return client.auth.getSession(); })
      .then(function (result) {
        return result && result.data ? (result.data.session || null) : null;
      })
      .catch(function () { return null; });
  }

  window.fetch = async function (input, init) {
    if (!isLegacyAiRequest(input, init)) return originalFetch(input, init);

    var session = await getSession();
    var token = session && typeof session.access_token === 'string'
      ? session.access_token
      : '';
    if (!token) return originalFetch(input, init);

    var sourceHeaders = init && init.headers !== undefined
      ? init.headers
      : (typeof Request !== 'undefined' && input instanceof Request ? input.headers : undefined);
    var headers = new Headers(sourceHeaders);
    headers.set('Authorization', 'Bearer ' + token);
    var nextInit = Object.assign({}, init || {}, { headers: headers });
    return originalFetch(input, nextInit);
  };

  window.CECLegacyAuthShim = Object.freeze({
    targetOrigin: LEGACY_ORIGIN,
    targetPath: LEGACY_PATH
  });
})();
