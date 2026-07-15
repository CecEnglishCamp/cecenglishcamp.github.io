(function () {
  "use strict";

  var GRADES = [3, 4, 5, 6];
  var WEEKS = 36;
  var DAY_ORDER = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
  var DAY_LABEL = {
    monday: ["월요일", "Monday"], tuesday: ["화요일", "Tuesday"],
    wednesday: ["수요일", "Wednesday"], thursday: ["목요일", "Thursday"],
    friday: ["금요일", "Friday"], saturday: ["토요일", "Saturday"]
  };
  var TYPE_LABEL = {
    "camp-a": "Camp A", "reading": "Reading", "listen-find": "Listen & Find",
    "look-speak": "Look & Speak", "writing": "Writing", "review": "Review"
  };
  var STATUS = {
    ready:   { badge: "ready",   text: "" },
    pending: { badge: "pending", text: "준비 중" },
    coming:  { badge: "coming",  text: "곧 만나요" },
    locked:  { badge: "locked",  text: "구독 후 이용" }
  };
  var BOOK_EMOJI = {
    "peter-rabbit": "🐰", "red-riding-hood": "🧺", "jack-and-the-beanstalk": "🌱",
    "frog-prince": "🐸", "elves-and-the-shoemaker": "👞", "thumbelina": "🌷",
    "emperors-new-clothes": "👑", "lucky-hans": "🍀", "velveteen-rabbit": "🧸"
  };

  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function el(t, c, tx) { var e = document.createElement(t); if (c) e.className = c; if (tx != null) e.textContent = tx; return e; }

  function params() {
    var p = new URLSearchParams(location.search);
    var g = parseInt(p.get("grade"), 10);
    var w = parseInt(p.get("week"), 10);
    var d = p.get("day");
    if (GRADES.indexOf(g) === -1) g = 3;
    if (!(w >= 1 && w <= WEEKS)) w = 1;
    if (DAY_ORDER.indexOf(d) === -1) {
      var map = ["monday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
      d = map[new Date().getDay()];
    }
    var done = parseInt(p.get("done"), 10);
    return { grade: g, week: w, day: d, done: (done >= 0 ? done : null) };
  }

  // Progress store — localStorage now, swap for Supabase Phase 2 (progress/attendance).
  function key(pm) { return "cec:done:g" + pm.grade + ":w" + pad(pm.week) + ":" + pm.day; }
  function getDone(pm) {
    try { return JSON.parse(localStorage.getItem(key(pm)) || "{}"); } catch (e) { return {}; }
  }
  function setDone(pm, obj) {
    try { localStorage.setItem(key(pm), JSON.stringify(obj)); } catch (e) {}
  }

  function selfLink(pm, path) {
    // internal-only return path back to this mission, marking item done on return
    return "/learning-roadmap/mission.html?grade=" + pm.grade + "&week=" + pad(pm.week) + "&day=" + pm.day;
  }

  function missionURL(grade, week, day) {
    return "/learning-roadmap/mission.html?grade=" + grade + "&week=" + pad(week) + "&day=" + day;
  }

  function render(manifest, pm) {
    var root = document.getElementById("mission");
    root.innerHTML = "";

    var entry = null;
    for (var i = 0; i < manifest.weeks.length; i++) {
      if (manifest.weeks[i].week === pm.week) { entry = manifest.weeks[i]; break; }
    }
    if (!entry) { root.appendChild(el("p", "rm-error", "이 주차는 아직 준비 중입니다.")); return; }

    var items = (entry.days && entry.days[pm.day]) || [];
    var done = getDone(pm);

    // apply "?done=i" marker from a returning resource, then clean the URL
    if (pm.done != null && items[pm.done] && items[pm.done].status === "ready") {
      done[pm.done] = true; setDone(pm, done);
      history.replaceState(null, "", missionURL(pm.grade, pm.week, pm.day));
    }

    var required = [];
    items.forEach(function (it, idx) { if (it.status === "ready" && it.url) required.push(idx); });
    var allDone = required.length > 0 && required.every(function (idx) { return done[idx]; });

    // ---- header
    var top = el("div", "mi-top");
    var back = el("a", "mi-back", "← Learning Roadmap");
    back.href = "/learning-roadmap/?grade=" + pm.grade + "&week=" + pad(pm.week);
    top.appendChild(back);
    root.appendChild(top);

    var head = el("header", "mi-head");
    head.appendChild(el("p", "mi-eyebrow", "TODAY'S MISSION"));
    var h = el("h1", "mi-title");
    h.appendChild(el("span", "mi-emoji", BOOK_EMOJI[entry.slug] || "📖"));
    h.appendChild(document.createTextNode(" " + (entry.book || "")));
    head.appendChild(h);
    head.appendChild(el("p", "mi-meta", "Week " + pad(entry.week) + " · Grade " + pm.grade + " · " + DAY_LABEL[pm.day][0]));
    root.appendChild(head);

    if (allDone) { root.appendChild(completePanel(pm, entry)); return; }

    // ---- checklist
    var intro = el("p", "mi-intro", "오늘은 아래 항목만 공부합니다.");
    root.appendChild(intro);

    var list = el("div", "mi-list");
    var firstOpen = -1;
    items.forEach(function (it, idx) {
      var meta = STATUS[it.status] || STATUS.pending;
      var isReady = it.status === "ready" && it.url;
      var isDone = !!done[idx];
      if (isReady && !isDone && firstOpen === -1) firstOpen = idx;

      var row = el("div", "mi-item" + (isDone ? " is-done" : "") + (isReady ? "" : " is-blocked"));

      var check = el("button", "mi-check", isDone ? "✓" : "");
      check.type = "button";
      check.setAttribute("aria-label", it.title + (isDone ? " 완료 취소" : " 완료 표시"));
      if (isReady) {
        check.addEventListener("click", function () {
          done[idx] = !done[idx]; setDone(pm, done); render(manifest, pm);
        });
      } else { check.disabled = true; }
      row.appendChild(check);

      var body = el("div", "mi-item-body");
      body.appendChild(el("span", "mi-item-type", TYPE_LABEL[it.type] || it.type));
      body.appendChild(el("span", "mi-item-title", it.title));
      row.appendChild(body);

      if (isReady) {
        var open = el("a", "mi-open", isDone ? "다시 열기" : "열기");
        var sep = it.url.indexOf("?") === -1 ? "?" : "&";
        open.href = it.url + sep + "return=" + encodeURIComponent(
          missionURL(pm.grade, pm.week, pm.day) + "&done=" + idx);
        row.appendChild(open);
      } else if (meta.text) {
        row.appendChild(el("span", "rm-badge " + meta.badge, meta.text));
      }
      list.appendChild(row);
    });
    root.appendChild(list);

    // ---- START (opens the first not-done ready item)
    if (firstOpen !== -1) {
      var cta = el("a", "mi-start", "Let's Go!  →");
      var it = items[firstOpen];
      var sep2 = it.url.indexOf("?") === -1 ? "?" : "&";
      cta.href = it.url + sep2 + "return=" + encodeURIComponent(
        missionURL(pm.grade, pm.week, pm.day) + "&done=" + firstOpen);
      root.appendChild(cta);
    }
  }

  function completePanel(pm, entry) {
    var isFriday = pm.day === "friday";
    var wrap = el("div", isFriday ? "mi-complete mi-week" : "mi-complete");
    wrap.appendChild(el("div", "mi-burst", isFriday ? "🎉" : "✅"));
    if (isFriday) {
      wrap.appendChild(el("h2", "mi-complete-title", "Congratulations!"));
      wrap.appendChild(el("p", "mi-complete-sub", "Week " + pad(entry.week) + " Complete"));
      wrap.appendChild(el("div", "mi-stars", "⭐⭐⭐⭐⭐"));
      var next = el("a", "mi-next", "다음 주로 가기  →");
      var nw = Math.min(entry.week + 1, WEEKS);
      next.href = "/learning-roadmap/?grade=" + pm.grade + "&week=" + pad(nw);
      wrap.appendChild(next);
    } else {
      wrap.appendChild(el("h2", "mi-complete-title", "잘했어요!"));
      wrap.appendChild(el("p", "mi-complete-sub", DAY_LABEL[pm.day][0] + " 학습을 끝냈습니다."));
      var back = el("a", "mi-next", "Learning Roadmap으로  →");
      back.href = "/learning-roadmap/?grade=" + pm.grade + "&week=" + pad(entry.week);
      wrap.appendChild(back);
    }
    var reset = el("button", "mi-reset", "다시 하기");
    reset.type = "button";
    reset.addEventListener("click", function () {
      try { localStorage.removeItem(key(pm)); } catch (e) {}
      location.href = missionURL(pm.grade, pm.week, pm.day);
    });
    wrap.appendChild(reset);
    return wrap;
  }

  var cache = {};
  function load(grade) {
    if (cache[grade]) return Promise.resolve(cache[grade]);
    return fetch("manifests/grade" + grade + ".json?t=" + Date.now(), { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error("manifest " + r.status); return r.json(); })
      .then(function (j) { cache[grade] = j; return j; });
  }

  function boot() {
    var pm = params();
    load(pm.grade)
      .then(function (m) { render(m, pm); })
      .catch(function (err) {
        document.getElementById("mission").innerHTML =
          '<p class="rm-error">미션을 불러오지 못했습니다.</p>';
        if (window.console) console.error(err);
      });
  }
  document.addEventListener("DOMContentLoaded", boot);
})();
