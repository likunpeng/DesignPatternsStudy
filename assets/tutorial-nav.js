(function () {
  const patterns = window.PATTERN_DATA || [];
  const categories = window.PATTERN_CATEGORIES || [];
  const path = window.location.pathname;
  const currentPath = path.slice(path.indexOf("/study/") + 7);
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

  const nav = document.createElement("nav");
  nav.className = "page-nav";
  nav.setAttribute("aria-label", "教程导航");

  const items = [
    '<a href="../index.html">返回首页</a>',
    previous ? `<a href="../${previous.file}">上一篇：${previous.name}</a>` : '<span>上一篇：无</span>',
    category ? `<span class="page-nav-current">${category.zh}</span>` : "",
    next ? `<a href="../${next.file}">下一篇：${next.name}</a>` : '<span>下一篇：无</span>',
  ].filter(Boolean);

  nav.innerHTML = items.join("");
  main.prepend(nav);
})();
