# CEC Handover

## Start Here 히어로 제목 축소 + About/Start Here nav 초기 3회 반짝임 (최신)

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
