/* =========================================
File: js/game.js
(Fixed: screen toggle, Q counter, battery gain, retries, goHome, gif path)
========================================= */
console.log("✅ game.js loaded successfully!");

let currentLevel = "A1";
let currentQuestion = 0;
let battery = 3;
let answered = false;

let questions = [];
let missionStates = [];

const START_BATTERY = 3;

/* ======== 예시 문제셋 (원본 유지 + 필요시 추가) ======== */
const questionsA1 = [
  { title: "Simple Present", text: "I ___ to school every day.", options: ["goes", "go", "going"], correct: 1 },
];
const questionsA2 = [
  { title: "Past Continuous", text: "I ___ when he called.", options: ["sleep", "was sleeping", "slept"], correct: 1 },
];
const questionsB1 = [
  { title: "Complex Sentence", text: "Although tired, she ___.", options: ["continue", "continued", "continues"], correct: 1 },
];
const questionsB2 = [
  { title: "Mixed Conditional", text: "Had I known, I ___ you.", options: ["would contact", "would have contacted", "will contact"], correct: 1 },
];

function byId(id) {
  return document.getElementById(id);
}

function clamp(n, min, max) {
  return Math.max(min, Math.min(max, n));
}

function setBattery(value) {
  battery = clamp(value, 0, 100);
  updateRobot();
}

function getLevelQuestions(level) {
  if (level === "A1") return questionsA1;
  if (level === "A2") return questionsA2;
  if (level === "B1") return questionsB1;
  return questionsB2;
}

function getRobotImageForLevel(level) {
  return (level === "B1" || level === "B2") ? "./assets/img/robo_jump.png" : "./assets/img/robo2.png";
}

function speak(text) {
  if (!("speechSynthesis" in window)) return;
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = "ko-KR";
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utter);
}

/* ======== 게임 시작 ======== */
function startGame(level) {
  currentLevel = level;
  currentQuestion = 0;
  answered = false;

  questions = getLevelQuestions(level);
  if (!questions || questions.length === 0) {
    console.error("❌ questions is empty for level:", level);
    return;
  }

  missionStates = questions.map((_, i) => ({
    id: i,
    completed: false,
    triedOnce: false,
    usedBaseCamp: false,
  }));

  const levelScreen = byId("levelScreen");
  const gameScreen = byId("gameScreen");
  const questionBox = byId("questionBox");
  const completionScreen = byId("completionScreen");

  if (!levelScreen || !gameScreen || !questionBox || !completionScreen) {
    console.error("❌ 필수 DOM 요소를 찾지 못했습니다. (id 확인 필요)");
    return;
  }

  // ✅ 핵심: inline style="display:none" 깨기
  levelScreen.style.display = "none";
  gameScreen.style.display = "block";
  gameScreen.classList.add("active");

  questionBox.style.display = "block";
  completionScreen.classList.remove("show");

  const robotImg = byId("robotImg");
  const robotGif = byId("robotGif");
  const robotContainer = byId("robotContainer");

  if (!robotImg || !robotGif || !robotContainer) {
    console.error("❌ 로봇 DOM 요소를 찾지 못했습니다.");
    return;
  }

  robotImg.src = getRobotImageForLevel(currentLevel);
  robotImg.style.display = "block";
  robotImg.style.opacity = "1";

  robotGif.style.display = "none";
  robotGif.classList.remove("show");

  robotContainer.classList.remove("stage2-vibrate");
  robotImg.classList.add("stage1");
  robotImg.classList.remove("stage2", "stage3", "warning", "full", "light-flash");

  const headerDesc = byId("headerDesc");
  if (headerDesc) headerDesc.classList.add("alert");

  setBattery(START_BATTERY);
  displayQuestion();
}

/* ======== 문제 표시 ======== */
function displayQuestion() {
  const q = questions[currentQuestion];
  if (!q) {
    completeGame();
    return;
  }

  const questionNum = byId("questionNum");
  const questionTitle = byId("questionTitle");
  const questionText = byId("questionText");
  const optionsContainer = byId("options");

  if (!questionNum || !questionTitle || !questionText || !optionsContainer) {
    console.error("❌ 문제 표시 DOM 요소를 찾지 못했습니다.");
    return;
  }

  questionNum.textContent = `Q${currentQuestion + 1}/${questions.length}`;
  questionTitle.textContent = q.title;
  questionText.textContent = q.text;

  optionsContainer.innerHTML = "";

  q.options.forEach((option, idx) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.type = "button";
    btn.textContent = option;
    btn.onclick = () => selectAnswer(idx);
    optionsContainer.appendChild(btn);
  });

  answered = false;
}

/* ======== 정답 선택 ======== */
function selectAnswer(selectedIdx) {
  if (answered) return;

  const q = questions[currentQuestion];
  if (!q) return;

  answered = true;

  const buttons = document.querySelectorAll(".option-btn");
  const state = missionStates[currentQuestion];

  if (!buttons[selectedIdx] || !buttons[q.correct]) {
    console.error("❌ option button index mismatch");
    answered = false;
    return;
  }

  // 클릭할 때마다 표시 초기화(재도전 대응)
  buttons.forEach((b) => b.classList.remove("correct", "wrong"));

  const isCorrect = selectedIdx === q.correct;
  buttons[selectedIdx].classList.add(isCorrect ? "correct" : "wrong");
  buttons[q.correct].classList.add("correct");

  if (isCorrect) {
    state.completed = true;

    // ✅ 배터리: 문제 수에 따라 고르게 증가 (1문제면 바로 100%)
    const gain = Math.ceil((100 - START_BATTERY) / questions.length);
    setBattery(battery + gain);

    setTimeout(() => {
      currentQuestion += 1;
      if (currentQuestion >= questions.length) completeGame();
      else displayQuestion();
    }, 650);
  } else {
    speak("틀렸어요! 다시 도전해봐요!");
    answered = false; // 재도전 허용
  }
}

/* ======== 로봇 상태 갱신 ======== */
function updateRobot() {
  const percent = byId("batteryPercent");
  const fill = byId("batteryFill");
  if (!percent || !fill) return;

  percent.textContent = String(battery);
  fill.style.width = `${battery}%`;

  const headerDesc = byId("headerDesc");
  const robotImg = byId("robotImg");

  if (headerDesc) headerDesc.classList.toggle("alert", battery <= 10);
  if (robotImg) {
    robotImg.classList.toggle("warning", battery <= 10);
    robotImg.classList.toggle("full", battery >= 100);
  }
}

/* ======== 게임 완료 ======== */
function completeGame() {
  const robotImg = byId("robotImg");
  const robotGif = byId("robotGif");
  const headerDesc = byId("headerDesc");

  const questionBox = byId("questionBox");
  const completionScreen = byId("completionScreen");
  const finalScore = byId("finalScore");

  if (!robotImg || !robotGif || !questionBox || !completionScreen || !finalScore) {
    console.error("❌ 완료 화면 DOM 요소를 찾지 못했습니다.");
    return;
  }

  setBattery(100);

  // ✅ B1/B2는 assets/videos/robo_jump.gif (스크린샷 기준)
  const bGif = "./assets/videos/robo_jump.gif";
  const aGif = "./assets/img/robo.gif";

  robotGif.src = (currentLevel === "B1" || currentLevel === "B2") ? bGif : aGif;
  robotGif.onerror = () => { robotGif.src = aGif; };

  robotImg.style.display = "none";
  robotGif.style.display = "block";
  setTimeout(() => robotGif.classList.add("show"), 10);

  if (headerDesc) headerDesc.classList.remove("alert");

  questionBox.style.display = "none";
  completionScreen.classList.add("show");

  finalScore.textContent = "최종 배터리: 100% ⚡ 완벽해! 넌 진짜 최고야!";
  speak("축하해! 고마워! 나를 구해줘서!");
}

/* ======== 기타 ======== */
function resetGame() {
  const levelScreen = byId("levelScreen");
  const gameScreen = byId("gameScreen");
  const questionBox = byId("questionBox");
  const completionScreen = byId("completionScreen");

  const headerDesc = byId("headerDesc");
  const robotImg = byId("robotImg");
  const robotGif = byId("robotGif");

  if (levelScreen) levelScreen.style.display = "flex";
  if (gameScreen) {
    gameScreen.classList.remove("active");
    gameScreen.style.display = "none";
  }
  if (questionBox) questionBox.style.display = "block";
  if (completionScreen) completionScreen.classList.remove("show");

  if (headerDesc) headerDesc.classList.remove("alert");

  if (robotGif) {
    robotGif.classList.remove("show");
    robotGif.style.display = "none";
  }
  if (robotImg) {
    robotImg.style.display = "block";
    robotImg.style.opacity = "1";
    robotImg.src = "./assets/img/robo2.png";
    robotImg.classList.remove("warning", "full", "light-flash");
    robotImg.classList.add("stage1");
  }

  currentQuestion = 0;
  answered = false;
  setBattery(START_BATTERY);

  const options = byId("options");
  if (options) options.innerHTML = "";
}

function goHome() {
  window.location.href = "index.html";
}

// ✅ inline onclick을 위한 전역 노출
window.startGame = startGame;
window.resetGame = resetGame;
window.goHome = goHome;
