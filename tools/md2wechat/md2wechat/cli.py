"""CLI：``python3 -m md2wechat ...``。

参数设计原则：

- 单文件 / 批量 / 仅查询三种入口互斥（``-i`` / ``--batch`` / ``--list-themes``）
- ``--output`` 默认 stdout，便于管道组合（如 ``| pbcopy``）
- 每次成功转换都在 stderr 重复公众号限制清单，强化记忆
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .converter import convert
from .themes import THEMES


WECHAT_NOTES = """\
公众号渲染限制清单（务必先读）：
  1. 公众号会拦截外链图 → 需用 -d 下载到本地，再从「素材管理」上传
  2. 只支持内联 CSS —— class 选择器与 <style>/<link>/<script> 会被剥离
  3. 外链会被改写到 mp.weixin.qq.com，target="_blank" 不生效
  4. 草稿箱需在移动端实测：桌面端样式可能与手机渲染不一致
  5. 不支持嵌套表格 / 单元格合并 / colspan
"""


# ------------------------------------------------------------------ #
# argparse
# ------------------------------------------------------------------ #


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="md2wechat",
        description="Markdown → 微信公众号文章 HTML 转换器（AgentObserver 内部工具）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=WECHAT_NOTES,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # 三种入口互斥
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "-i", "--input",
        type=Path,
        help="输入 markdown 文件路径；省略 -o 时写到 stdout",
    )
    source.add_argument(
        "--batch",
        type=str,
        metavar="GLOB",
        help="glob 模式批量转换（如 'marketing/*.md'），输出到 marketing/dist/",
    )
    source.add_argument(
        "--list-themes",
        action="store_true",
        help="列出所有可用主题并退出",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="输出 HTML 文件路径（默认 stdout）",
    )
    parser.add_argument(
        "-t", "--theme",
        default="sci-tech",
        choices=sorted(THEMES),
        help="主题预设（默认 sci-tech）",
    )
    parser.add_argument(
        "-d", "--download-images",
        action="store_true",
        help="下载外链图（http/https）到本地以避免公众号拦截",
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        default=Path("assets/wechat"),
        help="外链图下载目录（默认 ./assets/wechat）",
    )
    parser.add_argument(
        "--no-frontmatter",
        action="store_true",
        help="不移除文档开头的 YAML frontmatter 块（默认会自动剥离）",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="若发现未下载的外链图则退出码非零（适合 CI）",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细处理进度",
    )
    return parser


# ------------------------------------------------------------------ #
# 子命令
# ------------------------------------------------------------------ #


def cmd_list_themes() -> int:
    print(f"md2wechat {__version__} — 可用主题：")
    print()
    for theme in THEMES.values():
        print(f"  {theme.name:<18}  {theme.description}")
    print()
    print("默认主题：sci-tech。用 -t <name> 切换。")
    return 0


def _detect_external_images(md_text: str) -> bool:
    """粗略判断 md 里是否含 ``![](http*)``，用于 ``--strict`` 提示。"""
    return any(
        line.lstrip().startswith("![") and "](http" in line
        for line in md_text.splitlines()
    )


def cmd_convert_one(input_path: Path, args: argparse.Namespace) -> int:
    if not input_path.exists():
        print(f"error: 输入文件不存在：{input_path}", file=sys.stderr)
        return 2

    md_text = input_path.read_text(encoding="utf-8")
    had_external = _detect_external_images(md_text)

    html = convert(
        md_text,
        theme_name=args.theme,
        download=args.download_images,
        image_dir=args.image_dir,
        strip_frontmatter=not args.no_frontmatter,
        verbose=args.verbose,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding="utf-8")
        if args.verbose:
            print(
                f"[md2wechat] wrote {args.output} "
                f"({len(html)} bytes, theme={args.theme})",
                file=sys.stderr,
            )
    else:
        sys.stdout.write(html)

    # 每次转换都在 stderr 提醒限制清单（除非已 -v 详细模式打印过一次）
    if args.verbose:
        print(WECHAT_NOTES, file=sys.stderr)
    else:
        print(
            f"[md2wechat] theme={args.theme} bytes={len(html)} "
            f"({input_path.name} → {args.output or 'stdout'})",
            file=sys.stderr,
        )

    if args.strict and had_external and not args.download_images:
        print(
            f"error: {input_path} 含外链图但未指定 -d；"
            f"--strict 模式下退出非零",
            file=sys.stderr,
        )
        return 3

    return 0


def cmd_batch(pattern: str, args: argparse.Namespace) -> int:
    paths = sorted(Path(".").glob(pattern))
    if not paths:
        print(f"error: 无文件匹配模式：{pattern}", file=sys.stderr)
        return 2

    out_dir = args.output or Path("marketing/dist")
    out_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for p in paths:
        target = out_dir / f"{p.stem}.wechat.html"
        # 拷贝 args 但覆盖 input/output；避免 Namespace(**vars, input=p) 的多值冲突
        merged = vars(args).copy()
        merged["input"] = p
        merged["output"] = target
        single_args = argparse.Namespace(**merged)
        rc = cmd_convert_one(p, single_args)
        if rc != 0:
            failures += 1

    if failures:
        print(f"error: {failures} / {len(paths)} 文件失败", file=sys.stderr)
        return 1
    print(
        f"[md2wechat] batch ok: {len(paths)} files → {out_dir}/",
        file=sys.stderr,
    )
    return 0


# ------------------------------------------------------------------ #
# main
# ------------------------------------------------------------------ #


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_themes:
        return cmd_list_themes()
    if args.batch is not None:
        return cmd_batch(args.batch, args)
    return cmd_convert_one(args.input, args)


if __name__ == "__main__":
    sys.exit(main())