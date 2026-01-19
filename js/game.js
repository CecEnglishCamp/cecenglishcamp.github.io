/* =========================================
File: js/game.js
Grammar Game Final Version
========================================= */

console.log("✅ Grammar Game JS loaded successfully!");

// 기본 변수
let currentLevel = "A1";
let currentQuestion = 0;
let battery = 3;
let answered = false;
let questions = [];
let missionStates = [];

// 초기 배터리
const START_BATTERY = 3;

/* ======== 문제 세트 ======== */
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

/* ======== DOM 헬퍼 ======== */
const byId = (id) => document.getElementById(id);
const clamp = (n, min, max) => Math.max(min, Math.min(max, n));

/* ======== 로봇 경로 설정 ======== */
function getRobotImage(level) {
  return (level === "B1" || level === "B2")
    ? "./assets/img/robo_jump.png"
    : "./assets/img/robo2.png";
}
function getRobotGif(level) {
  return (level === "B1" || level === "B2")
    ? "./assets/videos/robo_jump.gif"
    : "./assets/img/robo.gif";
}

/* ======== 음성 ======== */
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
  battery = START_BATTERY;

  // 문제 선택
  if (level === "A1") questions = questionsA1;
  else if (level === "A2") questions = questionsA2;
  else if (level === "B1") questions = questionsB1;
  else questions = questionsB2;

  missionStates = questions.map((_, i) => ({
    id: i,
    completed: false,
    triedOnce: false,
  }));

  // 화면 전환
  byId("levelScreen").style.display = "none";
  const gameScreen = byId("gameScreen");
  gameScreen.style.display = "block";
  gameScreen.classList.add("active");

  const questionBox = byId("questionBox");
  const completionScreen = byId("completionScreen");
  questionBox.style.display = "block";
  completionScreen.classList.remove("show");

  const robotImg = byId("robotImg");
  const robotGif = byId("robotGif");
  const robotContainer = byId("robotContainer");

  // 초기 로봇 세팅
  robotImg.src = getRobotImage(currentLevel);
  robotGif.style.display = "none";
  robotGif.classList.remove("show");
  robotContainer.classList.remove("stage2-vibrate");

  // “급해요!” 문구 깜빡임 시작
  const headerDesc = byId("headerDesc");
  if (headerDesc) headerDesc.classList.add("alert");

  updateBattery(START_BATTERY);
  displayQuestion();
}

/* ======== 문제 표시 ======== */
function displayQuestion() {
  const q = questions[currentQuestion];
  if (!q) {
    completeGame();
    return;
  }

  byId("questionNum").textContent = `Q${currentQuestion + 1}/${questions.length}`;
  byId("questionTitle").textContent = q.title;
  byId("questionText").textContent = q.text;

  const options = byId("options");
  options.innerHTML = "";

  q.options.forEach((opt, idx) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.textContent = opt;
    btn.onclick = () => selectAnswer(idx);
    options.appendChild(btn);
  });

  answered = false;
}

/* ======== 정답 선택 ======== */
function selectAnswer(selectedIdx) {
  if (answered) return;
  answered = true;

  const q = questions[currentQuestion];
  const buttons = document.querySelectorAll(".option-btn");

  const correctIdx = q.correct;
  const isCorrect = selectedIdx === correctIdx;

  buttons[selectedIdx].classList.add(isCorrect ? "correct" : "wrong");
  buttons[correctIdx].classList.add("correct");

  if (isCorrect) {
    missionStates[currentQuestion].completed = true;

    const gain = Math.ceil((100 - START_BATTERY) / questions.length);
    updateBattery(battery + gain);

    setTimeout(() => {
      currentQuestion++;
      if (currentQuestion >= questions.length) completeGame();
      else displayQuestion();
    }, 800);
  } else {
    speak("틀렸어요! 다시 도전해봐요!");
    setTimeout(() => { answered = false; }, 1000);
  }
}

/* ======== 배터리 갱신 ======== */
function updateBattery(value) {
  battery = clamp(value, 0, 100);
  const percent = byId("batteryPercent");
  const fill = byId("batteryFill");
  percent.textContent = battery;
  fill.style.width = `${battery}%`;

  const robotImg = byId("robotImg");
  if (battery >= 100) robotImg.classList.add("full");
  else robotImg.classList.remove("full");
}

/* ======== 게임 완료 ======== */
function completeGame() {
  updateBattery(100);

  const robotImg = byId("robotImg");
  const robotGif = byId("robotGif");
  const headerDesc = byId("headerDesc");
  const completionScreen = byId("completionScreen");
  const questionBox = byId("questionBox");
  const finalScore = byId("finalScore");

  // 로봇 교체
  robotGif.src = getRobotGif(currentLevel);
  robotGif.onerror = () => { robotGif.src = "./assets/img/robo.gif"; };

  robotImg.style.display = "none";
  robotGif.style.display = "block";
  setTimeout(() => robotGif.classList.add("show"), 10);

  // 문구 정지
  if (headerDesc) headerDesc.classList.remove("alert");

  // 화면 전환
  questionBox.style.display = "none";
  completionScreen.classList.add("show");
  finalScore.textContent = "최종 배터리: 100% ⚡ 완벽해! 넌 진짜 최고야!";

  speak("축하해! 고마워! 나를 구해줘서!");
}

/* ======== 게임 리셋 ======== */
function resetGame() {
  byId("levelScreen").style.display = "flex";
  const gameScreen = byId("gameScreen");
  gameScreen.classList.remove("active");
  gameScreen.style.display = "none";

  const headerDesc = byId("headerDesc");
  if (headerDesc) headerDesc.classList.remove("alert");

  const robotImg = byId("robotImg");
  const robotGif = byId("robotGif");
  robotGif.classList.remove("show");
  robotGif.style.display = "none";
  robotImg.style.display = "block";
  robotImg.src = "./assets/img/robo2.png";

  currentQuestion = 0;
  answered = false;
  updateBattery(START_BATTERY);
  byId("options").innerHTML = "";
}

/* ======== 홈 이동 ======== */
function goHome() {
  window.location.href = "index.html";
}

/* ======== 전역 등록 ======== */
window.startGame = startGame;
window.resetGame = resetGame;
window.goHome = goHome;
