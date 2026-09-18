"""markdown-it 自定义渲染器：17 个 token 类型 + 代码高亮。

设计要点（v0.1）：

- 用 ``md.add_render_rule(token_type, fn)`` 覆盖 ``*_open/close`` 标签对（块级 + 内联 17 类）。
- **关键陷阱**：``add_render_rule`` 内部对回调做 ``function.__get__(self.renderer)``，会把
  函数绑定为 ``RendererHTML`` 实例方法（隐式 ``self``）。因此所有回调必须用
  :func:`staticmethod` 包装，否则会收到 5 个参数（self + 4 真实参数）。
- 不覆盖 markdown-it 的 9 个内建叶子规则（``code_inline`` / ``fence`` / ``image`` 等）；
  围栏代码块在 :func:`highlight` 里用 Pygments 预渲染，再走 ``html_block`` 注入。
- 关键不变量：每个规则产出的开标签必须形如 ``<tag style="{theme.<field>}">``；
  闭标签不需注册（markdown-it 在 token.nesting == -1 时自动闭合）。
"""

from __future__ import annotations

from markdown_it import MarkdownIt

from .themes import Theme


# ------------------------------------------------------------------ #
# 代码高亮（Pygments 内联样式）
# ------------------------------------------------------------------ #


def highlight(code: str, lang: str) -> str:
    """用 Pygments 把代码块转成内联样式 HTML，外面包 ``<pre><code>``。

    - 支持的语言由 Pygments lexer 决定；不识别时退化为纯文本（HTML 转义）
    - ``HtmlFormatter(style='friendly', noclasses=True)`` → 全部 token 样式内联
    - **关键清洗**：Pygments 默认输出 ``<div class="highlight"><pre>...``；此处正则剥掉
      外层 ``<div class="highlight">`` / ``</div>`` 与多余的 ``<pre>``，避免公众号
      检测到 ``class="`` 或双层 ``<pre>``
    """
    import re
    from pygments import highlight as _highlight
    from pygments.formatters.html import HtmlFormatter
    from pygments.lexers import get_lexer_by_name
    from pygments.util import ClassNotFound
    from html import escape

    if lang:
        try:
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = None
    else:
        lexer = None

    if lexer is None:
        body = escape(code)
    else:
        formatter = HtmlFormatter(style="friendly", noclasses=True, nowrap=False)
        body = _highlight(code, lexer, formatter)
        # 剥掉 Pygments 默认包装：<div class="highlight" style="..."><pre style="...">...</pre></div>\n
        # 关键：Pygments 给外层 <div> 加了 style 属性 —— 必须用 [^>]* 兼容
        body = re.sub(
            r'<div class="highlight"[^>]*><pre[^>]*>(.*?)</pre></div>\s*$',
            r"\1",
            body,
            count=1,
            flags=re.DOTALL,
        )

    return f"<pre><code>{body}</code></pre>"


# ------------------------------------------------------------------ #
# 辅助：根据 token 属性决定用哪个 theme 字段
# ------------------------------------------------------------------ #


def _heading_open(theme: Theme, tokens, idx: int) -> str:
    """按 tag（如 h1 / h2）取对应主题字段。"""
    tag = tokens[idx].tag  # e.g. "h1", "h2"
    style = getattr(theme, tag, None) or theme.h4
    return f'<{tag} style="{style}">'


def _link_open(theme: Theme, tokens, idx: int) -> str:
    """开链接标签；公众号会拦截外链，但保留样式仍有内联价值。"""
    token = tokens[idx]
    href = token.attrs.get("href", "#") if token.attrs else "#"
    target = token.attrs.get("target", "") if token.attrs else ""
    target_attr = f' target="{target}"' if target else ""
    return f'<a href="{href}"{target_attr} style="{theme.a}">'


def _tr_open(theme: Theme, tokens, idx: int) -> str:
    """``<tr>`` 没有强制样式，但若主题给了 ``tr`` 字段就用上。"""
    return f'<tr style="{theme.tr}">' if theme.tr else "<tr>"


def _fence(theme: Theme, tokens, idx: int) -> str:
    """围栏代码块（```` ```python ````）：调用 :func:`highlight` 并包裹主题样式。"""
    token = tokens[idx]
    lang = (token.info or "").strip().split() or [""]
    inner = highlight(token.content, lang[0])
    # highlight() 已经返回 ``<pre><code>...``，在外面再套一层 ``<pre>`` 会双层；
    # 因此手动拆开重包以应用主题样式。
    code = inner.split("<code>", 1)[1].rsplit("</code>", 1)[0]
    return f'<pre style="{theme.pre}"><code style="{theme.code_inline}">{code}</code></pre>'


def _code_block(theme: Theme, tokens, idx: int) -> str:
    """缩进代码块（4 空格）：无语言信息时按纯文本处理。"""
    token = tokens[idx]
    inner = highlight(token.content, "")
    code = inner.split("<code>", 1)[1].rsplit("</code>", 1)[0]
    return f'<pre style="{theme.pre}"><code style="{theme.code_inline}">{code}</code></pre>'


def _image(theme: Theme, tokens, idx: int) -> str:
    """``<img>``：从 ``token.attrs`` + ``token.content`` 重建带主题样式的标签。

    注意：markdown-it 把 alt 文本放在 ``token.content`` 而非 ``token.attrs["alt"]``。
    """
    token = tokens[idx]
    attrs = token.attrs or {}
    src = attrs.get("src", "")
    title = attrs.get("title", "")
    alt = token.content or ""
    title_attr = f' title="{title}"' if title else ""
    return f'<img src="{src}" alt="{alt}"{title_attr} style="{theme.img}" />'


# ------------------------------------------------------------------ #
# 渲染器构造
# ------------------------------------------------------------------ #


def build_renderer(theme: Theme) -> MarkdownIt:
    """构造一个用 ``theme`` 渲染所有元素的 MarkdownIt 对象。

    覆盖 17 个 token 类型；其余 token 走 markdown-it 默认。
    """
    md = MarkdownIt("commonmark", {"html": True, "linkify": True, "typographer": False})

    # ----- 块级：标题 -----
    md.add_render_rule(
        "heading_open",
        staticmethod(lambda tokens, idx, options, env: _heading_open(theme, tokens, idx)),
    )

    # ----- 段落 -----
    md.add_render_rule(
        "paragraph_open",
        staticmethod(lambda tokens, idx, options, env: f'<p style="{theme.p}">'),
    )

    # ----- 引用 -----
    md.add_render_rule(
        "blockquote_open",
        staticmethod(lambda tokens, idx, options, env: f'<blockquote style="{theme.blockquote}">'),
    )

    # ----- 列表 -----
    md.add_render_rule(
        "bullet_list_open",
        staticmethod(lambda tokens, idx, options, env: f'<ul style="{theme.ul}">'),
    )
    md.add_render_rule(
        "ordered_list_open",
        staticmethod(lambda tokens, idx, options, env: f'<ol style="{theme.ol}">'),
    )
    md.add_render_rule(
        "list_item_open",
        staticmethod(lambda tokens, idx, options, env: f'<li style="{theme.li}">'),
    )

    # ----- 表格 -----
    md.add_render_rule(
        "table_open",
        staticmethod(lambda tokens, idx, options, env: f'<table style="{theme.table}">'),
    )
    md.add_render_rule(
        "thead_open",
        staticmethod(lambda tokens, idx, options, env: "<thead>"),
    )
    md.add_render_rule(
        "tbody_open",
        staticmethod(lambda tokens, idx, options, env: "<tbody>"),
    )
    md.add_render_rule(
        "tr_open",
        staticmethod(lambda tokens, idx, options, env: _tr_open(theme, tokens, idx)),
    )
    md.add_render_rule(
        "th_open",
        staticmethod(lambda tokens, idx, options, env: f'<th style="{theme.th}">'),
    )
    md.add_render_rule(
        "td_open",
        staticmethod(lambda tokens, idx, options, env: f'<td style="{theme.td}">'),
    )

    # ----- 水平线 -----
    md.add_render_rule(
        "hr",
        staticmethod(lambda tokens, idx, options, env: f'<hr style="{theme.hr}" />'),
    )

    # ----- 围栏代码块 + 缩进代码块 -----
    # 关键：markdown-it 默认 fence 规则会输出 ``<pre><code class="language-X">``，
    # 既带 class 标签也不做语法高亮。这里完全替换为 Pygments 内联样式输出。
    md.add_render_rule(
        "fence",
        staticmethod(lambda tokens, idx, options, env: _fence(theme, tokens, idx)),
    )
    md.add_render_rule(
        "code_block",
        staticmethod(lambda tokens, idx, options, env: _code_block(theme, tokens, idx)),
    )

    # ----- 内联：strong / em / s / link -----
    md.add_render_rule(
        "strong_open",
        staticmethod(lambda tokens, idx, options, env: f'<strong style="{theme.strong}">'),
    )
    md.add_render_rule(
        "em_open",
        staticmethod(lambda tokens, idx, options, env: f'<em style="{theme.em}">'),
    )
    md.add_render_rule(
        "s_open",
        staticmethod(lambda tokens, idx, options, env: f'<s style="{theme.s}">'),
    )
    md.add_render_rule(
        "link_open",
        staticmethod(lambda tokens, idx, options, env: _link_open(theme, tokens, idx)),
    )

    # ----- 图片 -----
    # markdown-it 默认 ``image`` 规则输出 ``<img src="..." alt="..." />`` 不带 style，
    # 在窄屏公众号里可能溢出。这里从 src/alt 重建一个带 theme.img 样式的 <img>。
    md.add_render_rule(
        "image",
        staticmethod(lambda tokens, idx, options, env: _image(theme, tokens, idx)),
    )

    return md


__all__ = ["build_renderer", "highlight"]