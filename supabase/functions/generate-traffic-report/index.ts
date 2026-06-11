/**
 * CEC English Camp — generate-traffic-report
 * Supabase Edge Function
 *
 * Called by GitHub Actions at 12:00 PM and 6:00 PM PT.
 * Aggregates visit_events → builds markdown report → inserts into traffic_reports.
 *
 * Deploy:
 *   $env:SUPABASE_ACCESS_TOKEN="sbp_..."
 *   supabase functions deploy generate-traffic-report --project-ref rzlqlokqplhyntuirsmd
 */

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const SUPABASE_URL      = Deno.env.get('SUPABASE_URL')!;
const SUPABASE_SERVICE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;

Deno.serve(async (req) => {
  // Accept POST from GitHub Actions (Authorization: Bearer <REPORT_SECRET>)
  const authHeader = req.headers.get('Authorization') || '';
  const secret     = Deno.env.get('REPORT_SECRET') || '';
  if (secret && authHeader !== `Bearer ${secret}`) {
    return new Response('Unauthorized', { status: 401 });
  }

  const body       = await req.json().catch(() => ({}));
  const reportTime = (body.report_time as string) || '12:00 PM';   // '12:00 PM' | '6:00 PM'
  const tz         = 'America/Los_Angeles';

  const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

  // ── 1. Run daily aggregation for today ─────────────────
  await sb.rpc('aggregate_daily_stats');

  // Today's date in PT (GitHub sends UTC; Supabase stores UTC, we label by PT date)
  const nowPT   = new Date(new Date().toLocaleString('en-US', { timeZone: tz }));
  const dateStr = nowPT.toISOString().slice(0, 10);   // YYYY-MM-DD

  // ── 2. Fetch today's summary ───────────────────────────
  const { data: statsRows } = await sb
    .from('visit_stats_daily_v2')
    .select('*')
    .eq('date', dateStr);

  const total = (statsRows || []).reduce((acc, r) => ({
    page_views:      acc.page_views      + r.page_views,
    unique_visitors: acc.unique_visitors + r.unique_visitors,
    sessions:        acc.sessions        + r.sessions,
    cta_clicks:      acc.cta_clicks      + r.cta_clicks,
    signup_clicks:   acc.signup_clicks   + r.signup_clicks,
    payment_clicks:  acc.payment_clicks  + r.payment_clicks,
    bot_views:       acc.bot_views       + r.bot_views,
  }), {
    page_views: 0, unique_visitors: 0, sessions: 0,
    cta_clicks: 0, signup_clicks: 0, payment_clicks: 0, bot_views: 0
  });

  const avgDur = statsRows && statsRows.length > 0
    ? (statsRows.reduce((s, r) => s + (Number(r.avg_duration_seconds) || 0), 0) / statsRows.length).toFixed(0)
    : '—';

  // ── 3. Top 10 pages ────────────────────────────────────
  const top10 = [...(statsRows || [])]
    .sort((a, b) => b.page_views - a.page_views)
    .slice(0, 10);

  // ── 4. Conversion funnel ───────────────────────────────
  const funnelUrls = ['/', '/why-cec/', '/why-spacecamp/', '/payment/'];
  const funnel = Object.fromEntries(
    funnelUrls.map(u => {
      const row = (statsRows || []).find(r => r.normalized_url === u);
      return [u, row ? row.page_views : 0];
    })
  );

  // ── 5. Abnormal spike detection ────────────────────────
  const { data: spikes } = await sb.rpc('detect_abnormal_spikes', { target_date: dateStr });
  const abnormalFlags = (spikes || []).map((s: Record<string, unknown>) => ({
    url:    s.normalized_url,
    pv:     s.page_views,
    bv:     s.bot_views,
    ratio:  s.bot_ratio,
    reason: s.anomaly_reason,
  }));

  // ── 6. Recommendations ────────────────────────────────
  const recs: string[] = [];
  if (total.page_views > 0 && total.cta_clicks / total.page_views < 0.03) {
    recs.push('홈페이지 CTA 클릭률이 3% 미만입니다. CTA 위치·문구 개선을 검토하세요.');
  }
  if (funnel['/why-spacecamp/'] > 0 && funnel['/payment/'] === 0) {
    recs.push('Space Camp 페이지 유입은 있지만 payment 이동이 없습니다. CTA 강화가 필요합니다.');
  }
  if (total.bot_views > total.page_views * 0.2) {
    recs.push(`봇 트래픽 비중이 높습니다 (${total.bot_views}건). 비정상 IP 차단을 검토하세요.`);
  }
  if (abnormalFlags.length > 0) {
    recs.push(`비정상 트래픽 감지: ${abnormalFlags.length}개 URL 확인 필요`);
  }
  if (recs.length === 0) recs.push('특이 사항 없음. 정상 범위.');

  // ── 7. Build markdown report ───────────────────────────
  const title = `CEC Daily Traffic Report — ${dateStr} ${reportTime} PT`;

  const topTable = top10.map((r, i) =>
    `| ${i + 1} | ${r.normalized_url} | ${r.page_views} | ${r.unique_visitors} | ${r.cta_clicks} |`
  ).join('\n');

  const spikeBlock = abnormalFlags.length > 0
    ? abnormalFlags.map(f => `⚠️  \`${f.url}\` — ${f.reason} (PV: ${f.pv}, Bot: ${f.bv})`).join('\n')
    : '✅ 이상 징후 없음';

  const recsBlock = recs.map(r => `- ${r}`).join('\n');

  const md = `# ${title}

## 1. 오늘 현재 방문 요약

| 지표 | 값 |
|------|----|
| Page Views | ${total.page_views} |
| Unique Visitors | ${total.unique_visitors} |
| Sessions | ${total.sessions} |
| Avg Duration | ${avgDur}s |
| CTA Clicks | ${total.cta_clicks} |
| Signup Clicks | ${total.signup_clicks} |
| Payment Clicks | ${total.payment_clicks} |
| Bot (filtered) | ${total.bot_views} |

## 2. 상위 페이지 Top 10

| # | URL | Views | Unique | CTA |
|---|-----|-------|--------|-----|
${topTable}

## 3. 전환 흐름

| 페이지 | 방문자 수 |
|--------|-----------|
| / (홈) | ${funnel['/']} |
| /why-cec/ | ${funnel['/why-cec/']} |
| /why-spacecamp/ | ${funnel['/why-spacecamp/']} |
| /payment/ | ${funnel['/payment/']} |
| CTA 클릭 | ${total.cta_clicks} |

## 4. 이상 징후

${spikeBlock}

## 5. 추천 조치

${recsBlock}
`;

  // ── 8. Insert report ───────────────────────────────────
  const { error } = await sb.from('traffic_reports').insert({
    report_date:     dateStr,
    report_time:     reportTime,
    timezone:        tz,
    summary: {
      ...total,
      avg_duration_seconds: avgDur,
      funnel,
    },
    markdown:        md,
    abnormal_flags:  abnormalFlags,
    recommendations: recs,
  });

  if (error) {
    console.error('Insert error:', error);
    return new Response(JSON.stringify({ error: error.message }), { status: 500 });
  }

  return new Response(JSON.stringify({ ok: true, date: dateStr, report_time: reportTime }), {
    headers: { 'Content-Type': 'application/json' }
  });
});
