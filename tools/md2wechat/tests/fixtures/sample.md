---
title: md2wechat 测试样例
author: Claude
date: 2026-09-18
tags: [wechat, markdown, test]
---

# 标题 H1：md2wechat 测试样例

> 本文件用于 ``tests/test_renderer_inline.py`` 与 ``tests/test_cli.py``，覆盖 markdown 的常见元素，确保转换器在所有主题下都满足「内联样式」不变量。

## §1 段落与强调

这是一段普通**粗体**与*斜体*与~~删除线~~与 `inline code` 的混合文本。也可以混合使用 ***粗斜体*** 与 **[带强调的链接](https://example.com)**。

## §2 列表

无序列表：

- 列表项 A
- 列表项 B
  - 嵌套项 B-1
  - 嵌套项 B-2
- 列表项 C

有序列表：

1. 第一步
2. 第二步
3. 第三步

## §3 引用与代码块

> 引用块：这是引用的文字内容。
> 引用支持多行。

围栏代码块（含 Python）：

```python
def hello(name: str) -> str:
    return f"hello, {name}"

if __name__ == "__main__":
    print(hello("world"))
```

围栏代码块（含 Bash，无高亮）：

```bash
echo "plain shell"
ls -la /tmp
```

## §4 表格

| 列 A | 列 B | 列 C |
|---|---|---|
| 单元格 1 | 单元格 2 | 单元格 3 |
| 单元格 4 | 单元格 5 | 单元格 6 |

## §5 图片与链接

![本地相对路径](relative/path/foo.jpg)

![网络路径](https://example.com/bar.png "图片标题")

[外部链接示例](https://example.com)

---

> 📝 文末注：本文件不应在转换输出里出现任何 ``class="..."`` 或 ``<style>`` / ``<link>`` / ``<script>`` 标签。