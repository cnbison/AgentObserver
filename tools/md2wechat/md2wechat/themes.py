"""主题预设。

每套主题 = 一个 ``Theme`` dataclass，每个元素类型一个完整的 ``style="..."`` 字符串。
渲染器 (`renderer.py`) 不做拼装 —— 直接读取字段输出，保证每条规则都是纯数据。

配色约定：

- **sci-tech** 与 ``marketing/production-workflow.md §4.3`` 色板一致：
  深空蓝 ``#18242f`` / 暖橙 ``#edb28b`` / 奶油 ``#f0e9dd`` / 冷灰 ``#94a3b8`` /
  近黑 ``#0a1118`` / 翡翠 ``#4ade80`` / 浅红 ``#f87171``。
- **science-popular** 用更亲民的海军蓝 + 沙金。
- **marketing** 用大红 + 琥珀，适合推广文案。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Theme:
    """完整主题；每个字段都是一段可直接拼到 ``style="..."`` 的 CSS。"""

    name: str
    description: str

    # 容器与基础排版
    section: str
    body: str

    # 标题（h1–h4）
    h1: str
    h2: str
    h3: str
    h4: str

    # 段落与强调
    p: str
    strong: str
    em: str
    s: str

    # 引用
    blockquote: str

    # 列表
    ul: str
    ol: str
    li: str

    # 链接
    a: str

    # 代码
    code_inline: str
    pre: str

    # 图片
    img: str

    # 表格
    table: str
    th: str
    td: str
    tr: str

    # 分隔线
    hr: str


SCI_TECH = Theme(
    name="sci-tech",
    description="科技风 — 深空蓝 + 暖橙；与 marketing/production-workflow.md §4.3 一致",
    section=(
        "font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', "
        "'Microsoft YaHei', 'Helvetica Neue', sans-serif; "
        "max-width: 720px; margin: 0 auto; padding: 20px 16px; "
        "color: #18242f; background: #ffffff; line-height: 1.75;"
    ),
    body="font-size: 16px; line-height: 1.75; color: #18242f;",
    h1=(
        "font-size: 22px; font-weight: 700; color: #18242f; "
        "margin: 28px 0 16px; border-left: 4px solid #edb28b; padding-left: 12px;"
    ),
    h2=(
        "font-size: 19px; font-weight: 700; color: #18242f; "
        "margin: 24px 0 12px; border-left: 3px solid #edb28b; padding-left: 10px;"
    ),
    h3="font-size: 17px; font-weight: 700; color: #edb28b; margin: 20px 0 10px;",
    h4="font-size: 16px; font-weight: 700; color: #94a3b8; margin: 18px 0 8px;",
    p="margin: 12px 0; color: #18242f;",
    strong="font-weight: 700; color: #edb28b;",
    em="font-style: italic; color: #0a1118;",
    s="text-decoration: line-through; color: #94a3b8;",
    blockquote=(
        "margin: 14px 0; padding: 10px 16px; border-left: 4px solid #edb28b; "
        "background: #f0e9dd; color: #18242f; border-radius: 0 4px 4px 0;"
    ),
    ul="margin: 12px 0; padding-left: 26px;",
    ol="margin: 12px 0; padding-left: 26px;",
    li="margin: 6px 0; color: #18242f;",
    a="color: #edb28b; text-decoration: underline;",
    code_inline=(
        "background: #f0e9dd; color: #d62828; padding: 2px 6px; "
        "border-radius: 4px; font-family: 'SF Mono', Consolas, Menlo, monospace; "
        "font-size: 14px;"
    ),
    pre=(
        "background: #0a1118; color: #f0e9dd; padding: 16px; border-radius: 8px; "
        "overflow-x: auto; font-family: 'SF Mono', Consolas, Menlo, monospace; "
        "font-size: 14px; line-height: 1.5; margin: 16px 0;"
    ),
    img="max-width: 100%; height: auto; display: block; margin: 16px auto; border-radius: 6px;",
    table="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px;",
    th=(
        "background: #18242f; color: #f0e9dd; padding: 8px 12px; "
        "text-align: left; border: 1px solid #94a3b8; font-weight: 600;"
    ),
    td="padding: 8px 12px; border: 1px solid #94a3b8; color: #18242f;",
    tr="",
    hr="border: none; border-top: 1px solid #94a3b8; margin: 24px 0;",
)


SCIENCE_POPULAR = Theme(
    name="science-popular",
    description="科普风 — 海军蓝 + 沙金；长文阅读更亲民",
    section=(
        "font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', "
        "'Microsoft YaHei', 'Helvetica Neue', sans-serif; "
        "max-width: 720px; margin: 0 auto; padding: 20px 16px; "
        "color: #1f2937; background: #ffffff; line-height: 1.85;"
    ),
    body="font-size: 17px; line-height: 1.85; color: #1f2937;",
    h1=(
        "font-size: 24px; font-weight: 700; color: #1f4e79; "
        "margin: 30px 0 18px; text-align: center;"
    ),
    h2=(
        "font-size: 20px; font-weight: 700; color: #1f4e79; "
        "margin: 24px 0 12px; border-bottom: 2px solid #f4a261; padding-bottom: 4px;"
    ),
    h3="font-size: 18px; font-weight: 700; color: #f4a261; margin: 20px 0 10px;",
    h4="font-size: 17px; font-weight: 700; color: #6b7280; margin: 16px 0 8px;",
    p="margin: 14px 0; color: #1f2937;",
    strong="font-weight: 700; color: #f4a261;",
    em="font-style: italic; color: #111827;",
    s="text-decoration: line-through; color: #6b7280;",
    blockquote=(
        "margin: 16px 0; padding: 12px 18px; border-left: 4px solid #f4a261; "
        "background: #fef3c7; color: #1f2937; border-radius: 0 6px 6px 0;"
    ),
    ul="margin: 14px 0; padding-left: 28px;",
    ol="margin: 14px 0; padding-left: 28px;",
    li="margin: 8px 0; color: #1f2937;",
    a="color: #1f4e79; text-decoration: underline;",
    code_inline=(
        "background: #fef3c7; color: #1f4e79; padding: 2px 6px; "
        "border-radius: 4px; font-family: 'SF Mono', Consolas, Menlo, monospace; "
        "font-size: 15px;"
    ),
    pre=(
        "background: #f9fafb; color: #1f2937; padding: 16px; border-radius: 8px; "
        "overflow-x: auto; font-family: 'SF Mono', Consolas, Menlo, monospace; "
        "font-size: 15px; line-height: 1.6; margin: 16px 0; border: 1px solid #e5e7eb;"
    ),
    img="max-width: 100%; height: auto; display: block; margin: 16px auto; border-radius: 8px;",
    table="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 15px;",
    th=(
        "background: #1f4e79; color: #ffffff; padding: 8px 12px; "
        "text-align: left; border: 1px solid #d1d5db; font-weight: 600;"
    ),
    td="padding: 8px 12px; border: 1px solid #d1d5db; color: #1f2937;",
    tr="",
    hr="border: none; border-top: 2px dashed #d1d5db; margin: 24px 0;",
)


MARKETING = Theme(
    name="marketing",
    description="营销风 — 大红 + 琥珀；推广文案更紧凑",
    section=(
        "font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', "
        "'Microsoft YaHei', 'Helvetica Neue', sans-serif; "
        "max-width: 720px; margin: 0 auto; padding: 18px 14px; "
        "color: #111827; background: #fff7ed; line-height: 1.7;"
    ),
    body="font-size: 16px; line-height: 1.7; color: #111827;",
    h1=(
        "font-size: 26px; font-weight: 800; color: #d62828; "
        "margin: 24px 0 14px; text-align: center; letter-spacing: 1px;"
    ),
    h2=(
        "font-size: 21px; font-weight: 700; color: #d62828; "
        "margin: 22px 0 10px; background: linear-gradient(to right, #fcbf49, transparent); "
        "padding: 6px 12px;"
    ),
    h3="font-size: 18px; font-weight: 700; color: #fcbf49; margin: 18px 0 8px;",
    h4="font-size: 16px; font-weight: 700; color: #6b7280; margin: 16px 0 6px;",
    p="margin: 10px 0; color: #111827;",
    strong="font-weight: 700; color: #d62828;",
    em="font-style: italic; color: #111827;",
    s="text-decoration: line-through; color: #6b7280;",
    blockquote=(
        "margin: 14px 0; padding: 12px 16px; border-left: 4px solid #fcbf49; "
        "background: #ffffff; color: #111827;"
    ),
    ul="margin: 12px 0; padding-left: 26px;",
    ol="margin: 12px 0; padding-left: 26px;",
    li="margin: 6px 0; color: #111827;",
    a="color: #d62828; text-decoration: underline; font-weight: 600;",
    code_inline=(
        "background: #ffffff; color: #d62828; padding: 2px 6px; "
        "border-radius: 4px; font-family: 'SF Mono', Consolas, Menlo, monospace; "
        "font-size: 14px; border: 1px solid #fcbf49;"
    ),
    pre=(
        "background: #111827; color: #fcbf49; padding: 14px; border-radius: 8px; "
        "overflow-x: auto; font-family: 'SF Mono', Consolas, Menlo, monospace; "
        "font-size: 14px; line-height: 1.5; margin: 14px 0;"
    ),
    img=(
        "max-width: 100%; height: auto; display: block; margin: 14px auto; "
        "border: 3px solid #fcbf49; border-radius: 6px;"
    ),
    table="width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 14px;",
    th=(
        "background: #d62828; color: #ffffff; padding: 8px 12px; "
        "text-align: left; border: 1px solid #fcbf49; font-weight: 600;"
    ),
    td="padding: 8px 12px; border: 1px solid #fcbf49; color: #111827;",
    tr="",
    hr="border: none; border-top: 2px solid #fcbf49; margin: 20px 0;",
)


THEMES: dict[str, Theme] = {
    "sci-tech": SCI_TECH,
    "science-popular": SCIENCE_POPULAR,
    "marketing": MARKETING,
}


def get_theme(name: str) -> Theme:
    """按名字取主题；找不到时给出可用列表。"""
    if name in THEMES:
        return THEMES[name]
    available = ", ".join(sorted(THEMES))
    raise KeyError(f"未知主题 '{name}'；可选：{available}")


__all__ = ["Theme", "SCI_TECH", "SCIENCE_POPULAR", "MARKETING", "THEMES", "get_theme"]