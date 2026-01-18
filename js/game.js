console.log("✅ grammar-game.js loaded successfully!");

// 기본 변수 설정
let currentLevel = 'A1';
let currentQuestion = 0;
let battery = 3;
let answered = false;
let engineSoundPlayed = false;
let questions = [];
let missionStates = [];

/* ======== 예시 문제셋 ======== */
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

/* ======== 게임 시작 ======== */
function startGame(level) {
  currentLevel = level;
  currentQuestion = 0;
  battery = 3;
  answered = false;
  engineSoundPlayed = false;

  if (level === 'A1') questions = questionsA1;
  else if (level === 'A2') questions = questionsA2;
  else if (level === 'B1') questions = questionsB1;
  else questions = questionsB2;

  missionStates = questions.map((q, i) => ({
    id: i, completed: false, triedOnce: false, usedBaseCamp: false
  }));

  document.getElementById('levelScreen').style.display = 'none';
  document.getElementById('gameScreen').classList.add('active');
  document.getElementById('questionBox').style.display = 'block';
  document.getElementById('completionScreen').classList.remove('show');

  const robotImg = document.getElementById('robotImg');
  const robotGif = document.getElementById('robotGif');
  const robotContainer = document.getElementById('robotContainer');

  // ✅ B1/B2는 점프 로봇 이미지 사용
  if (currentLevel === 'B1' || currentLevel === 'B2') {
    robotImg.src = 'assets/img/robo_jump.png';
    robotImg.onload = () => console.log("🔁 B-level robo_jump.png loaded");
  } else {
    robotImg.src = 'assets/img/robo2.png';
    robotImg.onload = () => console.log("🟢 A-level robo2.png loaded");
  }

  robotImg.style.display = 'block';
  robotGif.style.display = 'none';
  robotGif.classList.remove('show');

  // 쉐이킹 완전 제거
  robotContainer.classList.remove('stage2-vibrate');

  robotImg.classList.add('stage1');
  robotImg.classList.remove('stage2', 'stage3');

  // 🔴 “급해요!” 문구 깜빡임 효과 적용
  const headerDesc = document.getElementById('headerDesc');
  if (headerDesc) headerDesc.classList.add('alert');

  displayQuestion();
  updateRobot();
}

/* ======== 문제 표시 ======== */
function displayQuestion() {
  const q = questions[currentQuestion];
  document.getElementById("questionNum").textContent = `Q${currentQuestion + 1}/1`;
  document.getElementById("questionTitle").textContent = q.title;
  document.getElementById("questionText").textContent = q.text;

  const optionsContainer = document.getElementById("options");
  optionsContainer.innerHTML = "";

  q.options.forEach((option, idx) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.textContent = option;
    btn.onclick = () => selectAnswer(idx);
    optionsContainer.appendChild(btn);
  });

  answered = false;
}

/* ======== 정답 선택 ======== */
function selectAnswer(selectedIdx) {
  if (answered) return;
  answered = true;

  const q = questions[currentQuestion];
  const buttons = document.querySelectorAll(".option-btn");
  const state = missionStates[currentQuestion];

  buttons[selectedIdx].classList.add(selectedIdx === q.correct ? "correct" : "wrong");
  buttons[q.correct].classList.add("correct");

  if (selectedIdx === q.correct) {
    state.completed = true;
    battery = Math.min(battery + 100, 100);
    updateRobot();
    setTimeout(completeGame, 1000);
  } else {
    speak("틀렸어요! 다시 도전해봐요!");
    answered = false;
  }
}

/* ======== 로봇 상태 갱신 ======== */
function updateRobot() {
  const percent = document.getElementById("batteryPercent");
  const fill = document.getElementById("batteryFill");
  percent.textContent = battery;
  fill.style.width = battery + "%";
}

/* ======== 게임 완료 ======== */
function completeGame() {
  const robotImg = document.getElementById('robotImg');
  const robotGif = document.getElementById('robotGif');
  const headerDesc = document.getElementById('headerDesc');

  battery = 100;
  updateRobot();

  // ✅ B1/B2 레벨 완료 시 점프 GIF 사용
  if (currentLevel === 'B1' || currentLevel === 'B2') {
    robotGif.src = 'assets/videos/robo_jump.gif';
  } else {
    robotGif.src = 'assets/img/robo.gif';
  }

  robotImg.style.display = 'none';
  robotGif.style.display = 'block';
  setTimeout(() => robotGif.classList.add('show'), 10);

  if (headerDesc) headerDesc.classList.remove('alert');

  document.getElementById('questionBox').style.display = 'none';
  document.getElementById('completionScreen').classList.add('show');
  document.getElementById('finalScore').textContent =
    `최종 배터리: 100% ⚡ 완벽해! 넌 진짜 최고야!`;

  speak("축하해! 고마워! 나를 구해줘서!");
}

/* ======== 음성 ======== */
function speak(text) {
  if ('speechSynthesis' in window) {
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'ko-KR';
    window.speechSynthesis.speak(utter);
  }
}

/* ======== 기타 ======== */
function resetGame() {
  document.getElementById('levelScreen').style.display = 'flex';
  document.getElementById('gameScreen').classList.remove('active');
  const headerDesc = document.getElementById('headerDesc');
  if (headerDesc) headerDesc.classList.remove('alert');
}
