# CEC Handover

## G3 W06-08 Red Riding Hood Reading 1/2 + Writing 배치·연결 (최신)

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
