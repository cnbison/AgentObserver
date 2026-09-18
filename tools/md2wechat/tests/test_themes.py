"""主题预设的字段完整性测试。"""

from __future__ import annotations

import pytest

from md2wechat.themes import (
    MARKETING,
    SCIENCE_POPULAR,
    SCI_TECH,
    THEMES,
    Theme,
    get_theme,
)


# 每个 Theme 的必填字段集合；``tr`` 允许为空字符串（不强制样式）
REQUIRED_FIELDS: tuple[str, ...] = (
    "name", "description",
    "section", "body",
    "h1", "h2", "h3", "h4",
    "p", "strong", "em", "s",
    "blockquote",
    "ul", "ol", "li",
    "a",
    "code_inline", "pre",
    "img",
    "table", "th", "td", "tr",
    "hr",
)


@pytest.mark.parametrize(
    "theme",
    [SCI_TECH, SCIENCE_POPULAR, MARKETING],
    ids=["sci-tech", "science-popular", "marketing"],
)
def test_theme_is_dataclass_instance(theme: Theme) -> None:
    """主题必须是 Theme dataclass。"""
    assert isinstance(theme, Theme)


@pytest.mark.parametrize(
    "theme",
    [SCI_TECH, SCIENCE_POPULAR, MARKETING],
    ids=["sci-tech", "science-popular", "marketing"],
)
def test_theme_required_fields_non_empty(theme: Theme) -> None:
    """每个必填字段非空（``tr`` 允许为空字符串）。"""
    for field in REQUIRED_FIELDS:
        value = getattr(theme, field)
        if field == "tr":
            continue  # <tr> 不强制样式，允许空字符串
        assert value, f"{theme.name}.{field} 不应为空"


@pytest.mark.parametrize(
    "theme",
    [SCI_TECH, SCIENCE_POPULAR, MARKETING],
    ids=["sci-tech", "science-popular", "marketing"],
)
def test_theme_h_field_distinct(theme: Theme) -> None:
    """h1/h2/h3/h4 四个标题字段应两两不同（避免主题串色）。"""
    hs = {theme.h1, theme.h2, theme.h3, theme.h4}
    assert len(hs) == 4, f"{theme.name} 标题样式两两重复"


def test_themes_registry_contains_all_presets() -> None:
    """注册表应包含全部 3 套预设。"""
    assert set(THEMES) == {"sci-tech", "science-popular", "marketing"}


def test_themes_registry_dataclass_frozen() -> None:
    """Theme 是 frozen dataclass（不可写）。"""
    with pytest.raises(Exception):  # FrozenInstanceError 来自 dataclasses
        SCI_TECH.h1 = "mutated"  # type: ignore[misc]


def test_get_theme_returns_correct_instance() -> None:
    """``get_theme`` 按名取主题。"""
    assert get_theme("sci-tech") is SCI_TECH
    assert get_theme("science-popular") is SCIENCE_POPULAR
    assert get_theme("marketing") is MARKETING


def test_get_theme_unknown_raises_with_list() -> None:
    """未知主题名应抛 KeyError 且提示可用列表。"""
    with pytest.raises(KeyError, match=r"未知主题"):
        get_theme("nonexistent")
    with pytest.raises(KeyError, match=r"sci-tech"):
        get_theme("nonexistent")