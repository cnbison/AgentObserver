# md2wechat — Markdown → 微信公众号文章 HTML 转换器

> 本目录的工具把项目里的 Markdown（特别是 `marketing/*.md` 双语简报）转成**可直接粘贴到微信公众号草稿箱**的 HTML。  
> 所有 CSS 强制内联，可选下载外链图，三套主题预设与 `marketing/production-workflow.md §4.3` 视觉规范对齐。

## 安装

依赖项（`markdown-it-py`、`pygments`、`pyyaml`）已在本仓库常用 Python 环境内可用，无需安装步骤：

```bash
python3 -m md2wechat --version
```

## 快速使用

```bash
# 列出所有主题
python3 -m md2wechat --list-themes

# 单文件转换
python3 -m md2wechat \
    -i marketing/gosim_survey_agent_hackathon_intro.md \
    -o marketing/dist/intro.wechat.html \
    -t sci-tech

# 下载外链图（避免公众号拦截）
python3 -m md2wechat \
    -i post.md \
    -o post.wechat.html \
    -d --image-dir assets/wechat/

# 批量转换
python3 -m md2wechat --batch "marketing/*.md" -t marketing
```

## 公众号渲染限制（必读）

详见 `python3 -m md2wechat --help` 末尾的清单。简言之：

1. 公众号会拦截外链图 → 需用 `-d` 下载到本地再上传到「素材管理」
2. 只支持内联 CSS —— class 选择器与 `<style>/<link>/<script>` 会被剥离
3. 外链会被改写到 `mp.weixin.qq.com`，`target="_blank"` 不生效
4. 草稿箱需在移动端实测：桌面样式可能与手机不一致
5. 不支持嵌套表格 / 单元格合并 / colspan

## 主题对照表

| 预设 | 配色 | 用途 |
|---|---|---|
| `sci-tech`（默认） | 深空蓝 `#18242f` + 暖橙 `#edb28b` | 与 `marketing/production-workflow.md §4.3` 一致 |
| `science-popular` | 海军蓝 `#1f4e79` + 沙金 `#f4a261` | 科普长文，亲民 |
| `marketing` | 大红 `#d62828` + 琥珀 `#fcbf49` | 推广文案，紧凑 |

## CLI 参数

| 参数 | 说明 |
|---|---|
| `-i / --input <path>` | 单个输入 markdown（默认 stdout） |
| `--batch <glob>` | 批量转换（输出到 `marketing/dist/`） |
| `-o / --output <path>` | 输出 HTML（默认 stdout） |
| `-t / --theme <name>` | 主题（默认 `sci-tech`） |
| `-d / --download-images` | 下载外链图到本地 |
| `--image-dir <path>` | 外链图下载目录（默认 `assets/wechat/`） |
| `--no-frontmatter` | 保留 YAML frontmatter（默认会自动移除） |
| `--strict` | 存在外链图且未 `-d` 时 exit 非零 |
| `-v / --verbose` | 输出处理详情 |

## 开发

```bash
cd tools/md2wechat
python3 -m pytest tests/ -v
```

## 路线图

- **v0.1（当前）**：基础 md → 公众号 HTML + 代码高亮 + 图片本地化 + 主题预设
- **v0.2**：YAML frontmatter schema 校验（pyyaml）；图片 base64 fallback；批量发布到公众号 API