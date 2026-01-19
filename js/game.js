/* =========================================
File: js/game.js
- Left image + right quiz (DOM ids match index.html)
- 10 questions per level
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

  /** @type {Array<{title:string,text:string,options:string[],correct:number}>} */
  let activeQuestions = [];
  let correctCount = 0;

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

  function byId(id) {
    return /** @type {HTMLElement|null} */ (document.getElementById(id));
  }

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function setBattery(value) {
    battery = clamp(value, 0, 100);

    const percent = byId("batteryPercent");
    const fill = byId("batteryFill");
    if (percent) percent.textContent = String(battery);
    if (fill) fill.style.width = `${battery}%`;

    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.toggle("alert", battery <= 10);

    const robotImg = /** @type {HTMLImageElement|null} */ (byId("robotImg"));
    if (robotImg) {
      robotImg.classList.toggle("warning", battery <= 10);
      robotImg.classList.toggle("full", battery >= 100);
    }
  }

  function getRobotImageForLevel(level) {
    return (level === "B1" || level === "B2") ? "./assets/img/robo_jump.png" : "./assets/img/robo2.png";
  }

  function getCompletionGifForLevel(level) {
    // your repo has assets/videos/robo_jump.gif
    return (level === "B1" || level === "B2") ? "./assets/videos/robo_jump.gif" : "./assets/img/robo.gif";
  }

  function speak(text) {
    if (!("speechSynthesis" in window)) return;
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "ko-KR";
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utter);
  }

  function showGameScreen() {
    const levelScreen = byId("levelScreen");
    const gameScreen = byId("gameScreen");
    if (levelScreen) levelScreen.style.display = "none";
    if (gameScreen) {
      gameScreen.style.display = "block";
      gameScreen.classList.add("active");
    }
  }

  function showLevelScreen() {
    const levelScreen = byId("levelScreen");
    const gameScreen = byId("gameScreen");
    if (levelScreen) levelScreen.style.display = "flex";
    if (gameScreen) {
      gameScreen.classList.remove("active");
      gameScreen.style.display = "none";
    }
  }

  function setRobotToStatic() {
    const robotImg = /** @type {HTMLImageElement|null} */ (byId("robotImg"));
    const robotGif = /** @type {HTMLImageElement|null} */ (byId("robotGif"));
    if (!robotImg || !robotGif) return;

    robotImg.src = getRobotImageForLevel(currentLevel);
    robotImg.style.display = "block";
    robotImg.style.opacity = "1";
    robotImg.classList.remove("light-flash");

    robotGif.classList.remove("show");
    robotGif.style.display = "none";
    robotGif.style.opacity = "0";
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
    answeredLock = false;

    q.options.forEach((opt, idx) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "option-btn";
      btn.textContent = opt;
      btn.onclick = () => selectAnswer(idx);
      options.appendChild(btn);
    });

    const questionBox = byId("questionBox");
    const completion = byId("completionScreen");
    if (questionBox) questionBox.style.display = "block";
    if (completion) completion.classList.remove("show");
  }

  function lockOptions() {
    const options = byId("options");
    if (!options) return;
    options.querySelectorAll("button").forEach((b) => b.setAttribute("disabled", "true"));
  }

  function markOptions(correctIdx, selectedIdx) {
    const buttons = document.querySelectorAll(".option-btn");
    buttons.forEach((b, idx) => {
      b.classList.remove("correct", "wrong");
      if (idx === correctIdx) b.classList.add("correct");
      if (idx === selectedIdx && selectedIdx !== correctIdx) b.classList.add("wrong");
    });
  }

  function flashRobot() {
    const robotImg = byId("robotImg");
    if (!robotImg) return;
    robotImg.classList.add("light-flash");
    window.setTimeout(() => robotImg.classList.remove("light-flash"), 380);
  }

  function selectAnswer(selectedIdx) {
    if (answeredLock) return;
    answeredLock = true;

    const q = activeQuestions[currentQuestionIndex];
    if (!q) return;

    lockOptions();
    markOptions(q.correct, selectedIdx);

    const isCorrect = selectedIdx === q.correct;

    if (isCorrect) {
      correctCount += 1;

      // 3% -> 100%를 10문제에 나눠 충전
      const gain = Math.ceil((100 - START_BATTERY) / QUESTIONS_PER_LEVEL); // 10
      setBattery(battery + gain);
      flashRobot();

      window.setTimeout(() => {
        currentQuestionIndex += 1;
        if (currentQuestionIndex >= QUESTIONS_PER_LEVEL) finishGame();
        else renderQuestion();
      }, 650);
      return;
    }

    speak("틀렸어요! 다시 도전해봐요!");
    window.setTimeout(() => {
      answeredLock = false;
      const options = byId("options");
      if (!options) return;
      options.querySelectorAll("button").forEach((b) => b.removeAttribute("disabled"));
    }, 450);
  }

  function finishGame() {
    setBattery(100);

    const questionBox = byId("questionBox");
    const completion = byId("completionScreen");
    const finalScore = byId("finalScore");

    if (questionBox) questionBox.style.display = "none";
    if (completion) completion.classList.add("show");
    if (finalScore) finalScore.textContent = `정답: ${correctCount} / ${QUESTIONS_PER_LEVEL}   (배터리 100% ⚡)`;

    const robotImg = /** @type {HTMLImageElement|null} */ (byId("robotImg"));
    const robotGif = /** @type {HTMLImageElement|null} */ (byId("robotGif"));
    if (robotImg && robotGif) {
      robotGif.src = getCompletionGifForLevel(currentLevel);
      robotGif.onerror = () => { robotGif.src = "./assets/img/robo.gif"; };

      robotImg.style.display = "none";
      robotGif.style.display = "block";
      window.setTimeout(() => robotGif.classList.add("show"), 10);
    }

    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.remove("alert");

    speak("축하해! 고마워! 나를 구해줘서!");
  }

  function startGame(level) {
    currentLevel = level;

    const bank = QUESTION_BANK[level];
    if (!bank || bank.length < QUESTIONS_PER_LEVEL) {
      console.error("❌ 해당 레벨 문제(10개)가 부족합니다:", level);
      return;
    }

    activeQuestions = bank.slice(0, QUESTIONS_PER_LEVEL);
    currentQuestionIndex = 0;
    correctCount = 0;

    showGameScreen();
    setRobotToStatic();
    setBattery(START_BATTERY);

    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.add("alert");

    renderQuestion();
  }

  function resetGame() {
    showLevelScreen();

    const completion = byId("completionScreen");
    if (completion) completion.classList.remove("show");

    const headerDesc = byId("headerDesc");
    if (headerDesc) headerDesc.classList.remove("alert");

    activeQuestions = [];
    currentQuestionIndex = 0;
    correctCount = 0;
    answeredLock = false;

    setBattery(START_BATTERY);

    const options = byId("options");
    if (options) options.innerHTML = "";

    const robotImg = /** @type {HTMLImageElement|null} */ (byId("robotImg"));
    const robotGif = /** @type {HTMLImageElement|null} */ (byId("robotGif"));
    if (robotGif) {
      robotGif.classList.remove("show");
      robotGif.style.display = "none";
    }
    if (robotImg) {
      robotImg.style.display = "block";
      robotImg.src = "./assets/img/robo2.png";
      robotImg.classList.remove("warning", "full");
    }
  }

  function goHome() {
    window.location.href = "index.html";
  }

  // inline onclick 유지
  window.startGame = startGame;
  window.resetGame = resetGame;
  window.goHome = goHome;

  document.addEventListener("DOMContentLoaded", () => {
    setBattery(START_BATTERY);
  });
})();
