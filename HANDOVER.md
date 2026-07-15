# CEC Handover

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
