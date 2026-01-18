let currentLevel = 'A1';
let currentQuestion = 0;
let battery = 3;
let answered = false;
let engineSoundPlayed = false;
let questions = [];
let missionStates = [];

// 레벨별 문제 데이터
const questionsA1 = [
  { title: "Simple Present", text: "I ___ to school every day.", options: ["goes", "go", "going"], correct: 1 },
  { title: "Simple Past", text: "She ___ to the movies yesterday.", options: ["went", "goes", "going"], correct: 0 },
  { title: "Be Verb", text: "They ___ students.", options: ["is", "are", "am"], correct: 1 },
  { title: "Present Continuous", text: "He ___ eating now.", options: ["eat", "is eating", "eats"], correct: 1 },
  { title: "Negative", text: "I ___ like apples.", options: ["not", "don't", "doesn't"], correct: 1 },
  { title: "Yes/No Question", text: "___ you have a pen?", options: ["Do", "Does", "Are"], correct: 0 },
  { title: "Plural", text: "I have three ___.", options: ["book", "books", "bokes"], correct: 1 },
  { title: "Possessive", text: "This is ___ cat.", options: ["my", "me", "I"], correct: 0 },
  { title: "Articles", text: "___ apple is red.", options: ["A", "An", "The"], correct: 1 },
  { title: "Future", text: "I ___ visit you tomorrow.", options: ["will visit", "visit", "visits"], correct: 0 }
];

const questionsA2 = [
  { title: "Present Habit", text: "He usually ___ coffee in the morning.", options: ["drink", "drinks", "drinking"], correct: 1 },
  { title: "Past Continuous", text: "I ___ when he called.", options: ["sleep", "was sleeping", "slept"], correct: 1 },
  { title: "Present Perfect", text: "Have you ___ London?", options: ["visit", "visited", "visiting"], correct: 1 },
  { title: "Conditional", text: "If I ___, I would help.", options: ["have", "had", "having"], correct: 1 },
  { title: "Comparative", text: "This book is ___ than that one.", options: ["more interesting", "interestinger", "interesting"], correct: 0 },
  { title: "Must/Might", text: "You ___ do your homework.", options: ["must", "might", "can"], correct: 0 },
  { title: "Relative Clause", text: "The girl ___ won the prize.", options: ["who", "which", "whose"], correct: 0 },
  { title: "Passive Voice", text: "The letter ___ by my sister.", options: ["write", "written", "writing"], correct: 1 },
  { title: "Gerund", text: "___ is good for health.", options: ["Exercise", "Exercising", "Exercises"], correct: 1 },
  { title: "Reported Speech", text: "She said she ___ a student.", options: ["is", "was", "were"], correct: 1 }
];

const questionsB1 = [
  { title: "Complex Sentence", text: "Although tired, she ___.", options: ["continue", "continued", "continues"], correct: 1 },
  { title: "Perf Continuous", text: "I ___ English for 5 years.", options: ["study", "have studied", "have been studying"], correct: 2 },
  { title: "Subjunctive", text: "I suggest he ___ earlier.", options: ["come", "comes", "came"], correct: 0 },
  { title: "Inversion", text: "Never ___ I seen such beauty.", options: ["have", "had", "has"], correct: 0 },
  { title: "Participle", text: "___ by noise, I couldn’t sleep.", options: ["Disturbing", "Disturbed", "Disturb"], correct: 1 },
  { title: "Cleft", text: "It is John ___ did it.", options: ["who", "that", "which"], correct: 0 },
  { title: "Phrasal Verb", text: "They decided to ___ the meeting.", options: ["put up", "put off", "put up"], correct: 1 },
  { title: "Collocation", text: "I ___ an important decision.", options: ["make", "do", "take"], correct: 0 },
  { title: "Idiom", text: "She’s ___ a tough time.", options: ["going through", "going over", "going by"], correct: 0 },
  { title: "Advanced", text: "The project is said ___ soon.", options: ["to be", "being", "to have"], correct: 0 }
];

const questionsB2 = questionsB1; // 동일한 데이터 사용 가능

// 레벨별 문제 매칭
const questionSets = { A1: questionsA1, A2: questionsA2, B1: questionsB1, B2: questionsB2 };

// 게임 시작 함수
function startGame(level) {
  currentLevel = level;
  currentQuestion = 0;
  battery = 3;
  answered = false;
  questions = questionSets[level];
  document.querySelector("#level-select").style.display = "none";
  loadQuestion();
}

// 문제 로드
function loadQuestion() {
  const q = questions[currentQuestion];
  const qBox = document.querySelector("#question-box");
  const robotContainer = document.querySelector("#robot-container");

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

  // B1/B2 → robo_jump.gif 표시
  if (currentLevel === "B1" || currentLevel === "B2") {
    robotContainer.innerHTML = `
      <img src="assets/videos/robo_jump.gif" alt="Robo Jump" style="max-width: 420px; border-radius: 15px; box-shadow: 0 0 20px #00ffcc;">
    `;
  }
}

// 정답 체크
function checkAnswer(index) {
  const q = questions[currentQuestion];
  const buttons = document.querySelectorAll(".option");

  buttons.forEach(b => b.disabled = true);

  if (index === q.correct) {
    buttons[index].style.backgroundColor = "#00ff88";
    battery = Math.min(battery + 1, 100);
  } else {
    buttons[index].style.backgroundColor = "#ff4444";
    battery = Math.max(battery - 1, 0);
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

// 게임 종료 화면
function endGame() {
  const qBox = document.querySelector("#question-box");
  const robotContainer = document.querySelector("#robot-container");

  qBox.innerHTML = `
    <h2>🎉 축하합니다!</h2>
    <p>로봇이 완전히 깨어났습니다!</p>
    <p>⚡ 고맙습니다! ⚡</p>
    <button onclick="location.reload()">다시 시작</button>
  `;

  robotContainer.innerHTML = `
    <img src="assets/videos/robo_jump.gif" alt="Robo Success" style="max-width: 420px; border-radius: 15px; box-shadow: 0 0 25px #00ffcc;">
  `;
}
