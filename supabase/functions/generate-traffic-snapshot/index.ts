/**
 * CEC English Camp - generate-traffic-snapshot
 * Supabase Edge Function
 *
 * Called by GitHub Actions every 2 hours.
 * Queries visit_events for the most recent 2-hour window,
 * summarizes page_views, unique visitors, top pages, referrers,
 * and inserts a snapshot row into traffic_reports.
 *
 * Deploy:
 *   supabase functions deploy generate-traffic-snapshot --project-ref rzlqlokqplhyntuirsmd
 */

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const SUPABASE_URL         = Deno.env.get('SUPABASE_URL')!;
const SUPABASE_SERVICE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;

Deno.serve(async (req) => {
  // ── Auth ──
  const authHeader = req.headers.get('Authorization') || '';
  const secret     = Deno.env.get('REPORT_SECRET') || '';
  if (secret && authHeader !== `Bearer ${secret}`) {
    return new Response('Unauthorized', { status: 401 });
  }

  // ── Time window (UTC) ──
  const now = new Date();
  const windowEnd = new Date(now);
  windowEnd.setMinutes(0, 0, 0);
  const windowStart = new Date(windowEnd.getTime() - 2 * 60 * 60 * 1000);

  const startISO = windowStart.toISOString();
  const endISO   = windowEnd.toISOString();

  // ── Time label (America/Los_Angeles) ──
  const tz = 'America/Los_Angeles';
  const fmt = new Intl.DateTimeFormat('en-US', {
    timeZone: tz,
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
  const fmtDate = new Intl.DateTimeFormat('en-CA', {  // YYYY-MM-DD
    timeZone: tz,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });

  const startLabel = fmt.format(windowStart);
  const endLabel   = fmt.format(windowEnd);
  const dateStr    = fmtDate.format(windowEnd);  // report_date in PT
  const hourLabel  = `${startLabel} - ${endLabel} PT`;

  // ── Supabase client ──
  const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

  // ── 1. Fetch events in window ──
  const { data: events, error: fetchErr } = await sb
    .from('visit_events')
    .select('normalized_url, url, visitor_id, session_id, event_type, referrer, utm_source')
    .gte('created_at', startISO)
    .lt('created_at', endISO)
    .eq('is_bot', false)
    .eq('is_admin', false);

  if (fetchErr) {
    console.error('Fetch error:', fetchErr);
    return new Response(JSON.stringify({ error: fetchErr.message }), { status: 500 });
  }

  const total = events?.length || 0;

  // ── 2. Aggregate ──
  const uniqueVisitors = new Set(events?.map(e => e.visitor_id).filter(Boolean) || []).size;
  const uniqueSessions = new Set(events?.map(e => e.session_id).filter(Boolean) || []).size;

  // Event type counts
  const typeCount = new Map<string, number>();
  events?.forEach(e => {
    if (e.event_type) {
      typeCount.set(e.event_type, (typeCount.get(e.event_type) || 0) + 1);
    }
  });
  const pageViews   = typeCount.get('page_view') || 0;
  const ctaClicks   = typeCount.get('cta_click') || 0;
  const signupClicks  = typeCount.get('signup_click') || 0;
  const paymentClicks = typeCount.get('payment_click') || 0;

  // Top 5 pages
  const pageCount = new Map<string, number>();
  events?.forEach(e => {
    const page = e.normalized_url || e.url;
    if (page) {
      pageCount.set(page, (pageCount.get(page) || 0) + 1);
    }
  });
  const top5 = [...pageCount.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  // Referrer summary (domain level)
  const refCount = new Map<string, number>();
  events?.filter(e => e.referrer && e.referrer.trim()).forEach(e => {
    try {
      const domain = new URL(e.referrer).hostname.replace(/^www\./, '');
      refCount.set(domain, (refCount.get(domain) || 0) + 1);
    } catch {
      refCount.set('(direct)', (refCount.get('(direct)') || 0) + 1);
    }
  });
  const topRefs = [...refCount.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  // UTM source summary
  const utmCount = new Map<string, number>();
  events?.filter(e => e.utm_source && e.utm_source.trim()).forEach(e => {
    utmCount.set(e.utm_source, (utmCount.get(e.utm_source) || 0) + 1);
  });

  // ── 3. Build markdown ──
  const top5Lines = top5.length > 0
    ? top5.map(([url, count], i) => `| ${i + 1} | ${url} | ${count} |`).join('\n')
    : '| - | (데이터 없음) | 0 |';

  const refLines = topRefs.length > 0
    ? topRefs.map(([ref, count]) => `- ${ref}: ${count}`).join('\n')
    : '직접 방문 또는 데이터 없음';

  const utmLines = utmCount.size > 0
    ? [...utmCount.entries()].map(([src, count]) => `- ${src}: ${count}`).join('\n')
    : 'UTM 데이터 없음';

  const typeLines = [...typeCount.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([type, count]) => `- ${type}: ${count}`)
    .join('\n');

  const md = `# CEC Traffic Snapshot — ${hourLabel}

## 요약

| 항목 | 수치 |
|------|------|
| Total Events | ${total} |
| Unique Visitors | ${uniqueVisitors} |
| Unique Sessions | ${uniqueSessions} |
| Page Views | ${pageViews} |
| CTA Clicks | ${ctaClicks} |
| Signup Clicks | ${signupClicks} |
| Payment Clicks | ${paymentClicks} |

## Top 5 Pages

| # | URL | Views |
|---|-----|-------|
${top5Lines}

## Referrer Top 5

${refLines}

## UTM Source

${utmLines}

## Event Type

${typeLines}
`;

  // ── 4. Upsert into traffic_reports ──
  const { error: upsertErr } = await sb
    .from('traffic_reports')
    .upsert({
      report_date:  dateStr,
      report_time:  hourLabel,
      timezone:     tz,
      snapshot:     true,
      window_start: startISO,
      window_end:   endISO,
      summary: {
        total_events:     total,
        unique_visitors:  uniqueVisitors,
        unique_sessions:  uniqueSessions,
        page_views:       pageViews,
        cta_clicks:       ctaClicks,
        signup_clicks:    signupClicks,
        payment_clicks:   paymentClicks,
      },
      markdown: md,
    }, {
      onConflict: 'report_date,report_time,snapshot',
    });

  if (upsertErr) {
    console.error('Upsert error:', upsertErr);
    return new Response(JSON.stringify({ error: upsertErr.message }), { status: 500 });
  }

  // GitHub Actions log summary
  console.log(`[OK] Snapshot ${hourLabel}: ${total} events, ${uniqueVisitors} visitors, ${uniqueSessions} sessions`);

  return new Response(JSON.stringify({
    ok: true,
    window: hourLabel,
    date: dateStr,
    total_events: total,
    unique_visitors: uniqueVisitors,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });
});
