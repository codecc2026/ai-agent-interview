#!/usr/bin/env python3
"""从公众号原稿生成 GitHub Pages 用的 Docsify 站点副本。

只读取 ai-agent-interview-qa/articles/*.md，不修改原稿。
重复篇号保留 frontmatter date 较新的一篇。
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT.parent / "ai-agent-interview-qa" / "articles"
ARTICLES_DIR = ROOT / "articles"
QR_NAME = "wechat-qr.jpg"

FOOTER_TEMPLATE = """
---

## 关注公众号

更多 AI Agent 面试题在公众号持续更新。微信扫码关注 **FullStack 研发派**，后台回复「题库」，可以领取完整目录。

<img src="{src}" alt="FullStack 研发派" width="220" />
"""

@dataclass
class Article:
    source_name: str
    seq: int | None
    title: str
    chapter: str
    date: str
    body: str
    output_name: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"无法读取 {path}: {exc}") from exc


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text
    return parts[1], parts[2]


def field(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", frontmatter, re.M)
    if match is None:
        return ""
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value.strip()


def first_heading(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def md_label(text: str) -> str:
    return text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def keyword_slug(title: str, limit: int = 60) -> str:
    """把标题收成链接里的关键词，保留中英文，标点改成连字符。"""
    text = title.strip()
    if not text:
        return "untitled"
    text = re.sub(r"[\s　]+", "-", text)
    text = re.sub(r"[\\/:*?\"<>|#%&+=，。！？、；：“”‘’（）()\[\]【】《》…—·,.!?:;'\"`~]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-._")
    if len(text) > limit:
        text = text[:limit].rstrip("-._")
    return text or "untitled"


def output_filename(title: str, seq: int | None) -> str:
    slug = keyword_slug(title)
    if seq is None:
        return f"{slug}.md"
    return f"{seq:03d}-{slug}.md"


def unique_filename(name: str, used: set[str]) -> str:
    if name not in used:
        used.add(name)
        return name
    stem = name[:-3] if name.endswith(".md") else name
    suffix = name[-3:] if name.endswith(".md") else ""
    number = 2
    while True:
        candidate = f"{stem}-{number}{suffix}"
        if candidate not in used:
            used.add(candidate)
            return candidate
        number += 1


def prepare_body(body: str) -> str:
    return body.replace("明日预告", "预告")


def chapter_sort_key(name: str) -> tuple[int, str]:
    match = re.match(r"(\d+)", name)
    if match is None:
        return (10_000, name)
    return (int(match.group(1)), name)


def ensure_h1(body: str, title: str) -> str:
    lines = body.lstrip("\n").splitlines()
    if lines and lines[0].startswith("# ") and not lines[0].startswith("## "):
        return "\n".join(lines).rstrip() + "\n"
    heading = title.strip() or "未命名"
    rest = "\n".join(lines).lstrip("\n")
    if rest:
        return f"# {heading}\n\n{rest.rstrip()}\n"
    return f"# {heading}\n"


def with_footer(body: str, image_src: str) -> str:
    if QR_NAME in body:
        return body if body.endswith("\n") else body + "\n"
    footer = FOOTER_TEMPLATE.format(src=image_src).strip("\n")
    return body.rstrip() + "\n\n" + footer + "\n"


def load_articles() -> list[Article]:
    if not SOURCE_DIR.is_dir():
        raise SystemExit(f"找不到原稿目录: {SOURCE_DIR}")

    numbered: dict[int, Article] = {}
    specials: list[Article] = []
    skipped: list[str] = []

    paths = sorted(p for p in SOURCE_DIR.iterdir() if p.is_file() and p.suffix == ".md")
    if not paths:
        raise SystemExit(f"原稿目录里没有 Markdown: {SOURCE_DIR}")

    for path in paths:
        text = read_text(path).replace("\r\n", "\n")
        if not text.strip():
            print(f"跳过空文件: {path.name}", file=sys.stderr)
            continue
        frontmatter, body = split_frontmatter(text)
        seq_raw = field(frontmatter, "seq")
        title = field(frontmatter, "title") or first_heading(body) or path.stem
        chapter = field(frontmatter, "chapter")
        date = field(frontmatter, "date")
        published = ensure_h1(body, title)

        if seq_raw:
            try:
                seq = int(seq_raw)
            except ValueError:
                raise SystemExit(f"{path.name} 的 seq 不是整数: {seq_raw}")
            if seq <= 0:
                raise SystemExit(f"{path.name} 的 seq 必须大于 0: {seq}")
            article = Article(
                source_name=path.name,
                seq=seq,
                title=title,
                chapter=chapter or "未分类",
                date=date,
                body=published,
                output_name="",
            )
            current = numbered.get(seq)
            if current is None or (date, path.name) >= (current.date, current.source_name):
                if current is not None:
                    skipped.append(
                        f"篇号 {seq:03d} 保留 {path.name}（{date}），跳过 {current.source_name}（{current.date}）"
                    )
                numbered[seq] = article
            else:
                skipped.append(
                    f"篇号 {seq:03d} 保留 {current.source_name}（{current.date}），跳过 {path.name}（{date}）"
                )
            continue

        specials.append(
            Article(
                source_name=path.name,
                seq=None,
                title=title,
                chapter="专题",
                date=date,
                body=published,
                output_name="",
            )
        )

    for line in skipped:
        print(line)
    specials.sort(key=lambda item: (item.date, item.source_name))
    ordered = [numbered[seq] for seq in sorted(numbered)]
    articles = ordered + specials
    used: set[str] = set()
    for article in articles:
        article.output_name = unique_filename(output_filename(article.title, article.seq), used)
        if not article.output_name or "/" in article.output_name or article.output_name in {".", ".."}:
            raise SystemExit(f"生成了非法文件名: {article.source_name} -> {article.output_name!r}")
    return articles


def write_articles(articles: list[Article]) -> None:
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    for old in ARTICLES_DIR.glob("*.md"):
        old.unlink()
    for article in articles:
        target = ARTICLES_DIR / article.output_name
        if target.exists():
            raise SystemExit(f"输出文件名冲突: {article.output_name}")
        body = prepare_body(article.body)
        target.write_text(with_footer(body, f"../assets/{QR_NAME}"), encoding="utf-8")


def sidebar_markdown(articles: list[Article]) -> str:
    chapters: dict[str, list[Article]] = {}
    specials: list[Article] = []
    for article in articles:
        if article.seq is None:
            specials.append(article)
            continue
        chapters.setdefault(article.chapter, []).append(article)

    lines = ["- [首页](README.md)", ""]
    for name in sorted(chapters, key=chapter_sort_key):
        lines.append(f"- {name}")
        for article in chapters[name]:
            seq = article.seq or 0
            label = md_label(f"{seq:03d} {article.title}")
            lines.append(f"  - [{label}](articles/{article.output_name})")
        lines.append("")
    if specials:
        lines.append("- 专题")
        for article in specials:
            label = md_label(article.title)
            lines.append(f"  - [{label}](articles/{article.output_name})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def readme_markdown(articles: list[Article]) -> str:
    chapters: dict[str, list[Article]] = {}
    specials: list[Article] = []
    for article in articles:
        if article.seq is None:
            specials.append(article)
        else:
            chapters.setdefault(article.chapter, []).append(article)

    lines = [
        "# AI Agent 面试题专辑",
        "",
        "面向 AI 应用工程师和 Agent 开发工程师的面试阅读专辑。",
        "按主题分成章节，从技术选型、Prompt、RAG、检索、工具调用、编排框架、MCP，到安全评测、场景设计和项目表达。",
        "",
        "正文来自公众号 **FullStack 研发派**。",
        "",
        "## 目录",
        "",
    ]
    for name in sorted(chapters, key=chapter_sort_key):
        group = chapters[name]
        first = group[0]
        label = md_label(name)
        lines.append(
            f"- [{label}](articles/{first.output_name})（{len(group)} 篇）"
        )
    if specials:
        lines.extend(["", "## 专题", ""])
        for article in specials:
            lines.append(f"- [{md_label(article.title)}](articles/{article.output_name})")
    lines.extend(
        [
            "",
            "## 关注公众号",
            "",
            "更多面试题在公众号持续更新。微信扫码关注 **FullStack 研发派**，后台回复「题库」，可以领取完整目录。",
            "",
            f'<img src="assets/{QR_NAME}" alt="FullStack 研发派" width="220" />',
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    qr_path = ROOT / "assets" / QR_NAME
    if not qr_path.is_file():
        raise SystemExit(f"缺少二维码图片: {qr_path}")
    articles = load_articles()
    if not articles:
        raise SystemExit("没有可发布的文章")
    write_articles(articles)
    (ROOT / "_sidebar.md").write_text(sidebar_markdown(articles), encoding="utf-8")
    (ROOT / "README.md").write_text(readme_markdown(articles), encoding="utf-8")
    numbered = sum(1 for item in articles if item.seq is not None)
    specials = len(articles) - numbered
    print(f"已生成 {len(articles)} 篇（正篇 {numbered}，专题 {specials}）")


if __name__ == "__main__":
    main()
