"""md2wechat — Markdown → 微信公众号文章 HTML 转换器。

本仓库 (`AgentObserver`) 内部工具，把项目中的 Markdown 文档转成
可直接粘贴到公众号「图文素材 → 源代码视图」的 HTML：

- 所有样式强制内联（公众号会剥离 `<style>` / `<link>` / `<script>` 与 `class=`）
- 可选下载外链图到本地（公众号会拦截外链）
- 内置 Pygments 代码高亮（亦为内联样式）
- 3 套与 `marketing/production-workflow.md §4.3` 对齐的主题

详见 ``tools/md2wechat/README.md`` 与 ``python3 -m md2wechat --help``。
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]