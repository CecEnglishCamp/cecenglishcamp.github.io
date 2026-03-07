export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);

    // POST /register — 등록 저장
    if (request.method === 'POST' && url.pathname === '/register') {
      const data = await request.json();
      const now = new Date().toISOString();

      // 접수 번호 생성 (CEC-2026-001)
      const countResult = await env.cec_registrations.prepare(
        'SELECT COUNT(*) as cnt FROM registrations'
      ).first();
      const seq = String((countResult.cnt || 0) + 1).padStart(3, '0');
      const receipt_no = `CEC-2026-${seq}`;

      await env.cec_registrations.prepare(`
        INSERT INTO registrations
        (receipt_no, last_name, first_name, camp, grade, parent_phone, email, username, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        receipt_no,
        data.last_name || '',
        data.first_name || '',
        data.camp || '',
        data.grade || '',
        data.parent_phone || '',
        data.email || '',
        data.username || '',
        now
      ).run();

      return new Response(JSON.stringify({ ok: true, receipt_no }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // GET /list — 등록자 목록 조회 (관리자용)
    if (request.method === 'GET' && url.pathname === '/list') {
      const secret = url.searchParams.get('secret');
      if (secret !== 'cec2026admin') {
        return new Response('Unauthorized', { status: 401 });
      }
      const result = await env.cec_registrations.prepare(
        'SELECT * FROM registrations ORDER BY id DESC'
      ).all();
      return new Response(JSON.stringify(result.results), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    return new Response('Not Found', { status: 404 });
  }
};
