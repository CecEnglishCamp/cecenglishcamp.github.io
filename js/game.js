(() => {
  "use strict";

  const START_BATTERY = 3;
  const TOTAL = 10;

  // ✅ 실제 mp4 쓰시면 넣으세요(없으면 자동으로 gif로 fallback)
  const VIDEO_MAP = {
    A1: "",
    A2: "",
    B1: "",
    B2: "",
  };

  // ✅ B1/B2 100% 달성 시: assets/videos/robo_jump.gif 사용
  const COMPLETION_GIF_MAP = {
    A1: "./assets/img/robo.gif",
    A2: "./assets/img/robo.gif",
    B1: "./assets/videos/robo_jump.gif",
    B2: "./assets/videos/robo_jump.gif",
  };

  const QUESTIONS = {
    A1: [
      { title: "Simple Present", text: "I __ to school every day.", options: ["goes", "go", "going"], correct: 1 },
      { title: "Be Verb", text: "She __ happy.", options: ["am", "is", "are"], correct: 1 },
      { title: "Articles", text: "This is __ apple.", options: ["a", "an", "the"], correct: 1 },
      { title: "Prepositions", text: "The cat is __ the table.", options: ["in", "on", "at"], correct: 1 },
      { title: "Plural", text: "Two __ are here.", options: ["book", "books", "bookes"], correct: 1 },
      { title: "Can", text: "He __ swim.", options: ["can", "cans", "cannot to"], correct: 0 },
      { title: "Have", text: "They __ a dog.", options: ["has", "have", "having"], correct: 1 },
      { title: "This/That", text: "__ is my pencil (near).", options: ["This", "That", "Those"], correct: 0 },
      { title: "Adverbs", text: "He runs __.", options: ["quick", "quickly", "quicks"], correct: 1 },
      { title: "Possessive", text: "This is __ bag.", options: ["I", "me", "my"], correct: 2 },
    ],
    A2: [
      { title: "Past Simple", text: "We __ soccer yesterday.", options: ["play", "played", "playing"], correct: 1 },
      { title: "Past Continuous", text: "I __ when he called.", options: ["sleep", "was sleeping", "slept"], correct: 1 },
      { title: "Future", text: "I __ visit tomorrow.", options: ["will", "was", "did"], correct: 0 },
      { title: "Comparatives", text: "Tom is __ than Jim.", options: ["tall", "taller", "tallest"], correct: 1 },
      { title: "Much/Many", text: "How __ apples?", options: ["much", "many", "more"], correct: 1 },
      { title: "Some/Any", text: "Do you have __ water?", options: ["some", "any", "many"], correct: 1 },
      { title: "Present Perfect", text: "I have __ my homework.", options: ["finish", "finished", "finishing"], correct: 1 },
      { title: "Modal", text: "You __ wear a helmet.", options: ["should", "would", "used"], correct: 0 },
      { title: "Gerund", text: "I enjoy __ music.", options: ["listen", "to listen", "listening"], correct: 2 },
      { title: "Because", text: "I stayed home __ it rained.", options: ["because", "but", "so"], correct: 0 },
    ],
    B1: [
      { title: "Relative", text: "The man __ lives next door is kind.", options: ["who", "where", "when"], correct: 0 },
      { title: "Present Perfect", text: "She has __ to Japan.", options: ["go", "went", "been"], correct: 2 },
      { title: "Complex", text: "Although tired, she ___.", options: ["continue", "continued", "continues"], correct: 1 },
      { title: "Passive", text: "The room __ every day.", options: ["cleans", "is cleaned", "cleaned"], correct: 1 },
      { title: "Reported", text: "He said he __ busy.", options: ["is", "was", "be"], correct: 1 },
      { title: "Conditional", text: "If it rains, we __ inside.", options: ["stay", "stayed", "would stay"], correct: 0 },
      { title: "Quantifiers", text: "There are __ people here.", options: ["a little", "a few", "fewest"], correct: 1 },
      { title: "Infinitive", text: "I decided __ early.", options: ["leave", "to leave", "leaving"], correct: 1 },
      { title: "Linking", text: "I was tired, __ I went to bed.", options: ["so", "because", "although"], correct: 0 },
      { title: "Comparative", text: "This is __ interesting than that.", options: ["more", "most", "much"], correct: 0 },
    ],
    B2: [
      { title: "Mixed Conditional", text: "Had I known, I __ you.", options: ["would contact", "would have contacted", "will contact"], correct: 1 },
      { title: "Inversion", text: "Rarely __ such a view.", options: ["I have seen", "have I seen", "I saw"], correct: 1 },
      { title: "Passive", text: "The cake __ by my mom.", options: ["was made", "made", "is make"], correct: 0 },
      { title: "Reported", text: "He said he __ tired.", options: ["is", "was", "be"], correct: 1 },
      { title: "2nd Conditional", text: "If I were you, I __ apologize.", options: ["will", "would", "did"], correct: 1 },
      { title: "Perfect Modal", text: "You __ have told me.", options: ["should", "should to", "should have"], correct: 2 },
      { title: "Subjunctive", text: "I suggest that he __ earlier.", options: ["leave", "leaves", "left"], correct: 0 },
      { title: "Concession", text: "__ he was late, he apologized.", options: ["Despite", "Although", "Because"], correct: 1 },
      { title: "Causative", text: "I had my phone __", options: ["repair", "repaired", "repairing"], correct: 1 },
      { title: "Ellipsis", text: "I can play guitar and so __ my brother.", options: ["can", "does", "did"], correct: 0 },
    ],
  };

  let level = "A1";
  let index = 0;
  let correctCount = 0;
  let battery = START_BATTERY;
  let locked = false;

  const $ = (id) => document.getElementById(id);

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function speak(text) {
    if (!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "ko-KR";
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
  }

  function applyBatteryStageVisuals() {
    const frame = $("robotFrame");
    const headerDesc = $("headerDesc");
    if (!frame) return;

    frame.classList.remove(
      "card--danger",
      "card--ok",
      "card--boost",
      "card--ultra",
      "card--complete-left",
      "is-shaking-soft",
      "is-shaking-hard",
    );

    // 0~29: red blinking
    if (battery < 30) {
      frame.classList.add("card--danger");
      if (headerDesc) headerDesc.classList.add("alert");
      return;
    }

    // 30~69: green
    if (battery < 70) {
      frame.classList.add("card--ok");
      if (headerDesc) headerDesc.classList.remove("alert");
      return;
    }

    // 70~89: stronger green + soft shake
    if (battery < 90) {
      frame.classList.add("card--boost", "is-shaking-soft");
      if (headerDesc) headerDesc.classList.remove("alert");
      return;
    }

    // 90~99: ultra bright + hard shake
    if (battery < 100) {
      frame.classList.add("card--ultra", "is-shaking-hard");
      if (headerDesc) headerDesc.classList.remove("alert");
      return;
    }

    // 100: complete
    frame.classList.add("card--complete-left");
    if (headerDesc) headerDesc.classList.remove("alert");
  }

  function setBattery(value) {
    battery = clamp(value, 0, 100);

    const percent = $("batteryPercent");
    const fill = $("batteryFill");
    if (percent) percent.textContent = String(battery);
    if (fill) fill.style.width = `${battery}%`;

    applyBatteryStageVisuals();
  }

  function showGame() {
    const levelScreen = $("levelScreen");
    const gameScreen = $("gameScreen");
    if (levelScreen) levelScreen.style.display = "none";
    if (gameScreen) {
      gameScreen.style.display = "block";
      gameScreen.classList.add("active");
    }
  }

  function showLevel() {
    const levelScreen = $("levelScreen");
    const gameScreen = $("gameScreen");
    if (levelScreen) levelScreen.style.display = "flex";
    if (gameScreen) {
      gameScreen.style.display = "none";
      gameScreen.classList.remove("active");
    }
  }

  function showRobotImage() {
    const img = $("robotImg");
    const gif = $("robotGif");
    const vid = $("robotVideo");

    if (img) img.style.display = "block";
    if (gif) { gif.classList.remove("show"); gif.style.display = "none"; }

    if (vid) {
      vid.classList.remove("show");
      vid.style.display = "none";
      vid.pause();
      vid.removeAttribute("src");
      vid.load();
    }
  }

  function getRobotImageForLevel(lv) {
    return (lv === "B1" || lv === "B2") ? "./assets/img/robo_jump.png" : "./assets/img/robo2.png";
  }

  function showCompletionMedia() {
    const img = $("robotImg");
    const gif = $("robotGif");
    const vid = $("robotVideo");

    if (img) img.style.display = "none";

    const videoSrc = (VIDEO_MAP[level] || "").trim();
    if (vid && videoSrc) {
      vid.src = videoSrc;
      vid.style.display = "block";
      vid.classList.add("show");
      vid.currentTime = 0;

      const p = vid.play();
      if (p && typeof p.catch === "function") {
        p.catch(() => {
          if (vid) { vid.classList.remove("show"); vid.style.display = "none"; }
          showGifFallback();
        });
      }
      vid.onerror = () => {
        if (vid) { vid.classList.remove("show"); vid.style.display = "none"; }
        showGifFallback();
      };
      return;
    }

    showGifFallback();

    function showGifFallback() {
      if (!gif) return;
      gif.src = COMPLETION_GIF_MAP[level] || "./assets/img/robo.gif";
      gif.style.display = "block";
      setTimeout(() => gif.classList.add("show"), 10);
    }
  }

  function render() {
    const q = QUESTIONS[level]?.[index];
    if (!q) return finish();

    const num = $("questionNum");
    const title = $("questionTitle");
    const text = $("questionText");
    const options = $("options");

    if (num) num.textContent = `Q${index + 1}/${TOTAL}`;
    if (title) title.textContent = q.title;
    if (text) text.textContent = q.text;

    if (!options) return;
    options.innerHTML = "";
    locked = false;

    q.options.forEach((opt, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "option-btn";
      btn.textContent = opt;
      btn.onclick = () => choose(i);
      options.appendChild(btn);
    });
  }

  function mark(correctIdx, selectedIdx) {
    const buttons = document.querySelectorAll(".option-btn");
    buttons.forEach((b, idx) => {
      b.classList.remove("correct", "wrong");
      if (idx === correctIdx) b.classList.add("correct");
      if (idx === selectedIdx && selectedIdx !== correctIdx) b.classList.add("wrong");
    });
  }

  function disableOptions(disabled) {
    document.querySelectorAll(".option-btn").forEach((b) => {
      if (disabled) b.setAttribute("disabled", "true");
      else b.removeAttribute("disabled");
    });
  }

  function choose(selectedIdx) {
    if (locked) return;
    locked = true;

    const q = QUESTIONS[level][index];
    if (!q) return;

    disableOptions(true);
    mark(q.correct, selectedIdx);

    const isCorrect = selectedIdx === q.correct;
    if (!isCorrect) {
      speak("틀렸어요! 다시 도전해봐요!");
      setTimeout(() => {
        locked = false;
        disableOptions(false);
      }, 450);
      return;
    }

    correctCount += 1;

    const gain = Math.ceil((100 - START_BATTERY) / TOTAL);
    setBattery(battery + gain);

    setTimeout(() => {
      index += 1;
      if (index >= TOTAL) finish();
      else render();
    }, 650);
  }

  function finish() {
    setBattery(100);

    const qbox = $("questionBox");
    const complete = $("completionScreen");
    const finalScore = $("finalScore");

    if (qbox) qbox.style.display = "none";
    if (complete) complete.classList.add("show");
    if (finalScore) finalScore.textContent = `정답: ${correctCount} / ${TOTAL}   (배터리 100% ⚡)`;

    showCompletionMedia();
    speak("축하해! 고마워! 나를 구해줘서!");
  }

  function startGame(nextLevel) {
    if (!QUESTIONS[nextLevel] || QUESTIONS[nextLevel].length < TOTAL) {
      console.error("❌ 해당 레벨 문제(10개)가 부족합니다:", nextLevel);
      return;
    }

    level = nextLevel;
    index = 0;
    correctCount = 0;
    locked = false;

    showGame();

    const qbox = $("questionBox");
    const complete = $("completionScreen");
    if (qbox) qbox.style.display = "block";
    if (complete) complete.classList.remove("show");

    showRobotImage();

    const img = $("robotImg");
    if (img) img.src = getRobotImageForLevel(level);

    setBattery(START_BATTERY);
    render();
  }

  function resetGame() {
    showLevel();

    const qbox = $("questionBox");
    const complete = $("completionScreen");
    const options = $("options");

    if (qbox) qbox.style.display = "block";
    if (complete) complete.classList.remove("show");
    if (options) options.innerHTML = "";

    showRobotImage();

    const img = $("robotImg");
    if (img) img.src = "./assets/img/robo2.png";

    setBattery(START_BATTERY);
  }

  function goHome() {
    window.location.href = "index.html";
  }

  window.startGame = startGame;
  window.resetGame = resetGame;
  window.goHome = goHome;

  document.addEventListener("DOMContentLoaded", () => {
    setBattery(START_BATTERY);
  });
})();
