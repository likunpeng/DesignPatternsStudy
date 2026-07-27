(function () {
  const STORAGE_KEY = "design-pattern-progress";

  // 计算当前页在 PATTERN_DATA 中的 key（与 tutorial-nav.js 保持一致）
  const path = window.location.pathname;
  const studyPathIndex = path.indexOf("/study/");
  const currentPath = studyPathIndex === -1
    ? path.replace(/^\/+/, "")
    : path.slice(studyPathIndex + 7);

  const patterns = window.PATTERN_DATA || [];
  const current = patterns.find((p) => p.file === currentPath);
  if (!current) return;
  const fileKey = current.file;

  // ---- 样式（自包含，避免改动 tutorial.css）----
  const style = document.createElement("style");
  style.textContent = `
    .learn-toast {
      position: fixed;
      left: 50%;
      bottom: 28px;
      transform: translateX(-50%) translateY(20px);
      background: #1e293b;
      border: 1px solid #334155;
      color: #f8fafc;
      padding: 12px 16px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      gap: 14px;
      box-shadow: 0 12px 40px rgba(0,0,0,.45);
      opacity: 0;
      pointer-events: none;
      transition: opacity .3s, transform .3s;
      z-index: 9999;
      font-size: .9rem;
      max-width: calc(100vw - 32px);
    }
    .learn-toast.show {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
      pointer-events: auto;
    }
    .learn-toast-undo {
      background: transparent;
      border: 1px solid #475569;
      color: #cbd5e1;
      border-radius: 8px;
      padding: 6px 12px;
      cursor: pointer;
      font-family: inherit;
      font-size: .82rem;
      flex-shrink: 0;
    }
    .learn-toast-undo:hover { border-color: #34d399; color: #34d399; }
    .learn-fab {
      position: fixed;
      right: 22px;
      bottom: 22px;
      z-index: 9998;
      background: #4f46e5;
      color: #fff;
      border: none;
      border-radius: 999px;
      padding: 12px 20px;
      font-size: .9rem;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      box-shadow: 0 10px 30px rgba(79,70,229,.45);
      transition: transform .15s, background .2s, color .2s, box-shadow .2s;
    }
    .learn-fab:hover { transform: translateY(-2px); }
    .learn-fab.done {
      background: #064e3b;
      color: #34d399;
      border: 1px solid #059669;
      box-shadow: 0 10px 30px rgba(16,185,129,.35);
    }
    @media (max-width: 1180px) {
      .learn-fab { bottom: 80px; }
      .learn-toast { bottom: 80px; }
    }
  `;
  document.head.appendChild(style);

  // ---- 存储 ----
  function load() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); }
    catch { return {}; }
  }
  function save(data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }
  function isLearned() {
    const d = load();
    return !!(d[fileKey] && d[fileKey].status === "learned");
  }

  // ---- Toast ----
  let toastTimer = null;
  function showToast() {
    let toast = document.getElementById("learn-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "learn-toast";
      toast.className = "learn-toast";
      document.body.appendChild(toast);
    }
    toast.innerHTML =
      '<span>🎉 已到达文末，自动标记为已学</span>' +
      '<button type="button" class="learn-toast-undo">撤销</button>';
    toast.querySelector(".learn-toast-undo").onclick = () => {
      undo();
      hideToast();
    };
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(hideToast, 6000);
  }
  function hideToast() {
    const toast = document.getElementById("learn-toast");
    if (toast) toast.classList.remove("show");
  }

  // ---- 标记 / 撤销 ----
  function markLearned() {
    const d = load();
    d[fileKey] = { status: "learned", date: new Date().toISOString().split("T")[0] };
    save(d);
    current.status = "learned";
    showToast();
    updateFab();
  }
  function undo() {
    const d = load();
    if (d[fileKey]) {
      d[fileKey].status = "pending";
      d[fileKey].date = null;
    }
    save(d);
    current.status = "pending";
    updateFab();
  }

  // ---- 浮动按钮 ----
  function ensureFab() {
    let fab = document.getElementById("learn-fab");
    if (fab) return fab;
    fab = document.createElement("button");
    fab.id = "learn-fab";
    fab.type = "button";
    fab.className = "learn-fab";
    fab.addEventListener("click", () => {
      if (isLearned()) undo();
      else markLearned();
    });
    document.body.appendChild(fab);
    return fab;
  }
  function updateFab() {
    const fab = document.getElementById("learn-fab");
    if (!fab) return;
    if (isLearned()) {
      fab.classList.add("done");
      fab.textContent = "✓ 已学完";
    } else {
      fab.classList.remove("done");
      fab.textContent = "标记已学";
    }
  }

  // ---- 滚动检测：到达文末 92% 视为读完 ----
  let ticking = false;
  let autoMarked = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      if (autoMarked) return;
      const scrollY = window.scrollY || window.pageYOffset || 0;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      // 内容可滚动且已读至 92% 才自动标记；避免短页面/打开即底部误判
      if (docHeight > 100 && scrollY >= docHeight * 0.92) {
        autoMarked = true;
        if (!isLearned()) markLearned();
      }
    });
  }

  ensureFab();
  updateFab();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  onScroll();
})();
