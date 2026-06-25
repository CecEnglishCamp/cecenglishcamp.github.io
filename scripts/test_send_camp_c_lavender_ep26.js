#!/usr/bin/env node
/**
 * Lavender Course EP26 — 단일 테스트 발송 스크립트
 *
 * DRY_RUN=true (기본값): 실제 API 호출 없음, 이메일 내용 콘솔 출력만
 * DRY_RUN=false        : cecenglishcamp@gmail.com 에게만 실제 발송
 *
 * 실행:
 *   DRY_RUN 미리보기: node scripts/test_send_camp_c_lavender_ep26.js
 *   실제 발송:        $env:DRY_RUN="false"; $env:LIVE_SEND_CONFIRM="YES_SEND_LAVENDER_EP26_TEST"; node scripts/test_send_camp_c_lavender_ep26.js
 */

import { readFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';

// ─── .env 로더 (npm 없이 직접 파싱) ─────────────────────────────────────────
function loadEnv(envPath = resolve('.env')) {
  if (!existsSync(envPath)) return;
  for (const line of readFileSync(envPath, 'utf-8').split('\n')) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const i = t.indexOf('=');
    if (i < 0) continue;
    const key = t.slice(0, i).trim();
    const val = t.slice(i + 1).trim().replace(/^["']|["']$/g, '');
    if (!(key in process.env)) process.env[key] = val;
  }
}
loadEnv();

// ─── 설정 ────────────────────────────────────────────────────────────────────
const ALLOWED_RECIPIENT  = 'cecenglishcamp@gmail.com';
const REQUIRED_CONFIRM   = 'YES_SEND_LAVENDER_EP26_TEST';

const DRY_RUN            = process.env.DRY_RUN !== 'false';
const RESEND_API_KEY     = process.env.RESEND_API_KEY || '';
const EMAIL_FROM         = process.env.EMAIL_FROM     || 'onboarding@resend.dev';
const EMAIL_REPLY_TO     = process.env.EMAIL_REPLY_TO || ALLOWED_RECIPIENT;
const TEST_RECIPIENT     = (process.env.TEST_RECIPIENT || ALLOWED_RECIPIENT).trim().toLowerCase();
const LIVE_SEND_CONFIRM  = process.env.LIVE_SEND_CONFIRM || '';

// ─── 안전장치 1: 수신자 고정 ─────────────────────────────────────────────────
if (TEST_RECIPIENT !== ALLOWED_RECIPIENT) {
  console.error(`\n🚫 BLOCKED: TEST_RECIPIENT는 반드시 "${ALLOWED_RECIPIENT}" 이어야 합니다.`);
  console.error(`   현재 값: "${TEST_RECIPIENT}"`);
  process.exit(1);
}

// ─── 안전장치 2: 실제 발송 시 명시적 확인 코드 필수 ─────────────────────────
if (!DRY_RUN && LIVE_SEND_CONFIRM !== REQUIRED_CONFIRM) {
  console.error('\n🚫 BLOCKED: 실제 발송을 위해 LIVE_SEND_CONFIRM이 필요합니다.');
  console.error(`   현재 값: "${LIVE_SEND_CONFIRM}"`);
  console.error('   실제 발송 명령:');
  console.error(`   $env:DRY_RUN="false"; $env:LIVE_SEND_CONFIRM="${REQUIRED_CONFIRM}"; node scripts/test_send_camp_c_lavender_ep26.js`);
  process.exit(1);
}

// ─── 안전장치 3: 실제 발송 시 API Key 필수 ──────────────────────────────────
if (!DRY_RUN && !RESEND_API_KEY) {
  console.error('\n🚫 BLOCKED: DRY_RUN=false이지만 RESEND_API_KEY가 없습니다.');
  console.error('   .env 파일에 RESEND_API_KEY를 추가하세요.');
  process.exit(1);
}

if (!DRY_RUN && !RESEND_API_KEY.startsWith('re_')) {
  console.error('\n🚫 BLOCKED: RESEND_API_KEY 형식이 올바르지 않습니다. (re_ 로 시작해야 함)');
  process.exit(1);
}

// ─── 이메일 템플릿 로드 ──────────────────────────────────────────────────────
const __dir        = dirname(fileURLToPath(import.meta.url));
const templatePath = join(__dir, '../email-templates/camp-c/lavender-ep26.html');

if (!existsSync(templatePath)) {
  console.error(`\n🚫 BLOCKED: 이메일 템플릿이 없습니다.`);
  console.error(`   경로: ${templatePath}`);
  process.exit(1);
}

const htmlContent = readFileSync(templatePath, 'utf-8');

// ─── 이메일 페이로드 ─────────────────────────────────────────────────────────
const subject = '[Lavender Course EP26] CEC 영어캠프에서 라벤더 한 다발을 보내드립니다';

const emailPayload = {
  from:     EMAIL_FROM,
  to:       [TEST_RECIPIENT],
  reply_to: EMAIL_REPLY_TO,
  subject,
  html:     htmlContent,
};

// ─── DRY_RUN 모드 ────────────────────────────────────────────────────────────
if (DRY_RUN) {
  console.log('\n🔵 [DRY_RUN] 실제 발송 없음 — 이메일 페이로드 미리보기\n');
  console.log('━'.repeat(60));
  console.log(`MODE      : DRY_RUN (API 호출 없음)`);
  console.log(`FROM      : ${emailPayload.from}`);
  console.log(`TO        : ${emailPayload.to[0]}`);
  console.log(`REPLY-TO  : ${emailPayload.reply_to}`);
  console.log(`SUBJECT   : ${emailPayload.subject}`);
  console.log(`HTML 길이  : ${htmlContent.length.toLocaleString()} 자`);
  console.log(`템플릿 경로 : ${templatePath}`);
  console.log('━'.repeat(60));
  console.log('\n✅ DRY_RUN 완료. 실제 발송 명령:');
  console.log(`   $env:DRY_RUN="false"; $env:LIVE_SEND_CONFIRM="${REQUIRED_CONFIRM}"; node scripts/test_send_camp_c_lavender_ep26.js\n`);
  process.exit(0);
}

// ─── 실제 발송 ───────────────────────────────────────────────────────────────
console.log(`\n🟡 [LIVE] Resend API 호출 시작...`);
console.log(`   TO: ${TEST_RECIPIENT}`);

const response = await fetch('https://api.resend.com/emails', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${RESEND_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(emailPayload),
});

const result = await response.json();

if (response.ok) {
  console.log('\n✅ 발송 성공!');
  console.log(`   Resend 이메일 ID: ${result.id}`);
  console.log('\n📬 cecenglishcamp@gmail.com 받은편지함을 확인하세요.');
  console.log('   스팸 폴더도 확인해 주세요.\n');
} else {
  console.error('\n🚫 발송 실패:');
  console.error(JSON.stringify(result, null, 2));
  process.exit(1);
}
