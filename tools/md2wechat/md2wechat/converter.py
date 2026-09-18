"""编排：读 md → 渲染为微信公众号可粘贴的 HTML。

本文件负责"管线"，把 markdown 文本经过若干步骤变成最终 HTML：

1. ``_strip_frontmatter``：若以 ``---\\n`` 开头，丢弃首段 YAML frontmatter
2. ``_download_external_images``：可选地把 ``![](http*)`` 下载到本地（避免公众号拦截）
3. ``build_renderer(theme).render(text)``：核心 markdown-it 渲染（见 ``renderer.py``）
4. 用主题 ``section`` 字段包裹 ``<section>``

调用方一般是 :func:`cli.main`；程序化使用见 :func:`convert`。
"""

from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from .renderer import build_renderer
from .themes import Theme, get_theme


# ------------------------------------------------------------------ #
# frontmatter
# ------------------------------------------------------------------ #


def _strip_frontmatter(text: str) -> str:
    """若 ``text`` 以 ``---\\n`` 开头，丢弃由 ``\\n---\\n`` 闭合的 YAML frontmatter 块。

    v0.1 简化版：只切片丢弃内容，不解析 YAML 字段；后续 v0.2 上 pyyaml 后可做 schema 校验。
    """
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :]


# ------------------------------------------------------------------ #
# 外链图下载
# ------------------------------------------------------------------ #


_EXTERNAL_IMG = re.compile(r"!\[([^\]]*)\]\((https?://[^\s)]+)\)")


def _download_external_images(
    text: str,
    dest: Path,
    timeout: float = 15.0,
    *,
    verbose: bool = False,
) -> str:
    """把 ``![](http*)`` / ``![](https*)`` 下载到 ``dest`` 并替换为本地文件名。

    - 本地相对路径 / ``data:`` URI / 已是本地路径：保持原样
    - 下载成功：替换为 ``dest/<basename>``（同名时附加 ``-1``, ``-2`` …）
    - 下载失败：``print(..., file=sys.stderr)`` 警告，URL 保留原样
    - 用 stdlib :mod:`urllib.request`，不引入 ``requests`` 依赖
    """
    dest.mkdir(parents=True, exist_ok=True)

    def replace(match: re.Match[str]) -> str:
        alt = match.group(1)
        url = match.group(2)
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310
                data = resp.read()
        except Exception as exc:  # noqa: BLE001
            print(
                f"[md2wechat] WARN failed to download {url}: {exc}; keeping original URL",
                file=sys.stderr,
            )
            return match.group(0)

        parsed = urlparse(url)
        basename = Path(parsed.path).name or "image"
        target = dest / basename
        counter = 1
        while target.exists():
            stem, suffix = target.stem, target.suffix
            target = dest / f"{stem}-{counter}{suffix}"
            counter += 1
        target.write_bytes(data)
        if verbose:
            print(f"[md2wechat] downloaded {url} → {target}", file=sys.stderr)
        return f"![{alt}]({target.name})"

    return _EXTERNAL_IMG.sub(replace, text)


# ------------------------------------------------------------------ #
# 对外主入口
# ------------------------------------------------------------------ #


def convert(
    md_text: str,
    theme_name: str = "sci-tech",
    *,
    download: bool = False,
    image_dir: Path | None = None,
    strip_frontmatter: bool = True,
    verbose: bool = False,
) -> str:
    """把 markdown 文本转成可直接粘贴到公众号草稿箱的 HTML。

    Parameters
    ----------
    md_text:
        原始 markdown 文本。
    theme_name:
        主题预设名，详见 :func:`themes.get_theme`。
    download:
        若为 ``True``，下载所有 ``http(s)://`` 图片到 ``image_dir``。
    image_dir:
        下载目录；默认 ``Path("assets/wechat")``。
    strip_frontmatter:
        若为 ``True``（默认），自动移除开头的 YAML frontmatter。
    verbose:
        是否打印下载进度到 stderr。
    """
    text = md_text.lstrip("﻿").replace("\r\n", "\n")
    if strip_frontmatter:
        text = _strip_frontmatter(text)
    if download:
        text = _download_external_images(
            text,
            image_dir or Path("assets/wechat"),
            verbose=verbose,
        )
    theme: Theme = get_theme(theme_name)
    md = build_renderer(theme)
    body = md.render(text)
    return f'<section style="{theme.section}">\n{body}\n</section>\n'


__all__ = [
    "convert",
    "_strip_frontmatter",
    "_download_external_images",
]