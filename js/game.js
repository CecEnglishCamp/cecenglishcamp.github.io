// ===============================
// Grammar Game JS
// ===============================

// 전역 변수
let currentLevel = 'A1';
let currentQuestion = 0;
let battery = 3;
let answered = false;
let engineSoundPlayed = false;
let questions = [];
let missionStates = [];

// ===============================
// 질문 데이터 (레벨별)
// ===============================

const questionsA1 = [
  { title: "Simple Present", text: "I ___ to school every day.", options: ["goes", "go", "going"], correct: 1 },
  { title: "Simple Past", text: "She ___ to the movies yesterday.", options: ["went", "goes", "going"], correct: 0 },
  { title: "Be Verb", text: "They ___ students.", options: ["is", "are", "am"], correct: 1 },
  { title: "Present Continuous", text: "He ___ eating now.", options: ["eat", "is eating", "eats"], correct: 1 },
  { title: "Negative", text: "I ___ like apples.", options: ["not", "don't", "doesn't"], correct: 1 },
  { title: "Yes/No Question", text: "___ you have a pen?", options: ["Do", "Does", "Are"], correct: 0 },
  { title: "Plural", text: "I have three ___ on my desk.", options: ["book", "books", "bokes"], correct: 1 },
  { title: "Possessive", text: "This is ___ cat.", options: ["my", "me", "I"], correct: 0 },
  { title: "Articles", text: "___ apple is red.", options: ["A", "An", "The"], correct: 1 },
  { title: "Future", text: "I ___ visit you tomorrow.", options: ["will visit", "visit", "visits"], correct: 0 }
];

const questionsA2 = [
  { title: "Present Habit", text: "He usually ___ coffee in the morning.", options: ["drink", "drinks", "drinking"], correct: 1 },
  { title: "Past Continuous", text: "I ___ when he called.", options: ["sleep", "was sleeping", "slept"], correct: 1 },
  { title: "Present Perfect", text: "Have you ___ London?", options: ["visit", "visited", "visiting"], correct: 1 },
  { title: "Conditional", text: "If I ___ time, I would help.", options: ["have", "had", "having"], correct: 1 },
  { title: "Comparative", text: "This book is ___ than that one.", options: ["more interesting", "interestinger", "interesting"], correct: 0 },
  { title: "Must/Might", text: "You ___ do your homework.", options: ["must", "might", "can"], correct: 0 },
  { title: "Relative Clause", text: "The girl ___ won the prize is my friend.", options: ["who", "which", "whose"], correct: 0 },
  { title: "Passive Voice", text: "The letter ___ by my sister.", options: ["write", "written", "writing"], correct: 1 },
  { title: "Gerund", text: "___ is good for health.", options: ["Exercise", "Exercising", "Exercises"], correct: 1 },
  { title: "Reported Speech", text: "She said she ___ a student.", options: ["is", "was", "were"], correct: 1 }
];

const questionsB1 = [
  { title: "Complex Sentence", text: "Although tired, she ___.", options: ["continue", "continued", "continues"], correct: 1 },
  { title: "Perfect Continuous", text: "I ___ English for 5 years.", options: ["study", "have studied", "have been studying"], correct: 2 },
  { title: "Subjunctive", text: "I suggest he ___ earlier.", options: ["come", "comes", "came"], correct: 0 },
  { title: "Inversion", text: "Never ___ I seen such beauty.", options: ["have", "had", "has"], correct: 0 },
  { title: "Participle", text: "___ by noise, I couldn’t sleep.", options: ["Disturbing", "Disturbed", "Disturbs"], correct: 1 },
  { title: "Cleft", text: "It is John ___ I met.", options: ["who", "that", "which"], correct: 0 },
  { title: "Phrasal Verb", text: "They decided to ___ the meeting.", options: ["put on", "put off", "put up"], correct: 1 },
  { title: "Collocation", text: "I ___ an important decision.", options: ["make", "do", "take"], correct: 0 },
  { title: "Idiom", text: "She’s ___ a tough time.", options: ["going through", "going over", "going by"], correct: 0 },
  { title: "Advanced", text: "The project is said ___ soon.", options: ["to be", "being", "to have"], correct: 0 }
];

// ===============================
// 게임 시작
// ===============================

function startGame(level) {
  currentLevel = level;
  battery = 3;
  currentQuestion = 0;
  answered = false;

  const robotImg = document.getElementById("robotImage");
  const robotContainer = document.querySelector(".robot-container");

  // ✅ 기존 애니메이션 제거
  robotImg.classList.remove("shake", "jump", "fadeIn", "happy", "charged");

  // ✅ 레벨별 로봇 이미지 변경
  if (level === "B1" || level === "B2") {
    robotImg.src = "assets/img/robo_jump.gif";
  } else {
    robotImg.src = "assets/img/robo2.png";
  }

  // ✅ 게임 UI 세팅
  document.querySelector(".level-grid").style.display = "none";
  document.getElementById("gameContainer").style.display = "flex";

  if (level === "A1") questions = questionsA1;
  else if (level === "A2") questions = questionsA2;
  else if (level === "B1") questions = questionsB1;
  else questions = questionsA1;

  loadQuestion();
}

// ===============================
// 문제 로드
// ===============================

function loadQuestion() {
  const question = questions[currentQuestion];
  const questionText = document.getElementById("questionText");
  const optionsContainer = document.getElementById("options");

  document.getElementById("questionTitle").textContent = question.title;
  questionText.textContent = question.text;
  optionsContainer.innerHTML = "";

  question.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.textContent = option;
    button.onclick = () => checkAnswer(index);
    optionsContainer.appendChild(button);
  });

  document.getElementById("questionCount").textContent = `Q${currentQuestion + 1}/10`;
}

// ===============================
// 정답 체크
// ===============================

function checkAnswer(selected) {
  const correct = questions[currentQuestion].correct;
  const robotImg = document.getElementById("robotImage");

  if (selected === correct) {
    battery += 10;
    robotImg.classList.add("happy");
  } else {
    battery -= 10;
    robotImg.classList.add("shake");
  }

  setTimeout(() => {
    robotImg.classList.remove("happy", "shake");
    nextQuestion();
  }, 1000);
}

// ===============================
// 다음 문제
// ===============================

function nextQuestion() {
  currentQuestion++;
  if (currentQuestion < questions.length) {
    loadQuestion();
  } else {
    showResult();
  }
}

// ===============================
// 결과 화면
// ===============================

function showResult() {
  const gameContainer = document.getElementById("gameContainer");
  const resultContainer = document.getElementById("resultContainer");
  const robotContainer = document.querySelector(".robot-container");

  gameContainer.style.display = "none";
  resultContainer.style.display = "flex";

  // ✅ 완료 시 GIF 또는 동영상 표시
  // robotContainer.innerHTML = `<video src="assets/video/robo_end.mp4" autoplay muted loop></video>`;
  robotContainer.innerHTML = `<img id="robotImage" src="assets/img/robo_charged.gif" alt="Robo Charged">`;

  resultContainer.innerHTML = `
    <h2 style="font-size: 1.6rem;">🎉 축하합니다!</h2>
    <p style="font-size: 1.2rem;">Robo가 완전히 충전되었습니다!</p>
    <p style="font-size: 1.2rem;">고맙습니다! ⚡</p>
    <button onclick="restartGame()">다시 시작</button>
  `;
}

// ===============================
// 다시 시작
// ===============================

function restartGame() {
  document.getElementById("resultContainer").style.display = "none";
  document.querySelector(".level-grid").style.display = "grid";
  document.getElementById("headerDesc").textContent = 
    "⚡ 급해요! Robo의 배터리가 3%밖에 안 남았어요! 문제를 맞춰서 다시 100%로 충전시켜 주세요! 🔋";
}
