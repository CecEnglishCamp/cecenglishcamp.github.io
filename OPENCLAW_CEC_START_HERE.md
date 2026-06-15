# 🦞 OPENCLAW — CEC 작업 시작 전 확인 사항

> **이 파일을 가장 먼저 읽으세요.**
> CEC English Camp GitHub Pages 작업을 위해 OpenClaw에서 이 리포지토리를 열었는지 확인합니다.

---

## ✅ 작업 전 체크리스트

### 1. 올바른 폴더인지 확인
```
pwd
```
결과가 아래와 **같아야 합니다**:
```
C:\Users\cecsu\cecenglishcamp.github.io
```
다른 폴더면 즉시 이동:
```
cd C:\Users\cecsu\cecenglishcamp.github.io
```

### 2. Git 상태 확인
```
git status
git log -3 --oneline
```

### 3. 최신 상태로 유지
- 작업 전 `git pull`로 origin과 동기화
- commit 전 `git diff --stat`로 변경 파일 확인
- commit 메시지는 영어로, 간결하고 명확하게

### 4. 작업 후 기본 흐름
```
git add <files>
git commit -m "commit message"
git push
```

---

## ⚠️ 규칙

| 항목 | 내용 |
|------|------|
| **Commit 메시지** | 영어, 간결, 명확 (예: `Add three CEC Blog articles for dental and kids English`) |
| **Push** | commit 후 반드시 push (단, 선생님이 보류 요청 시 제외) |
| **본인 작업** | `C:\cec-agent`는 OpenClaw 워크스페이스, 여기는 GitHub Pages 리포지토리 — 혼동 금지 |
| **삭제/수정** | 승인 없이 파일 삭제나 대규모 수정 금지 |

---

## 📂 주요 디렉토리

```
blog/        — 블로그 포스트 (HTML)
assets/      — 이미지, CSS, JS
```

---

*최초 작성: 2026-06-15*
