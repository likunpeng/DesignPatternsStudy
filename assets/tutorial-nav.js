(function () {
  const patterns = window.PATTERN_DATA || [];
  const categories = window.PATTERN_CATEGORIES || [];
  const path = window.location.pathname;
  const studyPathIndex = path.indexOf("/study/");
  const currentPath = studyPathIndex === -1
    ? path.replace(/^\/+/, "")
    : path.slice(studyPathIndex + 7);
  const currentIndex = patterns.findIndex((pattern) => pattern.file === currentPath);

  if (currentIndex === -1) {
    return;
  }

  const current = patterns[currentIndex];
  const previous = patterns[currentIndex - 1] || null;
  const next = patterns[currentIndex + 1] || null;
  const category = categories.find((item) => item.key === current.cat);
  const main = document.querySelector("main");

  document.body.dataset.category = current.cat;

  if (!main) {
    return;
  }

  const items = [
    '<a href="../index.html">返回首页</a>',
    previous ? `<a href="../${previous.file}">上一篇：${previous.name}</a>` : '<span>上一篇：无</span>',
    category ? `<span class="page-nav-current">${category.zh}</span>` : "",
    next ? `<a href="../${next.file}">下一篇：${next.name}</a>` : '<span>下一篇：无</span>',
  ].filter(Boolean);

  if (main.querySelector(".page-nav[data-tutorial-nav]")) {
    return;
  }

  function createNav(position) {
    const nav = document.createElement("nav");
    nav.className = position === "bottom" ? "page-nav page-nav-bottom" : "page-nav";
    nav.dataset.tutorialNav = position;
    nav.setAttribute("aria-label", position === "bottom" ? "教程底部导航" : "教程导航");
    nav.innerHTML = items.join("");
    return nav;
  }

  main.prepend(createNav("top"));
  main.append(createNav("bottom"));
})();
