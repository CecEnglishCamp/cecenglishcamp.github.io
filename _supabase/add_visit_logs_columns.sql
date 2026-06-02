-- visit_logs 테이블 컬럼 추가 (없으면 추가, 있으면 무시)
ALTER TABLE visit_logs ADD COLUMN IF NOT EXISTS duration_seconds INTEGER;
ALTER TABLE visit_logs ADD COLUMN IF NOT EXISTS video_id TEXT;
ALTER TABLE visit_logs ADD COLUMN IF NOT EXISTS student_name TEXT;

-- OpenClaw용 통계 뷰
CREATE OR REPLACE VIEW visit_stats_daily AS
SELECT DATE(created_at) as date, url, COUNT(*) as views
FROM visit_logs WHERE type='pageview'
GROUP BY DATE(created_at), url ORDER BY date DESC, views DESC;

CREATE OR REPLACE VIEW visit_today AS
SELECT url, COUNT(*) as views, AVG(duration_seconds) as avg_seconds
FROM visit_logs WHERE type='pageview' AND DATE(created_at)=CURRENT_DATE
GROUP BY url ORDER BY views DESC;

CREATE OR REPLACE VIEW video_plays AS
SELECT video_id, COUNT(*) as plays, DATE(created_at) as date
FROM visit_logs WHERE type='video_play'
GROUP BY video_id, DATE(created_at) ORDER BY date DESC, plays DESC;

CREATE OR REPLACE VIEW certificates_issued AS
SELECT DATE(created_at) as date, COUNT(*) as count, student_name
FROM visit_logs WHERE type='certificate_issued'
GROUP BY DATE(created_at), student_name ORDER BY date DESC;
