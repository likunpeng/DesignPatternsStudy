# 设计模式教程项目 · 长期约定

## 教程写作风格（用户明确要求）
- 生活类比优先用**具体实物/物理口**（如 USB-C ↔ HDMI），不要用 `show`/`project`/`play` 这类抽象方法名当类比——初学者觉得不好理解。
- 全文保持**一套故事线**：生活类比的场景 == 代码例的场景，且方法命名要能互相印证（如物理口 → `receiveUsbC`/`receiveHdmi`）。混用不同领域或抽象方法名会明显增加认知负担。
- "这个模式解决什么问题"一节要**直接陈述主角处境**，不要堆"前因/触发/后果"叙事铺垫。
- 真实业务场景（如支付 SDK）只作文末"延伸小注"，明确标注为非主线，避免分裂心智模型。
- 文件被外部频繁改动时，用 Python 脚本一次性读改写（正则/整块替换）比多次 Edit 更稳，避免 "modified since read"。
- 全景/索引类文章里出现的每一个模式名，都应加超链接跳转到对应模式笔记（如 `../creational/singleton-pattern.html`），包括表格单元格、`th` 标题、SVG 图中的文字。链接用 `class="pattern-link"`（accent 色、无下划线、hover 显示底线）。目标文件以 `learning-progress.md` 与实际目录为准。

## 目录结构
- 笔记按分类放 `creational/` `structural/` `behavioral/` `fundamentals/`；CSS 主题色：前置灰 `#4b5563`、创建蓝 `#2563eb`、结构绿 `#16805f`、行为紫 `#7c3aed`。
- 每学完一个模式须更新 `learning-progress.md`。
