"""渲染器输出的「内联样式」不变量测试。

公众号会把 ``class=`` 选择器、``<style>`` / ``<link>`` / ``<script>`` 全部剥离；
所以本工具的关键不变量是：**所有元素都带内联 ``style="..."``**，且**不出现**
会让公众号渲染异常的标签。
"""

from __future__ import annotations

import re

import pytest

from md2wechat.converter import convert
from md2wechat.themes import MARKETING, SCIENCE_POPULAR, SCI_TECH


SAMPLE_MD = """\
# 标题 H1

这是一段普通**粗体**与*斜体*与~~删除线~~文本。

## 子标题 H2

- 列表项 1
- 列表项 2

1. 有序项 1
2. 有序项 2

### 子标题 H3

> 引用块：仅供参考

#### 子标题 H4

```python
def hello():
    return "world"
```

```bash
echo "plain shell"
```

| 列 A | 列 B |
|---|---|
| 单元格 1 | 单元格 2 |

---

![FIG 示例](https://example.com/foo.png)

[链接示例](https://example.com)
"""


# ---------------------------------------------------------------- #
# 全局不变量（所有主题都要满足）
# ---------------------------------------------------------------- #


@pytest.mark.parametrize(
    "theme_name",
    ["sci-tech", "science-popular", "marketing"],
)
def test_no_class_attribute(theme_name: str) -> None:
    """输出 HTML 中不能出现 ``class="..."``。"""
    html = convert(SAMPLE_MD, theme_name=theme_name)
    assert 'class="' not in html, (
        f"theme={theme_name} 输出含 class 属性（公众号会剥离）"
    )


@pytest.mark.parametrize(
    "theme_name",
    ["sci-tech", "science-popular", "marketing"],
)
def test_no_external_style_or_script_tags(theme_name: str) -> None:
    """输出 HTML 中不能出现 ``<style>`` / ``<link rel="stylesheet">`` / ``<script>``。"""
    html = convert(SAMPLE_MD, theme_name=theme_name).lower()
    assert "<style" not in html
    assert "<link" not in html
    assert "<script" not in html


# ---------------------------------------------------------------- #
# 元素级别 — 每个应该带内联样式的标签都要带
# ---------------------------------------------------------------- #


@pytest.mark.parametrize(
    "tag,style_attr",
    [
        ("h1", "font-size"),
        ("h2", "font-size"),
        ("h3", "font-size"),
        ("h4", "font-size"),
        ("p", "margin"),
        ("ul", "margin"),
        ("ol", "margin"),
        ("li", "margin"),
        ("blockquote", "border-left"),
        ("a", "color"),
        ("strong", "font-weight"),
        ("em", "font-style"),
        ("code", "background"),
        ("pre", "background"),
        ("img", "max-width"),
        ("table", "border-collapse"),
        ("th", "background"),
        ("td", "padding"),
    ],
)
def test_tag_has_inline_style(tag: str, style_attr: str) -> None:
    """每个被覆盖的元素都应有 ``style="..."`` 且包含主题字段的特征属性。"""
    html = convert(SAMPLE_MD, theme_name="sci-tech")
    pattern = re.compile(rf'<{tag}[^>]*\bstyle="([^"]*)"', re.IGNORECASE)
    matches = pattern.findall(html)
    assert matches, f"<{tag}> 未在输出中出现"
    for style in matches:
        assert style_attr in style, (
            f"<{tag}> style 缺少 '{style_attr}'：{style[:80]}"
        )


# ---------------------------------------------------------------- #
# 代码高亮
# ---------------------------------------------------------------- #


def test_fenced_code_block_highlighted() -> None:
    """围栏代码块应由 Pygments 高亮，输出 ``<span style="...">`` 包裹 token。"""
    html = convert(SAMPLE_MD, theme_name="sci-tech")
    assert "<pre" in html and "</pre>" in html
    assert '<span style="' in html, "Pygments 应输出 <span style=...> 高亮 token"


def test_fenced_code_block_no_lang_falls_back() -> None:
    """未声明语言也应有 ``<pre>`` 包裹（fallback 到纯文本）。"""
    md = "```\nplain code\n```"
    html = convert(md, theme_name="sci-tech")
    assert "<pre" in html
    assert "plain code" in html


# ---------------------------------------------------------------- #
# 图片
# ---------------------------------------------------------------- #


def test_image_alt_text_preserved() -> None:
    """``alt`` 文本必须保留（无障碍 + 公众号图片删除后兜底）。"""
    md = "![替代文本 hello](foo.jpg)"
    html = convert(md, theme_name="sci-tech")
    assert 'alt="替代文本 hello"' in html


def test_image_src_preserved() -> None:
    """``src`` 必须原样保留。"""
    md = "![alt](path/to/foo.jpg)"
    html = convert(md, theme_name="sci-tech")
    assert 'src="path/to/foo.jpg"' in html


# ---------------------------------------------------------------- #
# frontmatter
# ---------------------------------------------------------------- #


def test_strip_frontmatter_by_default() -> None:
    """默认应剥离开头的 YAML frontmatter。"""
    md = "---\ntitle: test\n---\n# 正文"
    html = convert(md, theme_name="sci-tech")
    assert "title: test" not in html
    assert "<h1" in html  # 正文 H1 应保留


def test_keep_frontmatter_when_disabled() -> None:
    """``strip_frontmatter=False`` 时保留 frontmatter 内容（仍可能被解析）。"""
    md = "---\ntitle: test\n---\n# 正文"
    html = convert(md, theme_name="sci-tech", strip_frontmatter=False)
    assert "title: test" in html


# ---------------------------------------------------------------- #
# 主题差异
# ---------------------------------------------------------------- #


def test_themes_produce_distinct_outputs() -> None:
    """3 套主题应产出明显不同的 HTML（h1 颜色或字号至少一项不同）。"""
    sci = convert(SAMPLE_MD, theme_name="sci-tech")
    pop = convert(SAMPLE_MD, theme_name="science-popular")
    mkt = convert(SAMPLE_MD, theme_name="marketing")
    assert sci != pop
    assert pop != mkt
    assert sci != mkt


def test_theme_referenced_in_section_style() -> None:
    """``<section>`` 包裹 style 应来自主题 ``section`` 字段。"""
    html = convert(SAMPLE_MD, theme_name="sci-tech")
    assert SCI_TECH.section in html
    html2 = convert(SAMPLE_MD, theme_name="marketing")
    assert MARKETING.section in html2
    assert SCIENCE_POPULAR.section not in html  # sci-tech 主题里不应混入 science-popular