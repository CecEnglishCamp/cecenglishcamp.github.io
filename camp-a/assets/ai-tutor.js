/**
 * CEC 영어캠프 — AI Tutor Fallback Helper v20260619_4
 * 
 * API(DeepSeek Chat) 연결 실패 시 로컬 fallback 답변을 제공합니다.
 * 기술 오류 메시지를 학생에게 노출하지 않습니다.
 * 
 * 모든 AI 메시지는 sanitizeTutorMessage를 통과해야 합니다.
 * gbAddAI 함수가 호출될 때 자동으로 필터링됩니다.
 */

console.log("[AI Tutor] fallback module loaded v20260619_4");

(function() {
  // 전역 설정 — 공백이면 fallback 전용으로 작동
  window.AI_TUTOR_ENDPOINT =
    window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? 'https://api.cecenglishcamp.com/api/deepseek/chat/completions'
      : null; // live: fallback only (API tunnel unstable)

  /**
   * 최종 방어 필터 — 화면에 출력되기 전에 모든 오류 메시지를 차단
   * gbAddAI가 이 함수를 통과하도록 오버라이드됩니다.
   */
  window.sanitizeTutorMessage = function(text, fallbackCtx) {
    var s = String(text || '');
    var blocked = [
      'Failed to fetch',
      '연결 실패',
      'NetworkError',
      'Network Error',
      'Load failed',
      'TypeError',
      'fetch failed',
      '530',
      'tunnel error',
      'ERR_CONNECTION',
      'ERR_NAME_NOT_RESOLVED'
    ];
    for (var i = 0; i < blocked.length; i++) {
      if (s.indexOf(blocked[i]) >= 0) {
        console.warn('[AI Tutor] BLOCKED error message from display:', s);
        var ctx = fallbackCtx || {};
        var q = ctx.question || '이 이야기가 뭐야?';
        return window.gbLocalFallback
          ? window.gbLocalFallback(q, ctx)
          : 'Robo 선생님이 지금 기본 모드로 대답할게요. 오늘 문장을 다시 읽어볼까요?';
      }
    }
    return s;
  };

  /**
   * gbAddAI 오버라이드 — 모든 AI 메시지 출력 전 sanitizeTutorMessage 필터링
   * (week 페이지가 gbAddAI를 선언한 이후에 실행되도록 setTimeout 사용)
   */
  setTimeout(function() {
    if (typeof window.gbAddAI !== 'function') {
      // gbAddAI가 아직 정의되지 않았으면 기다림
      var checkExist = setInterval(function() {
        if (typeof window.gbAddAI === 'function') {
          clearInterval(checkExist);
          var origGbAddAI = window.gbAddAI;
          window.gbAddAI = function(msg, ctx) {
            var safeMsg = window.sanitizeTutorMessage(msg, ctx || {
              question: '이 이야기가 뭐야?',
              title: window.GB_BOOK || 'Peter Rabbit',
              sentence: window.GB_KEY_SENTENCE || ''
            });
            return origGbAddAI(safeMsg);
          };
          console.log('[AI Tutor] gbAddAI sanitize wrapper installed');
        }
      }, 100);
    } else {
      var origGbAddAI = window.gbAddAI;
      window.gbAddAI = function(msg, ctx) {
        var safeMsg = window.sanitizeTutorMessage(msg, ctx || {
          question: '이 이야기가 뭐야?',
          title: window.GB_BOOK || 'Peter Rabbit',
          sentence: window.GB_KEY_SENTENCE || ''
        });
        return origGbAddAI(safeMsg);
      };
      console.log('[AI Tutor] gbAddAI sanitize wrapper installed');
    }
  }, 50);

  /**
   * 로컬 fallback — API 없이도 Robo가 자연스럽게 대답
   */
  window.gbLocalFallback = function(question, ctx) {
    var book = ctx && ctx.title ? ctx.title : 'Peter Rabbit';
    var sentence = ctx && ctx.sentence ? ctx.sentence : '';

    var q = (question || '').toLowerCase();

    if (q.indexOf('이야기') >= 0 || q.indexOf('내용') >= 0 || q.indexOf('뭐') === 0 || q.indexOf('story') >= 0) {
      var s = '이 이야기는 <b>' + book + '</b> 이야기예요.';
      if (sentence) s += ' 오늘의 핵심 문장은 "<b>' + sentence + '</b>"입니다.';
      s += ' 천천히 읽고, 누가 무엇을 하는지 생각해 봐요.';
      return s;
    }

    if (q.indexOf('교훈') >= 0 || q.indexOf('배우') >= 0 || q.indexOf('lesson') >= 0 || q.indexOf('의미') >= 0) {
      return '이 이야기의 교훈은 <b>조심하고 생각하며 행동하자</b>는 거예요. 가족 말을 잘 듣는 것도 중요해요!';
    }

    if (q.indexOf('주인공') >= 0 || q.indexOf('character') >= 0 || q.indexOf('누구') >= 0) {
      return '주인공은 <b>Peter Rabbit</b>이에요. Peter는 호기심 많고 활발한 꼬마 토끼예요.';
    }

    if (q.indexOf('왜') >= 0 || q.indexOf('이유') >= 0 || q.indexOf('why') >= 0 || q.indexOf('because') >= 0) {
      return '좋은 질문이에요! 문장을 다시 읽어보고 <b>누가 무엇을 했는지</b> 찾아보세요. 행동에는 항상 이유가 있어요.';
    }

    if (sentence) {
      return '좋은 질문이에요. 오늘 문장 "<b>' + sentence + '</b>"를 먼저 읽어볼까요? 영어 문장을 따라 말한 뒤, 무슨 뜻인지 생각해 봐요.';
    }

    return '좋은 질문이에요! <b>' + book + '</b> 이야기를 함께 살펴보면서 영어 문장을 따라 말해 봐요.';
  };
})();
