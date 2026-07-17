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

  function slugify(text, fallback) {
    const ascii = text
      .toLowerCase()
      .replace(/&[a-z]+;/g, "")
      .replace(/[^\w\u4e00-\u9fa5]+/g, "-")
      .replace(/^-+|-+$/g, "");
    return ascii || fallback;
  }

  function buildToc() {
    const headings = Array.from(main.querySelectorAll("h2, h3"))
      .filter((heading) => !heading.closest(".summary"));

    if (headings.length < 3) {
      return;
    }

    const layout = document.createElement("div");
    layout.className = "tutorial-layout";
    main.parentNode.insertBefore(layout, main);
    layout.appendChild(main);

    const toggle = document.createElement("button");
    toggle.className = "toc-toggle";
    toggle.type = "button";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", "tutorial-toc");
    toggle.innerHTML = '<span aria-hidden="true">☰</span><span>目录</span>';

    const mask = document.createElement("div");
    mask.className = "toc-mask";

    const aside = document.createElement("aside");
    aside.className = "toc-drawer";
    aside.id = "tutorial-toc";
    aside.setAttribute("aria-label", "文章目录");

    const close = document.createElement("button");
    close.className = "toc-close";
    close.type = "button";
    close.setAttribute("aria-label", "收起目录");
    close.textContent = "×";

    const list = document.createElement("ol");
    list.className = "toc-list";

    const tocLinks = [];
    headings.forEach((heading, index) => {
      if (!heading.id) {
        heading.id = slugify(heading.textContent.trim(), `section-${index + 1}`);
      }

      const item = document.createElement("li");
      item.className = "toc-item";

      const link = document.createElement("a");
      link.className = `toc-link toc-link-${heading.tagName.toLowerCase()}`;
      link.href = `#${heading.id}`;
      link.textContent = heading.textContent.trim();
      link.dataset.targetId = heading.id;
      link.dataset.index = String(index);
      link.addEventListener("click", () => {
        if (window.innerWidth <= 1180) {
          closeDrawer();
        }
      });

      tocLinks.push(link);
      item.appendChild(link);
      list.appendChild(item);
    });

    const header = document.createElement("div");
    header.className = "toc-drawer-header";
    header.innerHTML = '<div class="toc-drawer-title">本页目录</div>';
    header.appendChild(close);
    aside.appendChild(header);
    aside.appendChild(list);

    document.body.appendChild(toggle);
    document.body.appendChild(mask);
    layout.insertBefore(aside, main);

    function openDrawer() {
      document.body.classList.add("toc-open");
      toggle.setAttribute("aria-expanded", "true");
    }

    function closeDrawer() {
      document.body.classList.remove("toc-open");
      toggle.setAttribute("aria-expanded", "false");
    }

    toggle.addEventListener("click", () => {
      if (document.body.classList.contains("toc-open")) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });

    close.addEventListener("click", closeDrawer);
    mask.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeDrawer();
      }
    });

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);

        if (!visible.length) {
          return;
        }

        const activeId = visible[0].target.id;
        const activeIndex = tocLinks.findIndex((link) => link.dataset.targetId === activeId);
        if (activeIndex === -1) {
          return;
        }

        tocLinks.forEach((link, index) => {
          link.classList.toggle("toc-link-active", index === activeIndex);
          link.classList.toggle("toc-link-passed", index < activeIndex);
        });
      },
      {
        rootMargin: "-18% 0px -62% 0px",
        threshold: [0, 1],
      }
    );

    headings.forEach((heading) => observer.observe(heading));
    tocLinks[0].classList.add("toc-link-active");
  }

  main.prepend(createNav("top"));
  main.append(createNav("bottom"));
  buildToc();
})();
