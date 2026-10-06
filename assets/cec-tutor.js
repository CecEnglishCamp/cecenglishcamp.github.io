/* Shared transport for the server-fixed Tutor Router. */
(function () {
  'use strict';

  function endpoint() {
    var configured = window.CEC_TUTOR_ENDPOINT;
    if (typeof configured !== 'string' || !configured) {
      throw new Error('TUTOR_NOT_CONFIGURED');
    }

    var url = new URL(configured, window.location.origin);
    var localEndpoint = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(url.hostname);
    var localPage = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(window.location.hostname);
    if (
      url.username || url.password || url.search || url.hash ||
      url.pathname !== '/robo/v1/tutor' ||
      !(url.protocol === 'https:' || (localEndpoint && localPage && url.protocol === 'http:'))
    ) {
      throw new Error('INVALID_TUTOR_ENDPOINT');
    }
    return url.href;
  }

  function escapeText(text) {
    return String(text).replace(/[&<>"']/g, function (character) {
      return {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      }[character];
    });
  }

  async function request(input) {
    if (!input || typeof input.lesson_id !== 'string' || typeof input.student_message !== 'string') {
      throw new Error('INVALID_REQUEST');
    }

    var response = await window.fetch(endpoint(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lesson_id: input.lesson_id,
        student_message: input.student_message
      })
    });
    if (!response.ok) return response;

    var data = await response.json();
    if (!data || data.ok !== true || data.lesson_id !== input.lesson_id || typeof data.reply !== 'string') {
      throw new Error('AI_INVALID_RESPONSE');
    }

    // Preserve the existing page SSE reader contract with one safe reply event.
    var event = {
      choices: [{ delta: { content: escapeText(data.reply) } }]
    };
    return new Response(
      'data: ' + JSON.stringify(event) + '\n\ndata: [DONE]\n\n',
      { headers: { 'Content-Type': 'text/event-stream' } }
    );
  }

  window.CECTutor = Object.freeze({ request: request });
})();
