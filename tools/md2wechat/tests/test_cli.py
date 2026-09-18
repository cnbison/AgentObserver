"""CLI 集成测试：用 subprocess 跑 ``python3 -m md2wechat``。

不在 CI 里假设 pytest 插件，每个测试都直接调用 stdlib subprocess。
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_DIR = REPO_ROOT / "tools" / "md2wechat"
FIXTURE = TOOL_DIR / "tests" / "fixtures" / "sample.md"


def _run(args: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    """在工具目录下运行 ``python3 -m md2wechat``，返回 CompletedProcess。"""
    cmd = [sys.executable, "-m", "md2wechat", *args]
    return subprocess.run(
        cmd,
        cwd=TOOL_DIR,
        capture_output=True,
        text=True,
        **kwargs,
    )


def test_cli_help_exits_0() -> None:
    """``--help`` 应正常退出（exit 0）并列出参数。"""
    result = _run(["--help"])
    assert result.returncode == 0
    assert "公众号渲染限制清单" in result.stdout


def test_cli_version_exits_0() -> None:
    """``--version`` 应输出 ``md2wechat`` 版本号。"""
    result = _run(["--version"])
    assert result.returncode == 0
    assert "md2wechat" in result.stdout
    assert "0.1" in result.stdout


def test_cli_list_themes_shows_all_three() -> None:
    """``--list-themes`` 应输出 3 套主题。"""
    result = _run(["--list-themes"])
    assert result.returncode == 0
    assert "sci-tech" in result.stdout
    assert "science-popular" in result.stdout
    assert "marketing" in result.stdout


def test_cli_list_themes_exits_0() -> None:
    """``--list-themes`` 是纯查询，应退出 0。"""
    result = _run(["--list-themes"])
    assert result.returncode == 0


def test_cli_missing_input_exits_2() -> None:
    """不存在的输入文件应退出码非零（约定 2）。"""
    result = _run(["-i", "/nonexistent/path.md"])
    assert result.returncode != 0


def test_cli_unknown_theme_exits_2() -> None:
    """非法主题名应被 argparse 拒绝（exit 2）。"""
    result = _run(["-i", str(FIXTURE), "-t", "nonexistent"])
    assert result.returncode == 2


def test_cli_convert_one_file(tmp_path: Path) -> None:
    """单文件转换：输出应满足内联样式不变量。"""
    out = tmp_path / "out.html"
    result = _run([
        "-i", str(FIXTURE),
        "-o", str(out),
        "-t", "sci-tech",
    ])
    assert result.returncode == 0, result.stderr
    assert out.exists()
    html = out.read_text(encoding="utf-8")
    assert 'class="' not in html
    assert "<style" not in html.lower()
    assert "<link" not in html.lower()
    assert "<script" not in html.lower()


def test_cli_convert_to_stdout(tmp_path: Path) -> None:
    """无 ``-o`` 时输出到 stdout。"""
    result = _run(["-i", str(FIXTURE), "-t", "sci-tech"])
    assert result.returncode == 0
    assert "<section" in result.stdout
    assert 'class="' not in result.stdout


def test_cli_strict_with_external_image_exits_nonzero(tmp_path: Path) -> None:
    """``--strict`` + 含外链图但未 -d 应退出非零（3）。"""
    md = tmp_path / "external.md"
    md.write_text(
        "# 外链图\n\n![external](https://example.com/foo.png)\n",
        encoding="utf-8",
    )
    out = tmp_path / "out.html"
    result = _run([
        "-i", str(md),
        "-o", str(out),
        "--strict",
    ])
    assert result.returncode == 3, result.stderr


def test_cli_batch_writes_to_dir(tmp_path: Path) -> None:
    """``--batch`` 应把所有匹配文件写到输出目录。"""
    out_dir = tmp_path / "batch"
    pattern = str(FIXTURE)  # 单文件也算 glob 匹配
    result = _run([
        "--batch", pattern,
        "-t", "sci-tech",
        "-o", str(out_dir),
    ])
    assert result.returncode == 0, result.stderr
    files = list(out_dir.glob("*.wechat.html"))
    assert files, f"未生成任何 .wechat.html 文件到 {out_dir}"


def test_cli_batch_no_match_exits_2(tmp_path: Path) -> None:
    """``--batch`` 无匹配文件应退出非零。"""
    result = _run(["--batch", str(tmp_path / "nonexistent-*.md")])
    assert result.returncode == 2


# Sanity check: 如果测试运行器找不到 fixture，整个模块 skip
if not FIXTURE.exists():
    pytest.skip(f"fixture not found: {FIXTURE}", allow_module_level=True)


# Sanity check: Python >= 3.10 才支持 md2wechat
if sys.version_info < (3, 10):
    pytest.skip("requires Python 3.10+", allow_module_level=True)


# Sanity check: 工具包可被 import
if shutil.which(sys.executable) is None:
    pytest.skip("python3 not found", allow_module_level=True)