/* =========================================
File: js/game.js
Purpose: 게임 로직 + headerDesc 워닝 깜빡임 자동 적용
========================================= */

(() => {
  "use strict";

  console.log("✅ game.js loaded successfully!");

  const START_BATTERY = 3;
  const QUESTIONS_PER_LEVEL = 10;

  let currentLevel = "A1";
  let currentQuestionIndex = 0;
  let battery = START_BATTERY;
  let answeredLock = false;

  let activeQuestions = [];
  let correctCount = 0;

  // ✅ 예시 문제 (각 레벨 10문제)
  const QUESTION_BANK = {
    A1: [
      { title: "Simple Present", text: "I ___ to school every day.", options: ["goes", "go", "going"], correct: 1 },
      { title: "Be Verb", text: "She ___ happy.", options: ["am", "is", "are"], correct: 1 },
      { title: "Articles", text: "This is ___ apple.", options: ["a", "an", "the"], correct: 1 },
      { title: "Prepositions", text: "The cat is ___ the table.", options: ["in", "on", "at"], correct: 1 },
      { title: "Plural", text: "Two ___ are on the desk.", options: ["book", "books", "bookes"], correct: 1 },
      { title: "This/That", text: "___ is my bag (near).", options: ["This", "That", "Those"], correct: 0 },
      { title: "Can", text: "I ___ swim.", options: ["can", "cans", "can'ts"], correct: 0 },
      { title: "Have", text: "They ___ a dog.", options: ["has", "have", "having"], correct: 1 },
      { title: "Adverbs", text: "He runs ___.", options: ["quick", "quickly", "quicks"], correct: 1 },
      { title: "Possessive", text: "This is ___ pen.", options: ["I", "me", "my"], correct: 2 },
    ],
    A2: [
      { title: "Past Simple", text: "We ___ soccer yesterday.", options: ["play", "played", "playing"], correct: 1 },
      { title: "Past Continuous", text: "I ___ when he called.", options: ["sleep", "was sleeping", "slept"], correct: 1 },
      { title: "Future", text: "I ___ visit tomorrow.", options: ["will", "was", "did"], correct: 0 },
      { title: "Comparatives", text: "Tom is ___ than Jim.", options: ["tall", "taller", "tallest"], correct: 1 },
      { title: "Much/Many", text: "How ___ apples?", options: ["much", "many", "more"], correct: 1 },
      { title: "Some/Any", text: "Do you have ___ water?", options: ["some", "any", "many"], correct: 1 },
      { title: "Present Perfect", text: "I have ___ my homework.", options: ["finish", "finished", "finishing"], correct: 1 },
      { title: "Modal", text: "You ___ wear a helmet.", options: ["should", "would", "used"], correct: 0 },
      { title: "Gerund", text: "I enjoy ___ music.", options: ["listen", "to listen", "listening"], correct: 2 },
      { title: "Because", text: "I stayed home ___ it rained.", options: ["because", "but", "so"], correct: 0 },
    ],
    B1: [
      { title: "Relative Clause", text: "The man ___ lives next door is kind.", options: ["who", "where", "when"], correct: 0 },
      { title: "Present Perfect", text: "She has ___ to Japan.", options: ["go", "went", "been"], correct: 2 },
      { title: "Complex Sentence", text: "Although tired, she ___.", options: ["continue", "continued", "continues"], correct: 1 },
      { title: "Passive", text: "The room ___ every day.", options: ["cleans", "is cleaned", "cleaned"], correct: 1 },
      { title: "Reported", text: "He said he ___ busy.", options: ["is", "was", "be"], correct: 1 },
      { title: "Conditionals", text: "If it rains, we ___ inside.", options: ["stay", "stayed", "would stay"], correct: 0 },
      { title: "Quantifiers", text: "There are ___ people here.", options: ["a little", "a few", "fewest"], correct: 1 },
      { title: "Infinitive", text: "I decided ___ early.", options: ["leave", "to leave", "leaving"], correct: 1 },
      { title: "Linking", text: "I was tired, ___ I went to bed.", options: ["so", "because", "although"], correct: 0 },
      { title: "Comparative", text: "This is ___ interesting than that.", options: ["more", "most", "much"], correct: 0 },
    ],
    B2: [
      { title: "Mixed Conditional", text: "Had I known, I ___ you.", options: ["would contact", "would have contacted", "will contact"], correct: 1 },
      { title: "Inversion", text: "Rarely ___ such a view.", options: ["I have seen", "have I seen", "I saw"], correct: 1 },
      { title: "Passive", text: "The cake ___ by my mom.", options: ["was made", "made", "is make"], correct: 0 },
      { title: "Reported", text: "He said he ___ tired.", options: ["is", "was", "be"], correct: 1 },
      { title: "Conditionals", text: "If I were you, I ___ apologize.", options: ["will", "would", "did"], correct: 1 },
      { title: "Perfect Modal", text: "You ___ have told me.", options: ["should", "should to", "should have"], correct: 2 },
      { title: "Subjunctive", text: "I suggest that he ___ earlier.", options: ["leave", "leaves", "left"], correct: 0 },
      { title: "Concession", text: "___ he was late, he apologized.", options: ["Despite", "Although", "Because"], correct: 1 },
      { title: "Causative", text: "I had my phone ___", options: ["repair", "repaired", "repairing"], correct: 1 },
      { title: "Ellipsis", text: "I can play guitar and so ___ my brother.", options: ["can", "does", "did"], correct: 0 },
    ],
  };

  // 🔧 헬퍼
  const byId = (id) => document.getElementById(id);
  const clamp = (n, min, max) => Math.max(min, Math.min(max, n));

  function setBattery(value) {
    battery = clamp(value, 0, 100);

    const percent = byId("batteryPercent");
    const fill = byId("batteryFill");
    if (percent) percent.textContent = String(battery);
    if (fill) fill.style.width = `${battery}%`;

    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.toggle("warning", battery <= 10);

    const robotImg = byId("robotImg");
    if (robotImg) {
      robotImg.classList.toggle("warning", battery <= 10);
      robotImg.classList.toggle("full", battery >= 100);
    }
  }

  function getRobotImageForLevel(level) {
    return (level === "B1" || level === "B2")
      ? "./assets/img/robo_jump.png"
      : "./assets/img/robo2.png";
  }

  function speak(text) {
    if (!("speechSynthesis" in window)) return;
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "ko-KR";
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utter);
  }

  // ✅ 게임 시작
  function startGame(level) {
    currentLevel = level;
    activeQuestions = QUESTION_BANK[level];
    currentQuestionIndex = 0;
    correctCount = 0;
    answeredLock = false;

    const levelScreen = byId("levelScreen");
    const gameScreen = byId("gameScreen");
    if (levelScreen) levelScreen.style.display = "none";
    if (gameScreen) gameScreen.style.display = "block";

    setBattery(START_BATTERY);

    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.add("warning"); // ⚡ 게임 시작 시 워닝 글씨 깜빡임 유지

    renderQuestion();
  }

  function renderQuestion() {
    const q = activeQuestions[currentQuestionIndex];
    if (!q) return finishGame();

    const questionNum = byId("questionNum");
    const questionTitle = byId("questionTitle");
    const questionText = byId("questionText");
    const options = byId("options");

    if (!questionNum || !questionTitle || !questionText || !options) return;

    questionNum.textContent = `Q${currentQuestionIndex + 1}/${QUESTIONS_PER_LEVEL}`;
    questionTitle.textContent = q.title;
    questionText.textContent = q.text;
    options.innerHTML = "";

    q.options.forEach((opt, idx) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "option-btn";
      btn.textContent = opt;
      btn.onclick = () => selectAnswer(idx);
      options.appendChild(btn);
    });
  }

  function selectAnswer(selectedIdx) {
    if (answeredLock) return;
    answeredLock = true;

    const q = activeQuestions[currentQuestionIndex];
    if (!q) return;

    const buttons = document.querySelectorAll(".option-btn");
    buttons.forEach((b) => b.disabled = true);

    const isCorrect = selectedIdx === q.correct;
    buttons[selectedIdx].classList.add(isCorrect ? "correct" : "wrong");
    buttons[q.correct].classList.add("correct");

    if (isCorrect) {
      correctCount++;
      setBattery(battery + Math.ceil((100 - START_BATTERY) / QUESTIONS_PER_LEVEL));
      setTimeout(() => {
        currentQuestionIndex++;
        if (currentQuestionIndex >= QUESTIONS_PER_LEVEL) finishGame();
        else renderQuestion();
      }, 600);
    } else {
      speak("틀렸어요! 다시 도전해봐요!");
      setTimeout(() => {
        answeredLock = false;
        buttons.forEach((b) => b.disabled = false);
      }, 800);
    }
  }

  function finishGame() {
    setBattery(100);

    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.remove("warning");

    const questionBox = byId("questionBox");
    const completion = byId("completionScreen");
    const finalScore = byId("finalScore");

    if (questionBox) questionBox.style.display = "none";
    if (completion) completion.classList.add("show");
    if (finalScore) finalScore.textContent = `최종 배터리: 100% ⚡ 완벽해! 넌 진짜 최고야!`;

    speak("정말 고마워! 나를 구해줘서!");
  }

  function resetGame() {
    const levelScreen = byId("levelScreen");
    const gameScreen = byId("gameScreen");
    if (levelScreen) levelScreen.style.display = "flex";
    if (gameScreen) gameScreen.style.display = "none";

    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.remove("warning");

    setBattery(START_BATTERY);
  }

  // ✅ 페이지 로드 시 워닝 시작
  document.addEventListener("DOMContentLoaded", () => {
    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.add("warning");
    setBattery(START_BATTERY);
  });

  // expose
  window.startGame = startGame;
  window.resetGame = resetGame;
})();
