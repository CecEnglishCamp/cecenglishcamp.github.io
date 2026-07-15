(function () {
  "use strict";
  // Include on Reading / Writing pages. Renders a validated "back to roadmap" link
  // into an element with id="rm-return". Accepts only same-origin internal paths.
  function safeReturn(raw) {
    if (!raw) return null;
    var v;
    try { v = decodeURIComponent(raw); } catch (e) { return null; }
    v = v.trim();
    // Must be a root-relative path, and must NOT be protocol-relative or backslash-based.
    if (v.charAt(0) !== "/") return null;      // block absolute URLs (http://, mailto:, etc.)
    if (v.charAt(1) === "/") return null;      // block //evil.com (protocol-relative)
    if (v.indexOf("\\") !== -1) return null;   // block backslash tricks
    if (/^\/+\\/.test(v)) return null;         // block /\evil.com
    return v;
  }

  function init() {
    var slot = document.getElementById("rm-return");
    if (!slot) return;
    var raw = new URLSearchParams(location.search).get("return");
    var href = safeReturn(raw) || "/learning-roadmap/";
    var a = document.createElement("a");
    a.href = href;
    a.className = "rm-return-link";
    a.textContent = "← Learning Roadmap으로 돌아가기";
    slot.appendChild(a);
  }
  document.addEventListener("DOMContentLoaded", init);
  window.CEC_safeReturn = safeReturn;
})();
