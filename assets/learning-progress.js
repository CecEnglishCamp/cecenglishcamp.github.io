/* CEC English Camp · learning progress client
 * cecenglishcamp.com은 Production Worker를 사용한다.
 * localhost/loopback 페이지에서는 window.CEC_LEARNING_PROGRESS_LOCAL_BASE 주입을 허용한다.
 */
(function () {
  'use strict';

  var SUPABASE_URL = 'https://rzlqlokqplhyntuirsmd.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_A4HJDb41-YeAMIaRnB8KeQ_ssECgA6q';
  var PRODUCTION_PROGRESS_URL = 'https://cec-robo-router-production.cecenglishcamp.workers.dev/robo/v1/learning/progress';
  var PROGRESS_PATH = '/robo/v1/learning/progress';
  var CURRICULUM_YEAR = 2026;
  var CURRICULUM_VERSION = 'prelaunch-1';
  var attemptedLessons = {};
  var pendingLessons = {};
  var authClient = null;

  function isLoopbackHost(hostname) {
    return hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1';
  }

  function progressUrl() {
    var currentHost = window.location && window.location.hostname;
    var currentProtocol = window.location && window.location.protocol;
    if (currentHost === 'cecenglishcamp.com') return PRODUCTION_PROGRESS_URL;
    if (!isLoopbackHost(currentHost) && !(currentHost === '' && currentProtocol === 'file:')) return null;

    var base = window.CEC_LEARNING_PROGRESS_LOCAL_BASE;
    if (typeof base !== 'string' || !base.trim()) return null;
    try {
      var parsed = new URL(base);
      if (!/^https?:$/.test(parsed.protocol) || !isLoopbackHost(parsed.hostname)) return null;
      return new URL(PROGRESS_PATH, parsed.origin).toString();
    } catch (_error) {
      return null;
    }
  }

  function getAuthClient() {
    if (authClient) return authClient;
    if (!window.supabase || typeof window.supabase.createClient !== 'function') return null;
    authClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    return authClient;
  }

  function safeResult(ok, code) {
    return { ok: ok === true, code: code };
  }

  async function getStudentContext() {
    var api = window.CECStudentContext;
    if (!api || typeof api.getStudentContext !== 'function') return null;
    try {
      var context = await api.getStudentContext();
      if (!context || context.status !== 'ready' || !context.student ||
          typeof context.student.id !== 'string' || !context.student.id) return null;
      return context;
    } catch (_error) {
      return null;
    }
  }

  async function complete(lessonId) {
    if (typeof lessonId !== 'string' || !lessonId || lessonId.length > 80) {
      return safeResult(false, 'INVALID_REQUEST');
    }

    var url = progressUrl();
    if (!url) return safeResult(false, 'LOCAL_API_NOT_CONFIGURED');
    if (attemptedLessons[lessonId] || pendingLessons[lessonId]) {
      return safeResult(false, 'DUPLICATE_SKIPPED');
    }
    pendingLessons[lessonId] = true;

    var studentContext = await getStudentContext();
    if (!studentContext) {
      delete pendingLessons[lessonId];
      return safeResult(false, 'STUDENT_CONTEXT_BLOCKED');
    }

    var client = getAuthClient();
    if (!client || !client.auth || typeof client.auth.getSession !== 'function') {
      delete pendingLessons[lessonId];
      return safeResult(false, 'AUTH_UNAVAILABLE');
    }

    var sessionResult;
    try {
      sessionResult = await client.auth.getSession();
    } catch (_error) {
      delete pendingLessons[lessonId];
      return safeResult(false, 'AUTH_INVALID');
    }
    var session = sessionResult && sessionResult.data && sessionResult.data.session;
    if (!session || !session.access_token) {
      delete pendingLessons[lessonId];
      return safeResult(false, 'AUTH_REQUIRED');
    }

    delete pendingLessons[lessonId];
    attemptedLessons[lessonId] = true;
    var controller = typeof AbortController === 'function' ? new AbortController() : null;
    var timeout = controller ? setTimeout(function () { controller.abort(); }, 5000) : null;
    try {
      var response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + session.access_token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: studentContext.student.id,
          lesson_id: lessonId,
          event: 'completed',
          curriculum_year: CURRICULUM_YEAR,
          curriculum_version: CURRICULUM_VERSION
        }),
        signal: controller ? controller.signal : undefined
      });
      var body = null;
      try { body = await response.json(); } catch (_error) { body = null; }
      if (response.ok && body && body.ok === true && body.lesson_id === lessonId && body.status === 'completed') {
        return safeResult(true, 'COMPLETED');
      }
      var code = body && typeof body.code === 'string' ? body.code : 'PROGRESS_WRITE_FAILED';
      return safeResult(false, code);
    } catch (_error) {
      return safeResult(false, 'PROGRESS_WRITE_FAILED');
    } finally {
      if (timeout !== null) clearTimeout(timeout);
    }
  }

  window.CECLearningProgress = Object.freeze({
    complete: complete,
    getStudentContext: getStudentContext
  });
})();
