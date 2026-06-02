-- OpenClaw가 방문 통계를 조회하는 뷰
CREATE OR REPLACE VIEW visit_stats_daily AS
SELECT
  DATE(created_at) as date,
  COUNT(*) as total_visits,
  COUNT(DISTINCT user_agent) as unique_visitors,
  url,
  COUNT(*) as page_views
FROM visit_logs
GROUP BY DATE(created_at), url
ORDER BY date DESC, page_views DESC;

-- 오늘 방문자 수
CREATE OR REPLACE VIEW visit_today AS
SELECT
  COUNT(*) as total_today,
  COUNT(DISTINCT user_agent) as unique_today,
  url,
  COUNT(*) as views
FROM visit_logs
WHERE DATE(created_at) = CURRENT_DATE
GROUP BY url
ORDER BY views DESC;
