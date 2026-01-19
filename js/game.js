File: js/game.js
- A1/A2 only
- 10 questions each
- Left frame: danger (red blink + ring)
- On 10 correct: frame turns green + video plays
========================================================= */
(() => {
  "use strict";

  const START_BATTERY = 3;
  const TOTAL = 10;

  // ✅ 영상 파일은 여기만 바꾸시면 됩니다.
  // - repo에 assets/videos/a1.mp4 / a2.mp4 업로드 권장
  // - 없으면 자동으로 gif로 fallback 됩니다.
  const VIDEO_MAP = {
    A1: "./assets/videos/a1.mp4",
    A2: "./assets/videos/a2.mp4",
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

  function setBattery(value) {
    battery = clamp(value, 0, 100);

    const percent = $("batteryPercent");
    const fill = $("batteryFill");
    if (percent) percent.textContent = String(battery);
    if (fill) fill.style.width = `${battery}%`;

    const headerDesc = $("headerDesc");
    if (headerDesc) headerDesc.classList.toggle("alert", battery <= 10);
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

  function setFrameDanger() {
    const frame = $("robotFrame");
    if (!frame) return;
    frame.classList.add("is-danger");
    frame.classList.remove("is-complete");
  }

  function setFrameComplete() {
    const frame = $("robotFrame");
    if (!frame) return;
    frame.classList.remove("is-danger");
    frame.classList.add("is-complete");
  }

  function showRobotImage() {
    const img = $("robotImg");
    const gif = $("robotGif");
    const vid = $("robotVideo");
    if (img) img.style.display = "block";
    if (gif) { gif.classList.remove("show"); gif.style.display = "none"; }
    if (vid) { vid.classList.remove("show"); vid.style.display = "none"; vid.pause(); }
  }

  function showRobotVideoOrFallback() {
    const img = $("robotImg");
    const gif = $("robotGif");
    const vid = $("robotVideo");

    if (img) img.style.display = "none";

    const videoSrc = VIDEO_MAP[level];
    if (vid && videoSrc) {
      vid.src = videoSrc;
      vid.style.display = "block";
      vid.classList.add("show");
      vid.currentTime = 0;

      const playPromise = vid.play();
      if (playPromise && typeof playPromise.catch === "function") {
        playPromise.catch(() => {
          // autoplay 정책 등으로 실패 -> fallback
          if (vid) { vid.classList.remove("show"); vid.style.display = "none"; }
          if (gif) {
            gif.src = "./assets/img/robo.gif";
            gif.style.display = "block";
            setTimeout(() => gif.classList.add("show"), 10);
          }
        });
      }
      // 비디오 파일 404/로드 실패 -> fallback
      vid.onerror = () => {
        if (vid) { vid.classList.remove("show"); vid.style.display = "none"; }
        if (gif) {
          gif.src = "./assets/img/robo.gif";
          gif.style.display = "block";
          setTimeout(() => gif.classList.add("show"), 10);
        }
      };
      return;
    }

    // no video element or map -> fallback gif
    if (gif) {
      gif.src = "./assets/img/robo.gif";
      gif.style.display = "block";
      setTimeout(() => gif.classList.add("show"), 10);
    }
  }

  function setRobotLevelImage() {
    const img = $("robotImg");
    if (!img) return;
    img.src = "./assets/img/robo2.png";
  }

  function render() {
    const q = QUESTIONS[level][index];
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

    const gain = Math.ceil((100 - START_BATTERY) / TOTAL); // 10
    setBattery(battery + gain);

    setTimeout(() => {
      index += 1;
      if (index >= TOTAL) finish();
      else render();
    }, 650);
  }

  function finish() {
    setBattery(100);
    setFrameComplete();

    const qbox = $("questionBox");
    const complete = $("completionScreen");
    const finalScore = $("finalScore");

    if (qbox) qbox.style.display = "none";
    if (complete) complete.classList.add("show");
    if (finalScore) finalScore.textContent = `최종 배터리: 100% ⚡  완벽해! 넌 진짜 최고야!`;

    showRobotVideoOrFallback();
    const headerDesc = $("headerDesc");
    if (headerDesc) headerDesc.classList.remove("alert");

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
    setFrameDanger();
    setBattery(START_BATTERY);

    const qbox = $("questionBox");
    const complete = $("completionScreen");
    if (qbox) qbox.style.display = "block";
    if (complete) complete.classList.remove("show");

    showRobotImage();
    setRobotLevelImage();

    const headerDesc = $("headerDesc");
    if (headerDesc) headerDesc.classList.add("alert");

    render();
  }

  function resetGame() {
    showLevel();
    setFrameDanger();
    setBattery(START_BATTERY);

    const qbox = $("questionBox");
    const complete = $("completionScreen");
    const options = $("options");

    if (qbox) qbox.style.display = "block";
    if (complete) complete.classList.remove("show");
    if (options) options.innerHTML = "";

    showRobotImage();

    const headerDesc = $("headerDesc");
    if (headerDesc) headerDesc.classList.remove("alert");
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
