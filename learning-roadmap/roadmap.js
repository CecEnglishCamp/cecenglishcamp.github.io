(function () {
  "use strict";

  var GRADES = [3, 4, 5, 6];
  var WEEKS = 36;
  var DAY_ORDER = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
  var DAY_LABEL = {
    monday: ["월요일", "Monday"],
    tuesday: ["화요일", "Tuesday"],
    wednesday: ["수요일", "Wednesday"],
    thursday: ["목요일", "Thursday"],
    friday: ["금요일", "Friday"],
    saturday: ["토요일", "Saturday"]
  };
  var TYPE_LABEL = {
    "camp-a": "Camp A",
    "reading": "Reading",
    "listen-find": "Listen & Find",
    "look-speak": "Look & Speak",
    "writing": "Writing",
    "review": "Review"
  };
  var STATUS = {
    ready:   { badge: "ready",   text: "수업 열기" },
    pending: { badge: "pending", text: "준비 중" },
    coming:  { badge: "coming",  text: "곧 만나요" },
    locked:  { badge: "locked",  text: "구독 후 이용" }
  };

  function qs() {
    var p = new URLSearchParams(location.search);
    var g = parseInt(p.get("grade"), 10);
    var w = parseInt(p.get("week"), 10);
    if (GRADES.indexOf(g) === -1) g = 3;
    if (!(w >= 1 && w <= WEEKS)) w = 1;
    return { grade: g, week: w };
  }

  function pad(n) { return (n < 10 ? "0" : "") + n; }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function renderGrades(cur) {
    var nav = document.getElementById("rm-grades");
    nav.innerHTML = "";
    GRADES.forEach(function (g) {
      var b = el("button", "rm-grade-btn", "Grade " + g);
      b.type = "button";
      if (g === cur.grade) b.setAttribute("aria-current", "true");
      b.addEventListener("click", function () { go(g, 1); });
      nav.appendChild(b);
    });
  }

  function renderWeeks(cur) {
    var nav = document.getElementById("rm-weeks");
    nav.innerHTML = "";
    for (var w = 1; w <= WEEKS; w++) {
      (function (w) {
        var b = el("button", "rm-week-btn", String(w));
        b.type = "button";
        b.setAttribute("aria-label", "Week " + pad(w));
        if (w === cur.week) b.setAttribute("aria-current", "true");
        b.addEventListener("click", function () { go(cur.grade, w); });
        nav.appendChild(b);
      })(w);
    }
  }

  function pad2(n) { return (n < 10 ? "0" : "") + n; }

  // Read per-day completion (same key format mission.js writes)
  function dayDone(grade, week, day, items) {
    var done = {};
    try { done = JSON.parse(localStorage.getItem("cec:done:g" + grade + ":w" + pad2(week) + ":" + day) || "{}"); } catch (e) {}
    var required = [];
    items.forEach(function (it, idx) { if (it.status === "ready" && it.url) required.push(idx); });
    return required.length > 0 && required.every(function (idx) { return done[idx]; });
  }

  // Overview row: label + status badge only. Entry into a lesson happens via the day's mission.
  function itemNode(item) {
    var meta = STATUS[item.status] || STATUS.pending;
    var node = el("div", "rm-item is-overview" + (item.status === "ready" ? "" : " is-blocked"));
    node.appendChild(el("span", "rm-item-type", TYPE_LABEL[item.type] || item.type));
    var title = el("span", "rm-item-title", item.title);
    node.appendChild(title);
    node.appendChild(el("span", "rm-badge " + meta.badge, meta.text));
    return node;
  }

  function renderWeek(manifest, cur) {
    var main = document.getElementById("rm-week");
    main.innerHTML = "";

    var entry = null;
    for (var i = 0; i < manifest.weeks.length; i++) {
      if (manifest.weeks[i].week === cur.week) { entry = manifest.weeks[i]; break; }
    }
    if (!entry) {
      main.appendChild(el("p", "rm-error", "이 주차 정보는 아직 준비 중입니다."));
      return;
    }

    var head = el("div", "rm-week-head");
    head.appendChild(el("span", "rm-week-num", "Week " + pad(entry.week)));
    head.appendChild(el("span", "rm-week-book", entry.book || ""));
    head.appendChild(el("span", "rm-week-grade", "Grade " + cur.grade));
    main.appendChild(head);

    var days = el("div", "rm-days");
    DAY_ORDER.forEach(function (dk) {
      var items = (entry.days && entry.days[dk]) || [];
      if (!items.length) return;
      var done = dayDone(cur.grade, entry.week, dk, items);
      var day = el("div", "rm-day" + (done ? " is-done" : ""));

      var label = el("p", "rm-day-label", DAY_LABEL[dk][0]);
      label.appendChild(el("span", null, DAY_LABEL[dk][1]));
      if (done) label.appendChild(el("span", "rm-day-tick", "✓ 완료"));
      day.appendChild(label);

      var list = el("div", "rm-items");
      items.forEach(function (it) { list.appendChild(itemNode(it)); });
      day.appendChild(list);

      var enter = el("a", "rm-enter", done ? "다시 보기 →" : "들어가기 →");
      enter.href = "mission.html?grade=" + cur.grade + "&week=" + pad(entry.week) + "&day=" + dk;
      day.appendChild(enter);

      days.appendChild(day);
    });
    main.appendChild(days);
  }

  var cache = {};
  function loadManifest(grade) {
    if (cache[grade]) return Promise.resolve(cache[grade]);
    return fetch("manifests/grade" + grade + ".json", { cache: "no-cache" })
      .then(function (r) {
        if (!r.ok) throw new Error("manifest " + grade + " " + r.status);
        return r.json();
      })
      .then(function (json) { cache[grade] = json; return json; });
  }

  function render() {
    var cur = qs();
    renderGrades(cur);
    renderWeeks(cur);
    var main = document.getElementById("rm-week");
    main.innerHTML = '<p class="rm-loading">불러오는 중…</p>';
    loadManifest(cur.grade)
      .then(function (m) { renderWeek(m, cur); })
      .catch(function (err) {
        main.innerHTML = "";
        main.appendChild(el("p", "rm-error", "이 학년 로드맵을 불러오지 못했습니다."));
        if (window.console) console.error(err);
      });
  }

  function go(grade, week) {
    history.pushState(null, "", "?grade=" + grade + "&week=" + week);
    render();
  }

  window.addEventListener("popstate", render);
  document.addEventListener("DOMContentLoaded", render);
})();
