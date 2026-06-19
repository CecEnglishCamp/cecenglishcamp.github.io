/**
 * CEC 영어캠프 — AI Tutor Fallback Helper
 * 
 * API(DeepSeek Chat) 연결 실패 시 로컬 fallback 답변을 제공합니다.
 * 기술 오류 메시지를 학생에게 노출하지 않습니다.
 */

(function() {
  // 전역 설정 — 공백이면 fallback 전용으로 작동
  window.AI_TUTOR_ENDPOINT =
    window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? 'https://api.cecenglishcamp.com/api/deepseek/chat/completions'
      : null; // live: fallback only (API tunnel unstable)

  /**
   * 로컬 fallback — API 없이도 Robo가 자연스럽게 대답
   */
  window.gbLocalFallback = function(question, ctx) {
    var book = ctx && ctx.book ? ctx.book : 'Peter Rabbit';
    var sentence = ctx && ctx.sentence ? ctx.sentence : '';

    var q = (question || '').toLowerCase();

    if (q.indexOf('???') >= 0 || q.indexOf('???') >= 0 || q.indexOf('?') === 0 || q.indexOf('story') >= 0) {
      var s = '이 이야기는 <b>' + book + '</b> 이야기예요.';
      if (sentence) s += ' 오늘의 핵심 문장은 "<b>' + sentence + '</b>"입니다.';
      s += ' 천천히 읽고, 누가 무엇을 하는지 생각해 봐요.';
      return s;
    }

    if (q.indexOf('??') >= 0 || q.indexOf('????') >= 0 || q.indexOf('lesson') >= 0 || q.indexOf('??') >= 0) {
      return '이 이야기의 교훈은 <b>조심하고 생각하며 행동하자</b>는 거예요. 가족 말을 잘 듣는 것도 중요해요!';
    }

    if (q.indexOf('???') >= 0 || q.indexOf('character') >= 0 || q.indexOf('????') >= 0) {
      return '주인공은 <b>Peter Rabbit</b>이에요. Peter는 호기심 많고 활발한 꼬마 토끼예요.';
    }

    if (q.indexOf('??') >= 0 || q.indexOf('??') >= 0 || q.indexOf('why') >= 0 || q.indexOf('because') >= 0) {
      return '좋은 질문이에요! 문장을 다시 읽어보고 <b>누가 무엇을 했는지</b> 찾아보세요. 행동에는 항상 이유가 있어요.';
    }

    if (sentence) {
      return '좋은 질문이에요. 오늘 문장 "<b>' + sentence + '</b>"를 먼저 읽어볼까요? 영어 문장을 따라 말한 뒤, 무슨 뜻인지 생각해 봐요.';
    }

    return '좋은 질문이에요! <b>' + book + '</b> 이야기를 함께 살펴보면서 영어 문장을 따라 말해 봐요.';
  };
})();
