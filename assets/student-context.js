/* CEC English Camp · authorized student context (tab-scoped selection) */
(function () {
  'use strict';

  if (window.CECStudentContext &&
      typeof window.CECStudentContext.getStudentContext === 'function') {
    return;
  }

  var STORAGE_KEY = 'cec_student_context_v1';
  var STUDENT_PATH = '/robo/v1/learning/students';
  var PRODUCTION_BASE = 'https://cec-robo-router-production.cecenglishcamp.workers.dev';
  var PREVIEW_BASE = 'https://cec-robo-router-preview.cecenglishcamp.workers.dev';
  var memoryContext = null;
  var pendingContext = null;

  document.documentElement.classList.add('cec-student-context-pending');

  function isLoopback(hostname) {
    return hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1';
  }

  function workerBase() {
    var hostname = window.location && window.location.hostname;
    if (hostname === 'cecenglishcamp.com') return PRODUCTION_BASE;
    if (isLoopback(hostname)) return PREVIEW_BASE;
    return null;
  }

  function exactKeys(value, allowed) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
    var keys = Object.keys(value).sort();
    var expected = allowed.slice().sort();
    return keys.length === expected.length && keys.every(function (key, index) {
      return key === expected[index];
    });
  }

  function validStudent(student) {
    return exactKeys(student, ['id', 'display_name', 'grade_level']) &&
      typeof student.id === 'string' && student.id.length > 0 &&
      typeof student.display_name === 'string' && student.display_name.length > 0 &&
      (student.grade_level === null || typeof student.grade_level === 'string');
  }

  function validDiscovery(body) {
    if (!exactKeys(body, ['students', 'selection_mode']) || !Array.isArray(body.students)) return false;
    if (!body.students.every(validStudent)) return false;
    if (body.students.length === 0) return body.selection_mode === 'setup_required';
    if (body.students.length === 1) return body.selection_mode === 'auto';
    return body.selection_mode === 'choose';
  }

  function clearStoredSelection() {
    try { window.sessionStorage.removeItem(STORAGE_KEY); } catch (_error) { /* fail closed */ }
  }

  function storedSelection() {
    try {
      var value = window.sessionStorage.getItem(STORAGE_KEY);
      return typeof value === 'string' && value ? value : null;
    } catch (_error) {
      return null;
    }
  }

  function storeSelection(studentId) {
    try { window.sessionStorage.setItem(STORAGE_KEY, studentId); } catch (_error) { /* memory state remains valid */ }
  }

  function ensureGate() {
    var gate = document.getElementById('cec-student-context-gate');
    if (gate) return gate;
    gate = document.createElement('div');
    gate.id = 'cec-student-context-gate';
    gate.setAttribute('role', 'dialog');
    gate.setAttribute('aria-modal', 'true');
    gate.style.cssText = 'position:fixed;inset:0;z-index:2147483647;background:rgba(10,22,40,.78);display:flex;align-items:center;justify-content:center;padding:20px;font-family:Arial,sans-serif';
    var panel = document.createElement('div');
    panel.setAttribute('data-cec-student-panel', 'true');
    panel.style.cssText = 'width:min(420px,100%);background:#fff;border-radius:16px;padding:24px;box-shadow:0 20px 60px rgba(0,0,0,.28);color:#20301d';
    gate.appendChild(panel);
    document.body.appendChild(gate);
    return gate;
  }

  function gatePanel() {
    return ensureGate().querySelector('[data-cec-student-panel]');
  }

  function blockLearning() {
    var panel = gatePanel();
    panel.replaceChildren();
    var title = document.createElement('strong');
    title.textContent = '학생 학습 정보를 아직 사용할 수 없습니다.';
    var message = document.createElement('p');
    message.textContent = '학생 설정을 확인한 후 다시 시도해 주세요.';
    message.style.marginBottom = '0';
    panel.appendChild(title);
    panel.appendChild(message);
    return { status: 'blocked', selectionMode: 'setup_required', student: null };
  }

  function unlockLearning() {
    document.documentElement.classList.remove('cec-student-context-pending');
    document.body.removeAttribute('aria-busy');
    var gate = document.getElementById('cec-student-context-gate');
    if (gate) gate.remove();
  }

  function ready(selectionMode, student) {
    memoryContext = Object.freeze({
      status: 'ready',
      selectionMode: selectionMode,
      student: Object.freeze({
        id: student.id,
        display_name: student.display_name,
        grade_level: student.grade_level
      })
    });
    unlockLearning();
    return memoryContext;
  }

  function chooseStudent(students) {
    var storedId = storedSelection();
    var storedStudent = storedId && students.find(function (student) { return student.id === storedId; });
    if (storedStudent) return Promise.resolve(ready('choose', storedStudent));
    if (storedId) clearStoredSelection();

    var panel = gatePanel();
    panel.replaceChildren();
    var title = document.createElement('strong');
    title.textContent = '학습할 학생을 선택해 주세요.';
    var list = document.createElement('div');
    list.style.cssText = 'display:grid;gap:10px;margin-top:16px';
    panel.appendChild(title);
    panel.appendChild(list);

    return new Promise(function (resolve) {
      students.forEach(function (student) {
        var button = document.createElement('button');
        button.type = 'button';
        button.textContent = student.display_name;
        button.style.cssText = 'padding:12px;border:1px solid #8aaa7d;border-radius:10px;background:#f4f9f1;color:#20301d;font-weight:700;cursor:pointer';
        button.addEventListener('click', function () {
          var authorizedStudent = students.find(function (candidate) { return candidate.id === student.id; });
          if (!authorizedStudent) return;
          storeSelection(authorizedStudent.id);
          resolve(ready('choose', authorizedStudent));
        });
        list.appendChild(button);
      });
    });
  }

  async function resolveContext() {
    document.body.setAttribute('aria-busy', 'true');
    if (!window.CECAuthSession || typeof window.CECAuthSession.getSession !== 'function') return blockLearning();

    var session;
    try { session = await window.CECAuthSession.getSession(); } catch (_error) { return blockLearning(); }
    if (!session || typeof session.access_token !== 'string' || !session.access_token) return blockLearning();

    var base = workerBase();
    if (!base) return blockLearning();
    var response;
    try {
      response = await window.fetch(base + STUDENT_PATH, {
        method: 'GET',
        headers: { 'Authorization': 'Bearer ' + session.access_token },
        cache: 'no-store'
      });
    } catch (_error) {
      return blockLearning();
    }
    if (!response || !response.ok) return blockLearning();

    var body;
    try { body = await response.json(); } catch (_error) { return blockLearning(); }
    if (!validDiscovery(body)) return blockLearning();
    if (body.students.length === 0) {
      clearStoredSelection();
      return blockLearning();
    }
    if (body.students.length === 1) {
      clearStoredSelection();
      return ready('auto', body.students[0]);
    }
    return chooseStudent(body.students);
  }

  function getStudentContext() {
    if (memoryContext) return Promise.resolve(memoryContext);
    if (!pendingContext) pendingContext = resolveContext();
    return pendingContext;
  }

  window.CECStudentContext = Object.freeze({ getStudentContext: getStudentContext });
})();
