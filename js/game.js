
    let currentLevel = 'A1';
    let currentQuestion = 0;
    let battery = 3;
    let answered = false;
    let engineSoundPlayed = false;
    let questions = [];
    let missionStates = [];

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
      { title: "Conditional", text: "If I ___ time, I would help.", options: ["have", "had", "having"], correct: 1 },
      { title: "Comparative", text: "This book is ___ than that one.", options: ["more interesting", "interestinger", "interesting"], correct: 0 },
      { title: "Must/Might", text: "You ___ finish your homework.", options: ["must", "might", "can"], correct: 0 },
      { title: "Relative Clause", text: "The girl ___ won the prize.", options: ["who", "which", "whose"], correct: 0 },
      { title: "Passive Voice", text: "The letter was ___ by my sister.", options: ["write", "written", "writing"], correct: 1 },
      { title: "Gerund", text: "___ is good for health.", options: ["Exercise", "Exercising", "Exercises"], correct: 1 },
      { title: "Reported Speech", text: "She said she ___ a student.", options: ["is", "was", "were"], correct: 1 }
    ];

    const questionsB1 = [
      { title: "Complex Sentence", text: "Although tired, she ___.", options: ["continue", "continued", "continues"], correct: 1 },
      { title: "Perf Continuous", text: "I ___ English for 5 years.", options: ["study", "have studied", "have been studying"], correct: 2 },
      { title: "Subjunctive", text: "I suggest he ___ earlier.", options: ["come", "comes", "came"], correct: 0 },
      { title: "Inversion", text: "Never ___ I seen such beauty.", options: ["have", "had", "has"], correct: 0 },
      { title: "Participle", text: "___ by noise, I couldn't sleep.", options: ["Disturb", "Disturbing", "Disturbed"], correct: 2 },
      { title: "Cleft", text: "It is John ___ did the work.", options: ["who", "that", "which"], correct: 0 },
      { title: "Phrasal Verb", text: "They decided to ___ their trip.", options: ["put on", "put off", "put up"], correct: 1 },
      { title: "Collocation", text: "I ___ an important decision.", options: ["make", "do", "take"], correct: 0 },
      { title: "Idiom", text: "She's ___ a tough time.", options: ["going through", "going over", "going by"], correct: 0 },
      { title: "Advanced", text: "The project is said ___ soon.", options: ["to be", "being", "to have"], correct: 0 }
    ];

    const questionsB2 = [
      { title: "Mixed Conditional", text: "Had I known, I ___ you.", options: ["would contact", "would have contacted", "will contact"], correct: 1 },
      { title: "Hypothetical", text: "If you studied, you ___ pass.", options: ["would", "would be", "would have"], correct: 0 },
      { title: "Nominalization", text: "The ___ was delayed.", options: ["implement", "implementation", "implementing"], correct: 1 },
      { title: "Parallel", text: "She enjoys reading, writing, ___.", options: ["to speak", "speaking", "speak"], correct: 1 },
      { title: "Passive Advanced", text: "It is believed ___ change is real.", options: ["that", "which", "who"], correct: 0 },
      { title: "Discourse", text: "___ said, we must act.", options: ["In light of", "As a result", "Therefore"], correct: 0 },
      { title: "Ellipsis", text: "Who solved it? John ___.", options: ["did", "solved", "did solve"], correct: 0 },
      { title: "Hedging", text: "Results ___ suggest correlation.", options: ["might", "could", "appear to"], correct: 2 },
      { title: "Causative", text: "She had the mechanic ___ car.", options: ["repair", "to repair", "repaired"], correct: 0 },
      { title: "Vocabulary", text: "Proposal was met with ___.", options: ["resistance", "persist", "assistance"], correct: 0 }
    ];

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
        id: i,
        completed: false,
        triedOnce: false,
        usedBaseCamp: false
      }));

      document.getElementById('levelScreen').style.display = 'none';
      document.getElementById('gameScreen').classList.add('active');
      document.getElementById('questionBox').style.display = 'block';
      document.getElementById('completionScreen').classList.remove('show');

      const robotImg = document.getElementById('robotImg');
      const robotGif = document.getElementById('robotGif');
      robotImg.style.display = 'block';
      robotGif.style.display = 'none';
      robotGif.classList.remove('show');
      robotImg.classList.add('stage1');
      robotImg.classList.remove('stage2', 'stage3');

      displayQuestion();
      updateRobot();
    }

    function displayQuestion() {
      const q = questions[currentQuestion];
      document.getElementById("questionNum").textContent = `Q${currentQuestion + 1}/10`;
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

    function selectAnswer(selectedIdx) {
      if (answered) return;
      answered = true;

      const q = questions[currentQuestion];
      const buttons = document.querySelectorAll(".option-btn");
      const state = missionStates[currentQuestion];

      buttons[selectedIdx].classList.add(selectedIdx === q.correct ? "correct" : "wrong");
      buttons[q.correct].classList.add("correct");

      if (selectedIdx === q.correct) {
        if (!state.triedOnce) {
          battery = Math.min(battery + 10, 100);
          state.triedOnce = true;
        } else if (state.usedBaseCamp) {
          battery = Math.min(battery + 15, 100);
        }
        
        state.completed = true;
        updateRobot();
        
        if (battery >= 50) flashLight();

        setTimeout(() => {
          if (currentQuestion < 9) {
            currentQuestion++;
            displayQuestion();
          } else {
            completeGame();
          }
        }, 1500);
      } else {
        speak("틀렸어요! 다시 도전해봐요!");
        state.triedOnce = true;
        state.usedBaseCamp = true;
        
        setTimeout(() => { answered = false; }, 1500);
      }
    }

    function updateRobot() {
      const percent = document.getElementById("batteryPercent");
      const fill = document.getElementById("batteryFill");
      const robot = document.getElementById("robotContainer");
      const robotImg = document.getElementById("robotImg");

      percent.textContent = battery;
      fill.style.width = battery + "%";

      if (battery < 40) {
        robotImg.classList.add('stage1');
        robotImg.classList.remove('stage2', 'stage3');
        robot.classList.remove('stage2-vibrate');
      } else if (battery < 100) {
        robotImg.classList.add('stage2');
        robotImg.classList.remove('stage1', 'stage3');
        robot.classList.add('stage2-vibrate');
      } else {
        robotImg.classList.add('stage3');
        robotImg.classList.remove('stage1', 'stage2');
        robot.classList.remove('stage2-vibrate');
      }

      if (battery <= 30 && battery > 0) {
        robot.classList.add('warning');
        if (battery === 3 || battery === 13 || battery === 23) playWarningSound();
      } else {
        robot.classList.remove('warning');
      }

      if (battery >= 50 && battery < 80) {
        robot.classList.add('glow');
        robotImg.classList.add('glow');
        if (!engineSoundPlayed) { playEngineSound(); engineSoundPlayed = true; }
      } else if (battery < 50) {
        robot.classList.remove('glow');
        robotImg.classList.remove('glow');
      }

      if (battery >= 80 && battery < 100) {
        robot.classList.add('glow');
        robotImg.classList.add('glow');
        robot.style.animation = 'engineVibration 0.3s infinite';
      } else if (battery >= 50 && battery < 80) {
        robot.style.animation = 'none';
      }

      if (battery >= 100) {
        robot.classList.add('full');
        robot.classList.remove('warning');
        robotImg.classList.add('full');
        robot.style.animation = 'none';
      }
    }

    function completeGame() {
      battery = 100;
      updateRobot();
      const robotImg = document.getElementById('robotImg');
      const robotGif = document.getElementById('robotGif');
      const headerP = document.getElementById('headerDesc');

      robotImg.style.display = 'none';
      robotGif.style.display = 'block';
      setTimeout(() => robotGif.classList.add('show'), 10);

      if (headerP) headerP.classList.add('hide');

      document.getElementById('questionBox').style.display = 'none';
      document.getElementById('completionScreen').classList.add('show');
      document.getElementById('finalScore').textContent = `최종 배터리: 100% ⚡ 완벽해! 넌 진짜 최고야!`;

      speak("축하해! 고마워! 나를 구해줘서!");
    }

    function resetGame() {
      document.getElementById('levelScreen').style.display = 'flex';
      document.getElementById('gameScreen').classList.remove('active');
      const headerP = document.getElementById('headerDesc');
      if (headerP) headerP.classList.remove('hide');
    }

    function goHome() {
      window.location.href = 'index.html';
    }

    function flashLight() {
      const robot = document.getElementById('robotContainer');
      robot.classList.remove('light-flash');
      setTimeout(() => { robot.classList.add('light-flash'); }, 10);
    }

    function speak(text) {
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'ko-KR';
        window.speechSynthesis.speak(utterance);
      }
    }

    function playEngineSound() {
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(80, now);
        osc.frequency.exponentialRampToValueAtTime(100, now + 0.5);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.05, now + 0.5);
        osc.start(now);
        osc.stop(now + 0.5);
      } catch(e) {}
    }

    function playWarningSound() {
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(800, now);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.setValueAtTime(0, now + 0.2);
        osc.start(now);
        osc.stop(now + 0.2);
      } catch(e) {}
    }
  

