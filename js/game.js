let currentLevel = 'A1';
let currentQuestion = 0;
let battery = 3;
let answered = false;
let questions = [];

// 레벨별 문제 세트
const questionSets = {
  A1: [
    { title: "Simple Present", text: "I ___ to school every day.", options: ["goes", "go", "going"], correct: 1 },
    { title: "Simple Past", text: "She ___ to the movies yesterday.", options: ["went", "goes", "going"], correct: 0 },
  ],
  A2: [
    { title: "Present Perfect", text: "He has ___ to London.", options: ["go", "gone", "going"], correct: 1 },
  ],
  B1: [
    { title: "Complex Sentence", text: "Although tired, she ___.", options: ["continue", "continued", "continues"], correct: 1 },
  ],
  B2: [
    { title: "Subjunctive", text: "I suggest he ___ earlier.", options: ["come", "comes", "came"], correct: 0 },
  ]
};

// 🔹 게임 시작
function startGame(level) {
  currentLevel = level;
  currentQuestion = 0;
  battery = 3;
  answered = false;
  questions = questionSets[level];

  // 레벨 선택 화면 숨기기
  document.querySelector("#level-select").style.display = "none";

  // 레벨별 이미지 변경
  const robotContainer = document.querySelector("#robot-container");
  if (level === "B1" || level === "B2") {
    robotContainer.innerHTML = `
      <img src="assets/videos/robo_jump.png" 
           alt="Robo Jump"
           id="robot-image"
           style="max-width: 400px; border-radius: 15px; box-shadow: 0 0 20px #00ffcc;">
    `;
  } else {
    robotContainer.innerHTML = `
      <img src="assets/videos/robo_idle.png" 
           alt="Robo Idle"
           id="robot-image"
           style="max-width: 400px; border-radius: 15px; box-shadow: 0 0 20px #ff4444;">
    `;
  }

  loadQuestion();
}

// 🔹 문제 로드
function loadQuestion() {
  const q = questions[currentQuestion];
  const qBox = document.querySelector("#question-box");

  qBox.innerHTML = `
    <h3>Q${currentQuestion + 1}/${questions.length}</h3>
    <h2>${q.title}</h2>
    <p>${q.text}</p>
    <div id="options">
      ${q.options.map((opt, i) => `
        <button class="option" onclick="checkAnswer(${i})">${opt}</button>
      `).join('')}
    </div>
  `;
}

// 🔹 정답 확인
function checkAnswer(index) {
  const q = questions[currentQuestion];
  const buttons = document.querySelectorAll(".option");
  buttons.forEach(btn => btn.disabled = true);

  if (index === q.correct) {
    buttons[index].style.backgroundColor = "#00ff88";
    battery = Math.min(battery + 10, 100);
  } else {
    buttons[index].style.backgroundColor = "#ff4444";
    battery = Math.max(battery - 10, 0);
  }

  setTimeout(() => {
    currentQuestion++;
    if (currentQuestion < questions.length) {
      loadQuestion();
    } else {
      endGame();
    }
  }, 1000);
}

// 🔹 게임 종료
function endGame() {
  const qBox = document.querySelector("#question-box");
  const robotContainer = document.querySelector("#robot-container");

  qBox.innerHTML = `
    <h2>⚡ Robo가 완전히 충전되었습니다! ⚡</h2>
    <p>정말 고마워! 나를 구해줬어! 🚀</p>
    <button onclick="location.reload()">다시 시작</button>
  `;

  // 🎬 완료 시 robo_jump.gif 로 변경
  robotContainer.innerHTML = `
    <img src="assets/videos/robo_jump.gif"
         alt="Robo Jump Animation"
         id="robot-gif"
         style="max-width: 420px; border-radius: 15px; box-shadow: 0 0 25px #00ffcc;">
  `;
}
