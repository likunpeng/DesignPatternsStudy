#!/usr/bin/env python3
"""
批量更新所有设计模式学习笔记 HTML 文件的 CSS 样式，使其统一。
"""
import os
import re
import glob

BASE_DIR = "/Users/likunpeng/Documents/AI/study"

# 统一的 CSS 模板（按类别区分 accent 色）
TEMPLATES = {
    "fundamentals": """    :root {
      color-scheme: light;
      --bg: #f8fafc;
      --paper: #ffffff;
      --ink: #1e293b;
      --muted: #64748b;
      --line: #e2e8f0;
      --accent: #475569;
      --accent-soft: #f1f5f9;
      --code-bg: #1e293b;
      --code-ink: #f8fafc;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
    }

    main {
      width: min(980px, calc(100% - 32px));
      margin: 32px auto;
      padding: 40px;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, .08);
    }

    h1, h2, h3 { line-height: 1.25; color: var(--ink); }
    h1 { margin: 0 0 12px; font-size: clamp(2rem, 4vw, 3.2rem); letter-spacing: -0.04em; }
    h2 { margin-top: 44px; padding-top: 20px; border-top: 1px solid var(--line); font-size: 1.55rem; }
    h3 { margin-top: 28px; font-size: 1.18rem; }
    p { margin: 12px 0; }
    ul { padding-left: 1.25rem; }
    li { margin: 6px 0; }

    code {
      padding: 0.14rem 0.32rem;
      border-radius: 5px;
      background: var(--accent-soft);
      color: var(--accent);
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 0.92em;
    }

    pre {
      overflow: auto;
      padding: 18px 20px;
      border-radius: 12px;
      background: var(--code-bg);
      color: var(--code-ink);
      line-height: 1.6;
    }

    pre code { padding: 0; background: transparent; color: inherit; font-size: 0.9rem; }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow: hidden;
      background: #fff;
    }

    th, td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }

    th { background: var(--accent-soft); color: var(--accent); font-weight: 700; }
    tr:last-child td { border-bottom: 0; }

    .lead { max-width: 780px; color: var(--muted); font-size: 1.08rem; }
    .meta { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0 30px; }
    .tag {
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 0.9rem;
    }
    .note {
      margin: 18px 0;
      padding: 16px 18px;
      border-left: 5px solid var(--accent);
      border-radius: 10px;
      background: var(--accent-soft);
    }
    .summary { margin-top: 28px; padding: 20px; border-radius: 14px; background: var(--accent-soft); }

    @media (max-width: 680px) {
      main { width: min(100% - 18px, 980px); margin: 10px auto; padding: 22px 16px; border-radius: 14px; }
      table { display: block; overflow-x: auto; }
    }""",
    "creational": """    :root {
      color-scheme: light;
      --bg: #f8fafc;
      --paper: #ffffff;
      --ink: #1e293b;
      --muted: #64748b;
      --line: #e2e8f0;
      --accent: #4f46e5;
      --accent-soft: #eef2ff;
      --code-bg: #1e293b;
      --code-ink: #f8fafc;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
    }

    main {
      width: min(980px, calc(100% - 32px));
      margin: 32px auto;
      padding: 40px;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, .08);
    }

    h1, h2, h3 { line-height: 1.25; color: var(--ink); }
    h1 { margin: 0 0 12px; font-size: clamp(2rem, 4vw, 3.2rem); letter-spacing: -0.04em; }
    h2 { margin-top: 44px; padding-top: 20px; border-top: 1px solid var(--line); font-size: 1.55rem; }
    h3 { margin-top: 28px; font-size: 1.18rem; }
    p { margin: 12px 0; }
    ul { padding-left: 1.25rem; }
    li { margin: 6px 0; }

    code {
      padding: 0.14rem 0.32rem;
      border-radius: 5px;
      background: var(--accent-soft);
      color: var(--accent);
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 0.92em;
    }

    pre {
      overflow: auto;
      padding: 18px 20px;
      border-radius: 12px;
      background: var(--code-bg);
      color: var(--code-ink);
      line-height: 1.6;
    }

    pre code { padding: 0; background: transparent; color: inherit; font-size: 0.9rem; }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow: hidden;
      background: #fff;
    }

    th, td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }

    th { background: var(--accent-soft); color: var(--accent); font-weight: 700; }
    tr:last-child td { border-bottom: 0; }

    .lead { max-width: 780px; color: var(--muted); font-size: 1.08rem; }
    .meta { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0 30px; }
    .tag {
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 0.9rem;
    }
    .note {
      margin: 18px 0;
      padding: 16px 18px;
      border-left: 5px solid var(--accent);
      border-radius: 10px;
      background: var(--accent-soft);
    }
    .summary { margin-top: 28px; padding: 20px; border-radius: 14px; background: var(--accent-soft); }

    @media (max-width: 680px) {
      main { width: min(100% - 18px, 980px); margin: 10px auto; padding: 22px 16px; border-radius: 14px; }
      table { display: block; overflow-x: auto; }
    }""",
    "structural": """    :root {
      color-scheme: light;
      --bg: #f8fafc;
      --paper: #ffffff;
      --ink: #1e293b;
      --muted: #64748b;
      --line: #e2e8f0;
      --accent: #059669;
      --accent-soft: #ecfdf5;
      --code-bg: #1e293b;
      --code-ink: #f8fafc;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
    }

    main {
      width: min(980px, calc(100% - 32px));
      margin: 32px auto;
      padding: 40px;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, .08);
    }

    h1, h2, h3 { line-height: 1.25; color: var(--ink); }
    h1 { margin: 0 0 12px; font-size: clamp(2rem, 4vw, 3.2rem); letter-spacing: -0.04em; }
    h2 { margin-top: 44px; padding-top: 20px; border-top: 1px solid var(--line); font-size: 1.55rem; }
    h3 { margin-top: 28px; font-size: 1.18rem; }
    p { margin: 12px 0; }
    ul { padding-left: 1.25rem; }
    li { margin: 6px 0; }

    code {
      padding: 0.14rem 0.32rem;
      border-radius: 5px;
      background: var(--accent-soft);
      color: var(--accent);
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 0.92em;
    }

    pre {
      overflow: auto;
      padding: 18px 20px;
      border-radius: 12px;
      background: var(--code-bg);
      color: var(--code-ink);
      line-height: 1.6;
    }

    pre code { padding: 0; background: transparent; color: inherit; font-size: 0.9rem; }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow: hidden;
      background: #fff;
    }

    th, td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }

    th { background: var(--accent-soft); color: var(--accent); font-weight: 700; }
    tr:last-child td { border-bottom: 0; }

    .lead { max-width: 780px; color: var(--muted); font-size: 1.08rem; }
    .meta { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0 30px; }
    .tag {
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 0.9rem;
    }
    .note {
      margin: 18px 0;
      padding: 16px 18px;
      border-left: 5px solid var(--accent);
      border-radius: 10px;
      background: var(--accent-soft);
    }
    .summary { margin-top: 28px; padding: 20px; border-radius: 14px; background: var(--accent-soft); }

    @media (max-width: 680px) {
      main { width: min(100% - 18px, 980px); margin: 10px auto; padding: 22px 16px; border-radius: 14px; }
      table { display: block; overflow-x: auto; }
    }""",
    "behavioral": """    :root {
      color-scheme: light;
      --bg: #f8fafc;
      --paper: #ffffff;
      --ink: #1e293b;
      --muted: #64748b;
      --line: #e2e8f0;
      --accent: #7c3aed;
      --accent-soft: #f5f3ff;
      --code-bg: #1e293b;
      --code-ink: #f8fafc;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
    }

    main {
      width: min(980px, calc(100% - 32px));
      margin: 32px auto;
      padding: 40px;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, .08);
    }

    h1, h2, h3 { line-height: 1.25; color: var(--ink); }
    h1 { margin: 0 0 12px; font-size: clamp(2rem, 4vw, 3.2rem); letter-spacing: -0.04em; }
    h2 { margin-top: 44px; padding-top: 20px; border-top: 1px solid var(--line); font-size: 1.55rem; }
    h3 { margin-top: 28px; font-size: 1.18rem; }
    p { margin: 12px 0; }
    ul { padding-left: 1.25rem; }
    li { margin: 6px 0; }

    code {
      padding: 0.14rem 0.32rem;
      border-radius: 5px;
      background: var(--accent-soft);
      color: var(--accent);
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 0.92em;
    }

    pre {
      overflow: auto;
      padding: 18px 20px;
      border-radius: 12px;
      background: var(--code-bg);
      color: var(--code-ink);
      line-height: 1.6;
    }

    pre code { padding: 0; background: transparent; color: inherit; font-size: 0.9rem; }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      border: 1px solid var(--line);
      border-radius: 12px;
      overflow: hidden;
      background: #fff;
    }

    th, td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }

    th { background: var(--accent-soft); color: var(--accent); font-weight: 700; }
    tr:last-child td { border-bottom: 0; }

    .lead { max-width: 780px; color: var(--muted); font-size: 1.08rem; }
    .meta { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0 30px; }
    .tag {
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 0.9rem;
    }
    .note {
      margin: 18px 0;
      padding: 16px 18px;
      border-left: 5px solid var(--accent);
      border-radius: 10px;
      background: var(--accent-soft);
    }
    .summary { margin-top: 28px; padding: 20px; border-radius: 14px; background: var(--accent-soft); }

    @media (max-width: 680px) {
      main { width: min(100% - 18px, 980px); margin: 10px auto; padding: 22px 16px; border-radius: 14px; }
      table { display: block; overflow-x: auto; }
    }""",
}

# 按目录映射到类别
DIR_TO_CAT = {
    "fundamentals": "fundamentals",
    "creational": "creational",
    "structural": "structural",
    "behavioral": "behavioral",
}

CSS_PATTERN = re.compile(r'<style>.*?</style>', re.DOTALL)

def get_category(filepath):
    rel = os.path.relpath(filepath, BASE_DIR)
    parts = rel.split(os.sep)
    if len(parts) >= 2:
        return DIR_TO_CAT.get(parts[0], "fundamentals")
    return "fundamentals"

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cat = get_category(filepath)
    new_css = TEMPLATES[cat]

    # 替换 <style>...</style> 内容
    new_content = CSS_PATTERN.sub(f'<style>\n{new_css}\n  </style>', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Updated: {filepath} ({cat})")

def main():
    # 更新所有子目录下的 HTML
    for subdir in ["fundamentals", "creational", "structural", "behavioral"]:
        pattern = os.path.join(BASE_DIR, subdir, "*.html")
        for filepath in glob.glob(pattern):
            update_file(filepath)

if __name__ == "__main__":
    main()
