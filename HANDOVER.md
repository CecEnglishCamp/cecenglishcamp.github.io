# CEC Handover

## 사이트 전체 점검 후속 — 긴급 수정 2건: peter_rabbit_img1 게이트 복구 + nasa-space-camp nav 복구 (최신)

- **배경**: 직전 세션의 읽기 전용 전체 점검(수정 없음)에서 발견한 [치명] 항목 2건을 이번에 수정
- **1) `camp-a/speaking/peter_rabbit_img1.html`**: `isCecAdminUser()))return;`(닫는 괄호 1개 초과)로 인해 게이트 스크립트 전체가 `SyntaxError`로 죽어 로그인 없이 완전 열람 가능했던 문제. 괄호 1개 제거해 다른 41개 파일과 동일한 정상 구문으로 통일. 다른 41개 파일에는 이 오타가 없었음(이 파일 1개만의 국소 버그)
- **2) `nasa-space-camp/index.html`**: nav CSS를 전부 외부 `/assets/style.css`에만 의존했는데 그 파일이 **git 히스토리상 생성된 적이 없는 파일**(최초 제작 시점부터의 실수)이라 404 → nav가 `position:static`·높이 1493px(전체 페이지)로 렌더링되어 로고 이미지가 화면 전체를 뒤덮는 완전한 레이아웃 붕괴. `/assets/style.css` 참조 제거 후, 동일한 non-inner 드롭다운 마크업 구조를 쓰는 `index.html`의 nav CSS(nav·로고·드롭다운·햄버거·반응형 미디어쿼리 전체)를 그대로 이식해 복구
  - 참고로 발견했으나 이번 범위 밖이라 손대지 않은 것: 파일 맨 끝에 `</content>`라는 정체불명 잔여 태그(HTML 표준 아님, 브라우저가 무시해 렌더링엔 무해)
- 백업: 태그 `pre-urgentfix-20260718`(push 완료, 날짜 표기 1회 실수 후 정정) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-urgentfix-20260718\`
- 커밋: `866bf6dc2` "fix: syntax error breaking auth gate on peter_rabbit_img1, restore nasa-space-camp nav layout"
- 검증(Playwright, 라이브 https): `peter_rabbit_img1.html` — JS 에러 0건, 비로그인 접속 시 `mom-teacher/login.html?next=...`로 정상 리다이렉트(게이트 작동 확인). `nasa-space-camp/` — nav `position:fixed`·높이 68px 정상, 네트워크 에러 0건, 데스크톱 드롭다운 hover·모바일 햄버거 메뉴 전부 스크린샷으로 확인

## iPad safe-area 상단 여백 적용 (로드맵/Listen&Find/Picture Speaking 헤더)

- **배경**: iPad에서 상단 헤더(홈/목록/뒤로 버튼)가 상태바에 붙어 겹치거나 눌리기 힘든 문제. `lostwords/` scene은 `apple-mobile-web-app-status-bar-style: black-translucent` PWA 메타가 이미 있어 홈 화면 앱 모드에서 콘텐츠가 상태바 뒤까지 확장되는 것이 핵심 원인이었음
- **적용(85개 파일, 전부 +1/-1 균일)**:
  - `learning-roadmap/index.html`·`mission.html`: viewport에 `viewport-fit=cover` 추가. `roadmap.css`의 `.rm-topbar` → `padding: max(16px, env(safe-area-inset-top)) 0 0`
  - `lostwords/*.html` 40개(scene만, 랜딩 `index.html` 제외 — PWA 메타·fixed 헤더 없어 범위 밖): `.header`의 `height:54px`→`min-height:54px`, `padding:0 18px`→`padding: max(14px, env(safe-area-inset-top)) 18px 0`. viewport-fit=cover는 이미 전부 있었음
  - `camp-a/speaking/*.html` 42개(scene만, index류 8개·`wizard_of_oz_img1.html`은 다른 템플릿이라 제외): `.spk-nav`의 `height:52px`→`min-height:52px`, `padding:0 20px`→`padding: max(10px, env(safe-area-inset-top)) 20px 0`. viewport-fit=cover 신규 추가(원래 없었음)
- 백업: 태그 `pre-ipad-safearea-20260717`(push 완료) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-ipad-safearea-20260717\`(94개 파일 원본)
- 커밋: `2583a6093` "fix: iPad safe-area top padding on roadmap/lostwords/speaking headers, viewport-fit=cover, v4 cache"
- **⚠️ 검증 한계(구조적, 자동화로 넘을 수 없음)**: `env(safe-area-inset-top)`은 iOS/iPadOS Safari(WebKit) 전용 값이라 Chromium 기반 Playwright로는 실측 불가(항상 0으로 평가됨). `max(Xpx, env(...))` 로직이 최소 패딩을 보장하는 것과 iPad 4개 해상도(820×1180/1180×820/768×1024/1024×768) 스크린샷에서 레이아웃 안 깨지는 것까지만 코드·시각 레벨로 확인. **실제 iPad 실기기에서 상태바와의 최종 겹침 해소 여부는 Sung이 직접 확인 필요**
- 검증 중 발견(버그 아님): 좁은 세로 폭에서 "CEC Picture Speaking" 브랜드명이 2줄로 줄바꿈되는 현상 — `height→min-height` 전환으로 인한 자연스러운 결과(원래 고정 height였다면 텍스트가 잘렸을 것이 오히려 자동으로 커져 개선됨)
- 라이브 확인: `/learning-roadmap/`(viewport-fit=cover·roadmap.css?v=4), `/lostwords/ww_img1.html`, `/camp-a/speaking/wind_willows_img1.html` 3개 URL 전부 safe-area CSS 반영 확인

## Learning Roadmap: 전체 노출 + ready만 활성/pending 비활성(회색)

- **선행 사실 확인**: 직전 세션에서 지시받은 "pending 비활성화" 작업이 백업 태그(`pre-disable-pending-20260716`)만 생성되고 **실제 커밋은 안 된 상태**였음을 git log로 확인 후 이번에 실제 적용함(iPad에서 "준비 중"이 여전히 선명하게 보인다는 증상이 정확했음)
- **정확한 원인**: `roadmap.js`/`mission.js`의 pending 항목은 원래부터 클릭 핸들러·링크 자체가 없는 구조라 "클릭 차단"은 이미 충족돼 있었음. 진짜 문제는 `roadmap.css`의 `.is-blocked { opacity: 0.72 }`가 너무 높고 배지 색(진한 주황 `--pending`)을 그대로 둬서 시각적으로 "비활성화 안 된 것"처럼 보였던 것. 추가로 "들어가기" 버튼이 그 요일에 ready 항목이 전무해도 항상 활성화돼 있었고, mission.js에는 "오늘은 준비 중" 안내가 없었음
- **적용**:
  - `roadmap.css`: `.is-blocked` 항목 `opacity:0.5`+`grayscale(0.65)`, 배지를 회색조로 오버라이드. `.rm-enter.is-disabled` 신규(회색, `pointer-events:none`)
  - `roadmap.js`: 그 요일에 `status==='ready'`인 항목이 하나도 없으면 "들어가기"를 `href` 없는 `<span class="rm-enter is-disabled">준비 중</span>`으로 교체
  - `mission.js`: 오늘 요일에 ready 항목이 전무하면(Let's Go 버튼 자리에) "오늘은 준비 중입니다..." 안내 문구 추가
  - 주차 버튼(1~36)은 원래부터 잠금 로직이 없어 전부 노출·선택 가능 — 수정 불필요(요구사항 이미 충족)
  - `grade{3,4,5,6}.json`은 전혀 무수정(확인 완료), 표시/활성화 로직만 코드에서 처리 — **나중에 json의 status를 ready로만 바꾸면 코드 수정 없이 자동 활성화됨**
  - 캐시: `index.html`/`mission.html`의 `roadmap.js?v=2→v3`, `mission.js?v=2→v3`, `roadmap.css?v=2→v3`(CSS도 수정했으므로 함께 상향)
- 백업: 태그 `pre-disable-pending-20260717`(push 완료) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-disable-pending-20260717\learning-roadmap\`
- 커밋: `311b6aa58` "feat: roadmap pending items greyed/disabled, disabled enter button, mission empty-day notice, v3 cache"
- 검증(Playwright, iPad Pro 11 뷰포트, 라이브 https): Grade3 W02 — Reading1/Look&Speak/Reading2/Writing/Mom Teacher Review 전부 `opacity:0.5`·회색 배지("준비 중")·`is-blocked`, Camp A/Listen&Find는 `opacity:1`·초록 배지("수업 열기"). 목/토(ready 없음) "들어가기"→"준비 중" 비활성 정상 전환. Grade3 W01(전체 ready) pendingCount 0·disabledEnter 0(회귀 없음). W05~08·Grade4/5/6 W01도 로컬·라이브 결과 완전 일치. **홈 나갔다 재진입 후에도 Reading1이 여전히 회색·비활성 유지**(v3 캐시 정상, "준비 중" 선명 재발 없음)

## Mom Teacher 랜딩(index.html)에도 관리자 전체 커리큘럼 배너 추가

- **배경**: 관리자가 `trial-dashboard.html`에서는 전체 커리큘럼 배너를 보고 접근할 수 있게 됐지만(직전 세션), 랜딩(`mom-teacher/index.html`)에는 이 입구가 없어 관리자가 `/mom-teacher/curriculum/` 주소를 직접 쳐야 했음
- **적용**: `mom-teacher/index.html` 단 1개 파일, 순수 추가 26줄(삭제 0). `trial-dashboard.html`에서 검증된 패턴 그대로 재사용:
  - head에 `<script src="/assets/cec-admin-check.js">` 추가(이 페이지엔 원래 없었음)
  - 히어로 섹션 최상단(`.hero-badge` 바로 앞)에 `.admin-banner`("관리자 모드 — 전체 커리큘럼 바로가기", `/mom-teacher/curriculum/` 링크) 추가, 기본 `display:none`
  - body 하단 스크립트에서 `ensureAdminTrialSession()` 호출 후 `cec_mom_trial_session.admin===true`면 `document.body.classList.add('is-admin')` → CSS로 배너만 노출(다른 요소는 이 페이지에 트라이얼 제한 UI가 없어 숨길 대상 자체가 없음)
- 백업: 태그 `pre-momlanding-admin-20260716`(push 완료) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-momlanding-admin-20260716\`
- 커밋: `7b36f7c8f` "feat: admin curriculum shortcut banner on Mom Teacher landing (hidden for others)"
- 검증(Playwright, 로컬 정적서버 + 라이브 https 양쪽): 관리자 세션 → `is-admin` 부여·배너 노출·링크 `/mom-teacher/curriculum/` 정상. 일반 방문자 → `is-admin` 없음·배너 숨김·기존 `cta-group`/`hero-badge` 전부 정상(회귀 없음)
- **⚠️ 동일한 테스트 한계 재확인(버그 아님)**: 배너 클릭 후 `curriculum/` 실제 열람은 `require-auth.js`가 Supabase SDK로 세션을 서버 검증하기 때문에 가짜 토큰으로는 확인 불가 — 직전 trial-dashboard 작업 때와 같은 구조적 한계. 실제 회사 계정 로그인 상태에서의 최종 확인은 Sung이 직접 필요
- **[다음 큰 과제] Mom Teacher 트라이얼 인증 정식 이관**: localStorage 가짜 인증(비밀번호 base64 저장) + 리드가 Formspree로만 전송되는 구조 → Supabase Auth 기반으로 전면 교체 필요(계속 무수정, 기록만 유지)

## Mom Teacher 트라이얼 대시보드: 관리자 세션이면 전체 커리큘럼 안내로 전환

- **배경(런타임 실측으로 발견)**: 구글 로그인 후 관리자 Supabase 세션(`sb-rzlqlokqplhyntuirsmd-auth-token`, `user.email=cecenglishcamp@gmail.com`)이 정상 존재하는데도 `mom-teacher/trial-dashboard.html`이 여전히 "7일 체험(Peter Rabbit EP01~07만)" 화면을 보여줌
- **정확한 원인**: `cec-admin-check.js`의 `ensureAdminTrialSession()`은 실제로 정상 실행 중이었음(게이트 자체는 통과 — 그렇지 않았다면 애초에 이 페이지에 진입도 못했을 것). 이메일 파싱 경로(`user.email`, 정규식 `^sb-.*-auth-token$`, `toLowerCase().trim()`)도 실제 런타임 구조와 이미 일치해 수정 불필요. **진짜 원인은 페이지 콘텐츠(EP01~07 카드·체험 제한 안내·업그레이드 박스)가 전부 정적 HTML로 하드코딩되어 있어 "게이트 통과 여부"와 "콘텐츠 범위"가 애초에 연결되어 있지 않았던 것**
- **수정**: `mom-teacher/trial-dashboard.html` 단 1개 파일, 순수 추가 15줄(삭제 0). `cec-admin-check.js`가 관리자 세션에 대해 이미 생성해주는 `cec_mom_trial_session`의 `admin:true` 필드를 재사용 → `document.body.classList.add('is-admin')` → CSS로 체험 제한 안내(`.trial-note`)·업그레이드 박스(`.upgrade-box`)·무료체험 배지(`.lc-badge`/`.speak-badge`)를 숨기고, 새로 추가한 `.admin-banner`("관리자 모드 — 전체 커리큘럼 바로가기", `/mom-teacher/curriculum/` 링크)를 노출. 일반 트라이얼 사용자는 `admin` 필드가 없어 `is-admin` 클래스가 안 붙으므로 완전히 기존 그대로
- 백업: 태그 `pre-momadmin-fix-20260716`(push 완료) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-momadmin-fix-20260716\`
- 커밋: `5ab836689` "feat: admin sees full curriculum on Mom Teacher trial dashboard (trial UI intact for others)"
- 검증(Playwright): 로컬 정적서버 + 라이브 https 양쪽에서 관리자 세션(admin:true) → is-admin 부여·trial-note/upgrade-box/배지 전부 숨김(0개)·admin-banner 노출 확인. 일반 세션 → 완전 회귀 없음(배지 7개 그대로). 비로그인 → `login.html`로 정상 리다이렉트(회귀 없음)
- **⚠️ 검증 중 발견한 테스트 방법의 한계(버그 아님)**: 라이브에서 가짜 Supabase 토큰(`access_token:'dummy'`)으로 "전체 커리큘럼" 링크를 클릭하면 `require-auth.js`가 실제 Supabase SDK로 세션을 서버 검증하기 때문에 가짜 토큰은 통과 못하고 `login.html`로 리다이렉트됨(오히려 정상 — 가짜 토큰으로 결제 게이트를 우회할 수 없다는 뜻). `cec-admin-check.js`는 raw localStorage 파싱이라 가짜 토큰도 통과시키지만, `require-auth.js`는 SDK 레벨 검증이라 통과 못함 — 이 차이 때문에 진짜 계정 로그인 상태에서의 최종 E2E(curriculum/gradeX 결제 없이 열람)는 Sung이 직접 확인 필요
- **[다음 큰 과제] Mom Teacher 트라이얼 인증 정식 이관**: localStorage 가짜 인증(비밀번호 base64 저장) + 리드가 Formspree로만 전송되는 구조 → Supabase Auth 기반으로 전면 교체 필요(이번에도 무수정, 기록만 유지)

## Mom Teacher에 관리자 Google 로그인 추가 (유료 게이트 유지)

- **배경**: 회사 관리자(`cecenglishcamp@gmail.com`)는 Supabase에 Google(Social)로만 존재(비밀번호 없음). 본체 `/login.html`은 구글 로그인이 있지만, Mom Teacher는 자체 localStorage 트라이얼 로그인 흐름이라 구글 버튼이 없어 관리자가 진입할 방법이 없었음
- **조사 결과 — 게이트는 이미 관리자 Supabase 세션을 인식**(수정 불필요, 그대로 재사용):
  - `assets/cec-admin-check.js`의 `ensureAdminTrialSession()`이 localStorage의 `sb-*-auth-token`을 스캔해 관리자 이메일이면 `cec_mom_trial_session`을 자동 생성 → 트라이얼 콘텐츠(Peter Rabbit EP01~07 등) 게이트 통과
  - `assets/require-auth.js` line 56-59가 이미 관리자 이메일 early return으로 `mom-teacher/curriculum/`·`gradeX/epNN.html` 결제 게이트를 통과시킴
  - 즉 진짜 빠진 것은 "Supabase 세션을 만들 입구(구글 버튼)"뿐이었음
- **적용**: `mom-teacher/login.html` 단 1개 파일에 본체 `/login.html`과 동일한 "Google로 로그인" 버튼 + `supabase-js` 로드 + `signInWithOAuth('google', {redirectTo:'https://cecenglishcamp.com/login.html'})` 추가. 본체 login.html이 이미 `sessionStorage.cec_oauth_dest`를 읽어 임의 목적지로 이동시켜주는 구조라 별도 콜백 페이지 없이 연결. diff는 **순수 추가만(42줄, 삭제 0)** — 기존 이메일/비밀번호 트라이얼 폼(`cec_mom_users` 비교), `register.html`, 게이트 로직 전부 무수정
- 백업: 태그 `pre-momteacher-google-20260716`(push 완료) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-momteacher-google-20260716\`
- 커밋: `ccca15846` "feat: add Google login to Mom Teacher (admin entry, paid gate intact)"
- 검증(Playwright, 라이브 https): 구글 버튼 표시 확인, 클릭 시 `https://rzlqlokqplhyntuirsmd.supabase.co/auth/v1/authorize?provider=google&redirect_to=...login.html` 요청이 실제로 발생해 구글 로그인 페이지까지 정상 도달(네트워크 레벨로 확인). 기존 트라이얼 폼(틀린 계정 시 에러 정상 표시) 회귀 없음. 비로그인 상태에서 `mom-teacher/curriculum/`·`grade3/ep01.html` 전부 `login.html?next=...`로 정상 리다이렉트(유료 게이트 유지 확인)
- **⚠️ 미확인 항목(회사 구글 계정 자격증명 필요, 이번 세션에서 수행 불가)**: 실제 구글 계정으로 로그인 완료 후 curriculum/에피소드가 결제 없이 열리는지는 Sung이 직접 확인 필요(코드 로직상 통과해야 함이 확실하나 최종 E2E 확인 남음)
- **[다음 큰 과제] Mom Teacher 트라이얼 인증 정식 이관**: localStorage 가짜 인증(비밀번호 base64 저장) + 리드가 Formspree로만 전송되는 구조 → Supabase Auth 기반으로 전면 교체 필요(이번에도 무수정, 기록만 유지)

## 관리자 = 회사 이메일 1개(cecenglishcamp@gmail.com) 전 구간 통과 + Mom Teacher v14 + /legal/ 죽은링크 수정

- **관리자 화이트리스트 = 회사 이메일 1개로 통일**(`cecsungkim@gmail.com` 미포함, 정책 확정): `assets/require-auth.js`의 관리자 체크(line 56-59)는 이미 Lost Words·Space Camp·일반 콘텐츠 게이트 전부보다 앞선 early return 구조였음(로직 변경 없이 주석만 보강). `assets/cec-admin-check.js`(CEC_ADMIN_EMAILS)도 원래부터 회사 이메일 1개
- **`admin/index.html`은 `.gitignore`(41번째 줄)로 git 추적·라이브 배포 대상이 아님을 확인**(`/admin/` 라이브 404, `git show HEAD:admin/index.html` → 커밋 이력에 없음). 로컬 파일에서 `cecsungkim@gmail.com`을 제거해 회사 이메일 1개로 맞췄으나 이 변경은 git/배포에 영향 없는 로컬 전용 조치 — franchise-lead 내부 대시보드로 mom-teacher 게이트와 무관
- **Mom Teacher 게이팅 페이지 캐시 무효화**: `mom-teacher/curriculum/index.html` + `mom-teacher/grade{3,4,5,6}/epNN.html` 중 require-auth.js를 로드하는 113개를 `?v=11`→`?v=14`로 교체(사이트 전체 1330개 중 이 범위만, 나머지 1177개는 무접촉 — 전체 일괄 교체는 블라스트 반경이 너무 커 이번 범위에서 제외). **참고**: `mom-teacher/grade4/ep13~ep20.html`(8개)은 애초에 require-auth.js 자체를 로드하지 않는 별도 이슈 발견(무접촉, 다음 과제로만 기록)
- **죽은 링크 수정**: `/legal/privacy.html`→`/privacy.html`, `/legal/terms.html`→`/terms.html`을 `mom-teacher/index.html`(306-307)·`login.html`(95)·`register.html`(112,120-121) + grep으로 추가 발견한 `mom-teacher/trial-dashboard.html`(162)까지 총 4개 파일에서 교체. 리포 전체 `/legal/` 참조 0건 확인
- 백업: 태그 `pre-adminfix-20260716`(push 완료) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-adminfix-20260716\`(require-auth.js·cec-admin-check.js·admin/index.html·mom-teacher/index.html·login.html·register.html 원본)
- 커밋: `ec82070ca` "feat: company admin bypass (annotate early return), v14 mom-teacher gate, fix dead /legal links" (118개 파일)
- 검증: `gh run list` pages-build-deployment 성공. 라이브 재확인 — `/legal/` 참조 0건, `require-auth.js?v=14`(mom-teacher/curriculum, grade3/ep01 확인), require-auth.js 로직이 커밋 diff상 주석만 추가(결제/비로그인 게이트 회귀 없음, 코드 레벨로 확인), privacy/terms 200
- **⚠️ 미확인 항목(실브라우저 로그인 필요, 계정 자격 증명 없어 이번 세션에서 수행 불가)**: `cecenglishcamp@gmail.com`으로 실제 로그인해 camp-a·grammar-camp·mom-teacher/curriculum·lostwords·space-camp 5개 경로가 결제 무관하게 통과되는지는 Sung이 직접 확인 필요
- **[다음 과제] 캐시버스터 파편화**: `?v=` 번호가 리포 전체 1330개 파일에 하드코딩으로 흩어져 있음 → 공통 include/템플릿으로 스크립트 로드를 일원화하면 다음부터는 한 곳만 바꾸면 됨
- **[다음 과제] Mom Teacher 트라이얼 인증 교체**: localStorage 가짜 인증(비밀번호 base64 저장) + 리드가 Formspree로만 전송되는 구조 → Supabase Auth 기반으로 전면 교체 필요(이번 세션 무수정, 기록만)
- **[다음 과제] grade4 ep13~20 require-auth 누락**: 8개 파일이 애초에 게이트 스크립트 자체를 로드하지 않음 — 별도 확인/수정 필요

## G6 A Little Princess: grade6.json 신설 + W01 단일지문 Reading/Writing + Listen&Find 승격·연결·랜딩 활성화

- `learning-roadmap/manifests/grade6.json` 신규 생성(36주 골격, G6 커리큘럼: A Little Princess(W01~08)·Five Children and It·The Jungle Book·Pinocchio·The Princess and the Goblin·Eight Cousins·Little Men). W01만 Reading/Writing `ready`, 나머지 주차는 전부 `pending` 유지(무접촉)
- G6 W01 A Little Princess Reading1/2(**단일 지문, 난이도 토글 없음** — G3~G5와 달리 이 학년은 토글 자체가 없는 설계, 라이브 확인 결과 `.tg` 토글 버튼 0개·`p-standard` 지문 1개만 렌더링) + Writing(자유작문 4단계: 빈칸채우기→나의글쓰기→ChatGPT 제출→다시쓰기) 배치
- `lostwords-wip/lp_img1~8.html` + `lesson_lp_img1~8.json`(16개) → `/lostwords/`로 git mv 승격. require-auth `?v=13`·noindex 이미 적용된 상태였음(버전 통일 불필요, 이전 책들과 달리 처음부터 최신). 고아 파일 `lostwords-wip/lp_index.html`(어디서도 참조 안 됨, 이전 G5 `ti_index.html`과 동일 전례로 삭제) 정리. 8개 scene에 Peter Rabbit/Treasure Island와 동일한 `.header-right`/`.header-nav-link` 패턴으로 "← Listen & Find 목록"/"홈" 나가는 링크 추가(파일당 diff +8/-1로 균일)
- G6 grade6.json W01~08 화요일 Listen&Find(`/lostwords/lp_img1~8.html`)·Look&Speak(`/camp-a/speaking/little_princess_img1~8.html`, 사전 존재 확인 후 연결) 연결(status ready), W09(Five Children and It)부터는 pending 유지
- `lostwords/index.html` 랜딩 A Little Princess 카드 "준비 중" 배지 해제 → 다른 4권과 동일한 `<a class="card">` 패턴으로 활성화. **이로써 Listen & Find 랜딩 5권(Peter Rabbit·Red Riding Hood·Wind in the Willows·Treasure Island·A Little Princess) 전부 프로덕션 승격 완료, "준비 중" 0건**
- 변경 전 `grade6.json.bak` 로컬 백업(커밋 대상 아님)
- 커밋: `843d93f80` "feat: G6 A Little Princess — grade6.json + W01 single-passage Reading/Writing, promote Listen&Find, link W01-08, activate landing"
- 백업: 태그 `pre-g6-20260716`(push 완료) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-g6-20260716\lostwords-wip\`(lp_ 16개 원본)
- 검증: `gh run list` pages-build-deployment 성공. 라이브 재확인 — `/learning-roadmap/?grade=6&week=01`·`/lostwords/lp_img1.html` 200, `/lostwords/` 랜딩 "준비 중" 0건, grade6.json W01 월/화/목 전부 실제 경로로 응답, lp_img1~8·little_princess_img1~8 16개 전부 200, 나가는 링크·require-auth v13·noindex 라이브 확인 완료

## Start Here 히어로 fold 재설계 + Free Learning 출구 교체 + 비초등 안내 강화 + 우클릭 방지

- **히어로 구조 분리(핵심 변경)**: 기존 `.hero`(단일 flex-center 박스에 kicker+h1+lead+mantra+stats 전부 포함, `min-height:78vh`)는 실측 결과 이미 뷰포트보다 짧아(예: 1440×900에서 실제 높이 702px) **다음 섹션이 로드 시 이미 보이는 상태**였음. 지시받은 대로 min-height를 64~68vh로 더 줄이면 오히려 다음 섹션이 더 잘 보이는 역효과가 실측으로 확인되어, `.hero-titleblock`(kicker+h1+lead, `min-height:calc(100vh - 64px)`, 세로 중앙정렬)과 `.hero-below`(mantra+stats, 일반 문서 흐름)로 마크업을 분리하는 방식으로 목표(제목만 첫 화면에 노출, stats·다음 섹션 미노출)를 달성. 모바일(≤640px)은 `.hero-titleblock{min-height:88vh}`로 별도 조정(80vh 테스트 중 414×896 폭에서 stats가 43px 정도 살짝 보여 88vh로 올려 안전마진 확보)
  - Playwright로 데스크톱(1440×900, 1920×1080)·랩탑(1366×768)·모바일(414×896, 375×812, 320×568) 6개 뷰포트 + 라이브 서버(1440×900, 414×896) 실측: 제목 100% 노출, stats/다음 섹션 전부 미노출, 가로 스크롤 없음 확인
- **Free Learning 출구 교체**: "Explore Freely" 버튼 `href="/camp-a/"` → `href="#choose-camp"`로 변경(비초등 학생이 Camp A로 잘못 유입되지 않도록), Step 1 섹션에 `id="choose-camp"` 부여. 클릭 시 정상 스크롤 확인(로컬 3457px, 라이브 hash 확인)
- **비-초등 안내 강화**: Step 1 h2 아래 `👉 먼저 나이에 맞는 캠프를 고르세요.`(초록 강조 배지 문구) 추가. 카드 4개 대상 표기(초등학생/중·고등학생/성인·학부모/엄마가 선생님)는 기존에 이미 명확해 문구·href 무수정
- **우클릭 방지(start-here.html 한정)**: `</body>` 직전에 `contextmenu` 이벤트만 `preventDefault()`하는 스크립트 추가. `user-select`/`selectstart`/`copy` 차단은 넣지 않아 텍스트 선택·복사·모바일 길게 누르기는 그대로 유지(Playwright로 `getSelection()` 정상 동작 확인, `user-select` computed 값 `auto` 확인)
- 백업: `E:\CEC CAMP STORAGE\CEC-Backup\backup-starthere-20260716\start-here.html` 최신본으로 갱신 복사(태그는 기존 `pre-starthere-20260716` 재사용)
- 커밋: `e79c44df4` "fix: shorten hero, route Free Learning to camp picker, non-elementary paths + disable right-click" (start-here.html 단일 파일, index.html 무수정)
- 검증: `gh run list` pages-build-deployment 성공 확인. 라이브 재확인 — fold 실측(위 수치), contextmenu preventDefault + 텍스트 선택 정상, Explore Freely→`#choose-camp` 스크롤 정상, Step1 카드 4개 href 무결
- **⚠️ 미완료 항목(참고)**: "실제 스마트폰으로 직접 열어 길게 누르기 확인"은 이 세션에서 물리 기기 접근이 없어 수행하지 못함 — iPhone 13 프로필 Playwright 터치 에뮬레이션 + 라이브 서버 대상 contextmenu/selection 검증으로 대체함. 실기기에서 길게 누르기 시 메뉴가 실제로 안 뜨는지는 사용자가 직접 폰으로 한 번 확인 권장

## Start Here 히어로 제목 축소 + About/Start Here nav 초기 3회 반짝임

- `start-here.html` 히어로 제목 한 단계 축소: `.hero h1` font-size `clamp(52px,8.8vw,104px)`→`clamp(40px,7.5vw,84px)`, `.hero .lead` `clamp(18px,2.2vw,24px)`→`clamp(16px,2vw,21px)`. mantra·stats 등 나머지 무수정.
- 공통 nav의 About 드롭다운에 "로드 후 3회만 반짝이고 멈춤" 연출 추가: `@keyframes cecBlink`(opacity 1↔.35) + `.cec-flash`/`.cec-flash-cyan`(`animation:cecBlink 0.7s ease-in-out 3` — iteration-count 3 고정, 무한 반복 아님) + `@media (prefers-reduced-motion: reduce)`로 애니메이션 차단. 지난 세션에서 About 드롭다운을 적용한 동일 17개 파일에 각각 `<style>` 1블록(공통 `<nav>` 태그 직전 삽입) + About 토글에 `cec-flash`, 드롭다운 안 "Start Here" 항목에 `cec-flash-cyan`(기존 시안 강조 유지) 클래스 부여. 파일당 diff는 정확히 +10/-2(스타일 블록 6줄 + 클래스 부여 2곳)로 균일.
- 커밋: `a67cee018` "style: reduce Start Here hero title, add initial 3x flash to About/Start Here nav"
- 검증: Playwright headless로 실측 —
  - 375px/414px 뷰포트에서 `document.documentElement.scrollWidth === clientWidth`(가로 스크롤 없음), 히어로 h1 `scrollWidth`가 box `width`와 동일(줄바꿈 넘침 없음), `.stats`(2열)·`.five/.steps-grid/.ways`(1열)·`.week`(2열) grid-template-columns 정상 접힘 확인
  - `getComputedStyle`로 `.cec-flash`/`.cec-flash-cyan`의 `animation-iteration-count: 3`, `animation-duration: 0.7s` 확인(무한 반복 아님)
  - `page.emulateMedia({reducedMotion:'reduce'})` 상태에서 `animation-name: none` 확인(접근성 정상 차단)
  - 모바일 hamburger 메뉴 오픈 시 About/Camps 등 항목 정상 노출(기존 사이트 전반의 hover-only 드롭다운은 터치 기기에서 서브메뉴가 탭으로 안 열리는 pre-existing 한계이며 오늘 변경과 무관 — 별도 이슈로 인지만 해둠, 이번 작업 범위 아님)
  - 라이브 재확인: `/start-here.html` clamp 값, `/about.html` CSS 블록·class 부여 전부 raw HTML로 확인

## Start Here 페이지 신설 + About 드롭다운(Start Here 먼저·시안 강조)

- `/start-here.html` 신규 생성(Sung 완성본 그린 톤 그대로 사용). 데스크톱 원본 대비 변경한 것은 딱 두 가지: (1) `noindex` 메타 제거(첫 진입 페이지라 색인 허용) (2) 임시 상단 링크(`.top` 블록)를 사이트 공통 `<nav>`(About 드롭다운 포함)로 교체하고 `</body>` 앞에 공통 `<footer>` 삽입 — 본문/디자인은 무수정
- **`/#camps` 앵커 이슈 발견 및 해결**: 홈(index.html)에는 Camp A/B/C를 고르는 카드 섹션 자체가 없어(히어로+nav+footer+플로팅 CTA뿐) Start Here 원본의 `/#camps` 링크 5곳이 전부 무효 앵커였음. Sung 결정에 따라 각 카드를 해당 캠프로 직접 연결(Camp A→`/camp-a/`, Camp B→`/camp-b/`, Camp C→`/camp-c/`, Mom Teacher→`/mom-teacher/`, "Explore Freely"→`/camp-a/`). index.html은 무수정.
- **About 메뉴 → 드롭다운 전환**: 공통 nav에 About 단일 링크가 있는 파일 22개 중, Camps/Courses 드롭다운 마크업·CSS를 실제로 갖춘 17개 파일에만 적용(about.html, account-help.html, index.html, index_black.html, index_space.html, camp-a/b/c/c2, franchise, essay-camp, grammar-camp, young-days, speaking, payment, mom-teacher/curriculum, nasa-space-camp). 각 파일이 기존에 쓰던 `-inner` wrapper 유무 패턴을 그대로 따라 삽입(about/account-help/franchise/payment는 `-inner` 있음, 나머지 13개는 없음). 항목 순서: **Start Here**(위, `color:#00f2ff;font-weight:700`로 강조) → **About CEC**(아래, 기본색). 파일당 diff는 About `<li>` 한 줄 → 드롭다운 블록 교체분만.
  - **범위 제외**(다음 세션 참고): `mom-teacher/index.html`은 드롭다운 CSS/마크업 자체가 없는 별도 심플 nav라 무수정 유지. `404.html·trial.html·terms.html·privacy.html·prestep.html`은 About이 footer 링크이거나 독립 버튼이라 nav 드롭다운 대상이 아니라 무수정.
- 백업: 태그 `pre-starthere-20260716`(push 완료) + `E:\CEC CAMP STORAGE\CEC-Backup\backup-starthere-20260716\`(수정 대상 17개 파일 원본, 리포 상대경로 유지)
- 커밋: `9d968d723` "feat: add Start Here guide + About dropdown (Start Here first, cyan highlight)"
- 검증: `gh run list` pages-build-deployment 성공 확인. 라이브 `https://cecenglishcamp.com/start-here.html`(noindex 없음, nav/footer 정상, Camp 카드 4개 각 캠프 페이지 연결, Explore Freely→camp-a, Roadmap/Start Your Journey→learning-roadmap 정상), `/about.html`·`/`(About 드롭다운: 위 Start Here 시안 강조 `color:#00f2ff;font-weight:700`, 아래 About CEC 기본색) 전부 raw HTML로 재확인 완료

## G5 Treasure Island: 매니페스트 신설 + W01 배치 + Listen&Find/Look&Speak 승격·연결(3단계 Reading) + G4 표기 수정

- `learning-roadmap/manifests/grade5.json` 신규 생성(36주, G5 커리큘럼 5권: Treasure Island(W01~09)·The Jungle Book·The Call of the Wild·Around the World in 80 Days·Anne of Green Gables)
- G5 W01 Treasure Island Reading1/2(**쉬운 글/기본 글/도전 글 3단계 토글**, G3/G4의 2단계보다 한 단계 더) + Writing 배치
- **G4 표기 버그 수정**: G4 W01 Reading1/2·Writing 페이지가 이전에 "Grade 3"로 잘못 표기되던 것을 "Grade 4"로 정정(라이브 확인 완료)
- `lostwords-wip/ti_img1~8.html` + `lesson_ti_img1~8.json`(16개) → `/lostwords/` 승격(require-auth v13 이미 적용 상태 확인), 고아 상태였던 `ti_index.html`도 정리. 8개 scene에 Peter Rabbit과 동일한 나가는 링크 추가.
- G5 grade5.json W01~08 화요일 Listen&Find(`ti_img1~8`)·Look&Speak(`treasure_island_img1~8`) 연결(ready), W09는 scene이 8개뿐이라 pending 유지
- `lostwords/index.html` 랜딩 Treasure Island 카드 활성화(A Little Princess만 "준비 중")
- 커밋: `a39e470b7`(grade5.json+G5 W01+G4 표기수정), `973e2ad91`(승격+연결+랜딩+nav), `8e7a2740b`(누락된 스테이징 삭제 반영 후속 수정)
- **⚠️ 작업 중 발견한 실수(투명 공개)**: 두 번째 커밋을 경로 지정(`git commit -- <path>...`)으로 나눠 커밋하는 과정에서 옛 `lostwords-wip/ti_img*.html` 경로의 **삭제분을 pathspec에 빠뜨려**, 약 7~10분간 `/lostwords/ti_img1.html`과 `/lostwords-wip/ti_img1.html`이 동시에 라이브 상태였음(중복 콘텐츠). 발견 즉시 세 번째 커밋(`8e7a2740b`)으로 누락된 삭제를 반영해 push, 현재는 `/lostwords-wip/ti_img1.html` 404 확인됨. **교훈: 앞으로 rename(이동) 파일이 포함된 작업을 경로 지정 커밋으로 나눌 때는 옛 경로도 pathspec에 반드시 포함할 것.**
- 검증: Grade 5 탭·W01 전체 확인, Reading1 3단계 토글(쉬운/기본/도전) 정상, W01~08 Listen&Find·Look&Speak 전부 "열기 ↗" 정상(W09는 pending 유지 확인), scene "목록" 클릭 시 정상 복귀, 비로그인 차단 정상, G4 Wind 페이지 "Grade 4" 표기 확인

## G4 Wind in the Willows: 매니페스트 신설 + W01 배치 + Listen&Find/Look&Speak 승격·연결

- `learning-roadmap/manifests/grade4.json` 신규 생성(36주, G4 커리큘럼 9권: Wind in the Willows·Wizard of Oz·Secret Garden·Tom Sawyer·Railway Children·Black Beauty·Pollyanna·Alice in Wonderland·A Christmas Carol)
- G4 W01 Wind in the Willows Reading1/2 + Writing 배치(W01과 동일 레벨), grade4.json W01 monday/wednesday reading·thursday writing → ready
- `lostwords-wip/ww_img1~8.html` + `lesson_ww_img1~8.json`(16개) → `/lostwords/`로 승격. **발견/수정**: ww_img 8개가 require-auth.js `?v=11`에 머물러 있던 것을 나머지와 동일하게 `?v=13`으로 정정(로직은 공유 파일이라 이미 적용되지만 캐시 방지 목적)
- G4 grade4.json W01~04 화요일 Listen&Find(`/lostwords/ww_img1~4.html`)·Look&Speak(`/camp-a/speaking/wind_willows_img1~4.html`) 연결(status ready), W05(Wizard of Oz, 미완성) 이후 무접촉
- `lostwords/index.html` 랜딩 Wind in the Willows 카드 활성화(Treasure Island·A Little Princess 2권은 계속 "준비 중")
- Peter Rabbit·Red Riding Hood와 동일한 `.header-right` 패턴으로 8개 scene에 나가는 링크 추가
- 커밋: `55d791b41`(grade4.json+W01자료), `fc1ce7fda`(승격+연결+랜딩+scene nav)
- 검증: W01~04 Listen&Find·Look&Speak 전부 "열기 ↗"(새 탭) 정상 / scene "목록" 클릭 시 `/lostwords/` 복귀(갇힘 없음) / 비로그인 `/login.html` 차단 정상 / noindex 유지 / 랜딩 카드 상태 정상(Grade 4 탭도 정상 작동 확인)

## G3 W06-08 Red Riding Hood Reading 1/2 + Writing 배치·연결

- W06~08 각 주 Reading1/2 + Writing 총 9개 파일 신규 생성(`library/camp-a-readings/grade3/red-riding-hood/w0{6,7,8}_r{1,2}.html`, `camp-a/writing/grade3/red-riding-hood/w0{6,7,8}.html`)
- grade3.json W06·W07·W08 monday reading / wednesday reading / thursday writing → ready 패치(정확히 9건)
- 커밋: `96e92ab2c` "feat: G3 W06-08 Red Riding Hood Reading 1/2 + Writing (G3 level)"
- 검증: W06 Reading1·W07 Reading2 열기→토글/정답보기 정상, W08 Writing Step2·4 저장·Step3 복사 정상
- **W05~08 네 주 전체(월~금, Listen&Find·Look&Speak 포함) 실측 결과 pending 항목 0건 — Red Riding Hood 4주 완비**

## G3 W05 Red Riding Hood Reading 1/2 + Writing 배치·연결

- `library/camp-a-readings/grade3/red-riding-hood/w05_r1.html`, `w05_r2.html`, `camp-a/writing/grade3/red-riding-hood/w05.html` 신규 생성(W01과 동일 레벨/템플릿)
- grade3.json W05 monday reading / wednesday reading / thursday writing → status pending→ready 패치(정확히 3건)
- 커밋: `de39be94d` "feat: G3 W05 Red Riding Hood Reading 1/2 + Writing (same level as W01)"
- 검증: Reading 1 열기→돌아가기 자동완료(✓) 정상 / 쉬운글·기본글 토글·정답보기 정상 / Writing Step2·4 새로고침 후 유지·Step3 복사 정상 / **W05 한 주 전체(월~금) 이제 전부 열림 확인**(더 이상 pending 항목 없음)
- 이로써 G3 Week01, Week05 두 주가 Camp A+Reading+Writing+Listen&Find+Look&Speak 전 항목 ready 상태로 완비됨

## Red Riding Hood /lostwords/ 승격 + G3 W05-08 연결

- `lostwords-wip/red_riding_hood_img1~9.html` + `lesson_rrh_img1~9.json`(18개) 전부 `/lostwords/`로 승격(보관 목적, 9개 전량 이동). noindex·require-auth v13 전부 유지 확인, 상대경로 정상.
- G3 grade3.json W05~08 화요일 연결(status: ready) — 완성된 것만 연결, 나머지 주차는 무접촉:
  - Listen & Find: W05→rrh_img1, W06→img2, W07→img3, W08→img4
  - Look & Speak: W05→camp-a/speaking/red_riding_hood_img10, W06→img11, W07→img12, W08→img13
  - 변경 전 `grade3.json.bak` 로컬 백업(커밋 대상 아님)
- `lostwords/index.html` 랜딩에서 Red Riding Hood 카드 활성화(Wind in the Willows·Treasure Island·A Little Princess 3권은 계속 "준비 중")
- Peter Rabbit과 동일한 `.header-right` 패턴으로 9개 scene에 "← Listen & Find 목록"/"홈" 나가는 링크 추가
- 커밋: `d7847c622` "feat: promote Red Riding Hood Listen&Find, link G3 W05-08, activate landing, add scene nav"
- 검증: W05~08 미션 Listen&Find·Look&Speak 전부 "열기 ↗"(새 탭) 정상 매칭 / scene "목록" 클릭 시 `/lostwords/` 복귀(갇힘 없음) / 비로그인 시 `/login.html` 차단 정상 / 랜딩 카드 상태 정상
- **재고 조사 결과 참고**: Jack and the Beanstalk·Frog Prince·Elves and the Shoemaker·Thumbelina·Emperor's New Clothes·Lucky Hans·Velveteen Rabbit(G3 W09~36)은 Listen & Find·Look & Speak 자료가 전혀 없음 — 이후 자료 제작 전까지 pending 유지가 정답. Little Princess(G6)·Treasure Island(G5)·Wind in the Willows(G4)는 완성돼 있으나 grade4/5/6.json 자체가 아직 없어 미연결 상태.

## Listen & Find 랜딩 + scene 나가는 길 + 메뉴 분리

- `lostwords/index.html` 신규 생성 — Listen & Find 전체 랜딩(G3 Peter Rabbit 활성, G3 Red Riding Hood·G4 Wind in the Willows·G5 Treasure Island·G6 A Little Princess는 "준비 중" 표시). noindex 없음(랜딩 1개는 검색 노출 허용, DEPLOY_NOTES §5 정책과 일치)
- `lostwords/peter_rabbit_img1.html`~`img7.html` 7개에 상단 헤더 우측에 "← Listen & Find 목록"(→`/lostwords/`) + "홈"(→`/`) 링크 추가 — 학습 로직/게이팅(require-auth v13)/noindex는 무수정, 헤더 우측에 링크만 추가(step-badge를 새 wrapper로 감싸 배치)
- 상단 메뉴 "Speaking" → "Listen & Find"(`/lostwords/`) + "Look & Speak"(`/speaking/`) 2줄로 분리, 18개 파일 전부 반영(모던 드롭다운 15개, `speaking/index.html`의 active-class 케이스 1개, 레거시 flat-`<li>` 구조 2개(`grammar/`, `about/index.html`) 각각 패턴에 맞게 처리)
- 커밋: `d1b1027f5` "feat: Listen & Find landing + scene nav links + split menu (Listen&Find / Look&Speak)"
- 백업: 태그 `pre-listenfind-menu-20260715` + 물리백업 `E:\CEC CAMP STORAGE\CEC-Backup\backup-listenfind-20260715\`(25개 파일, 원본 그대로 복사)
- 검증: 홈 nav에 두 링크 모두 노출 / `/lostwords/` 랜딩→Peter Rabbit 카드→img1 진입→"목록" 클릭 시 `/lostwords/`로 정상 복귀(갇힘 없음) / 비로그인 시 여전히 `/login.html`로 차단 / 로드맵 화요일 미션 "열기 ↗"(새 탭) 그대로 정상

## 로드맵 스크립트 4시간 엣지캐시 수정

- 증상: 화요일 Listen & Find가 강력 새로고침하면 ready로 보이지만, 홈으로 나갔다 재방문하면 다시 "준비 중"으로 보임
- 원인: `roadmap.js`/`mission.js`가 Cloudflare 엣지에 `Cache-Control: max-age=14400`(4시간)으로 캐시되어 옛 스크립트 파일이 서빙됨(`grade3.json`은 항상 정상이었음 — 스크립트 파일 자체가 문제)
- 조치: `learning-roadmap/index.html`·`mission.html`의 `roadmap.css`/`roadmap.js`/`mission.js` 호출부에 `?v=2` 버전 파라미터 추가(`require-auth.js?v=13`과 동일 패턴). JS/CSS 파일 내용 자체는 무수정.
  - 커밋: `eda181443` "fix: version-bust roadmap css/js to defeat 4h edge cache"
- **이후 규칙: roadmap.js/mission.js/roadmap.css를 고칠 때마다 index.html·mission.html의 `?v=` 숫자를 반드시 올릴 것(v2→v3…)** — 안 올리면 이번과 같은 4시간 캐시 문제 재발.
- 검증: 실브라우저로 홈→로드맵 재진입을 W01~04 각각 5회 반복, 전부 "수업 열기" 유지 확인(재발 없음). 요청 로그로 `roadmap.js?v=2` 정상 호출 확인.

## Peter Rabbit Listen & Find → `/lostwords/` 프로덕션 승격 완료

- `lostwords-wip/`의 Peter Rabbit img1~7(HTML 7 + lesson JSON 7)을 `/lostwords/`로 정식 승격
- G3 W01~04 화요일 Listen & Find를 `grade3.json`에 연결(status: ready)
  - W01→img1, W02→img2, W03→img3, W04→img4 (W05 이후 Red Riding Hood 등은 pending 유지, 무접촉)
- img5~7은 `/lostwords/`에 보관만 되어 있고 아직 어떤 Week에도 연결되지 않음(향후 재사용 대기)
- 스테이징 정리: `lostwords-wip/peter_rabbit_*` 원본 삭제 완료(구버전 `_before_apiclean.html` 포함), 사이트 내부에 `/lostwords-wip/`로 거는 잔존 링크 없음 확인(단, 세션 작업용 pilot 파일 `camp-a/grade3/week01a_connect_pilot.html`의 참조 링크는 `/lostwords/`로 함께 갱신)
- 커밋: `aa593c5bc` "feat: promote Peter Rabbit Listen & Find to /lostwords/, link G3 W01-04 Tue"

### 함께 발견·수정한 이슈: require-auth.js 게이트 공백

- 승격 작업 도중 `assets/require-auth.js`의 `isLostWords` 판별이 `/lostwords-wip/` 경로만 확인하고 있어, 새 프로덕션 경로 `/lostwords/`는 게이트가 적용되지 않는 것을 실측으로 확인
- `isLostWords`가 `/lostwords-wip/` 또는 `/lostwords/` 둘 다 인식하도록 수정, 캐시된 구버전 스크립트가 남아있을 경우를 대비해 `?v=12 → v=13`으로 버전 상승(적용된 27개 lostwords-wip HTML도 함께 v13으로 갱신)
- 라이브 검증(JWT 목킹): 비로그인→로그인 페이지, 로그인+미결제→`/payment/`, 활성 구독자→정상 통과 전부 확인. 기존 `/lostwords-wip/`·Camp A 회귀 없음 확인.

### 기능 확인 결과
- W01~04 화요일 미션에서 Listen & Find "열기 ↗"(새 탭, target=_blank)가 각 주 img1~4에 정확히 매칭됨
- `/lostwords/peter_rabbit_img1.html`에 noindex 유지 확인
- `/lostwords-wip/peter_rabbit_img1.html` 접근 시 404(정리 완료) 확인
