# CLAUDE.md

> 本文件是 **Claude Code** 在本仓库的会话指南。每条任务执行完毕后，请在 [CHANGELOG.md](./CHANGELOG.md) 追加变更记录并推送（详见 §6）。

---

## 1. 项目概述

**AgentObserver** 是 **GOSIM 巡天智能体黑客松（Agent Observer）2026** 的中文资料仓库。

- **赛事方**：GOSIM / BH3GEI（GitHub Pages 双部署）
- **赛程**：线上培训 10.1–10.4 / 线上比赛 10.5–10.7 / 颁奖 10.17（深圳）
- **数据来源**：
  - 主站：`https://create.gosim.org/survey26/`
  - 比赛平台：`https://bh3gei.github.io/agent-observer/`
- **本仓库用途**：将上述页面的内容本地化、整理为 Markdown，供内部学习、内容复用、对外宣传使用
- **代码仓库定位**：**纯文档仓库**，不包含比赛平台实现（比赛平台代码在 `BH3GEI/agent-observer` 独立仓库）

---

## 2. 仓库结构

```
AgentObserver/
├── README.md                      ← 仓库入口与导航
├── CLAUDE.md                      ← 本文件（Claude Code 会话指南）
├── survey26.md  (→ symlink)       ← 软链到 references/survey26.md
├── references/                    ← 核心文档（单一事实来源）
│   ├── survey26.md                ← 总览：愿景 / 赛题 / 如何参赛 / 奖项 / 排行榜
│   ├── survey26_brief.md          ← 赛题简报（8 章完整说明）
│   ├── survey26_start.md          ← 新手上路（6 步 + 卡住了速查表）
│   └── survey26_rules.md          ← 比赛规则与评分（9 节 + 评分公式）
├── marketing/                     ← 市场推广运营文档
│   ├── plan.md                    ← 推广方案（目标 / 选题 / 日历 / 团队）
│   ├── copy-bank.md               ← 文案库（30 选题 × 多平台版本）
│   ├── video-scripts.md           ← 视频脚本（4 类片 + 直播 + Checklist）
│   └── production-workflow.md     ← 制作流程 SOP + 工具栈
├── tools/                         ← 内部工具（独立 CLI 包）
│   └── md2wechat/                 ← Markdown → 微信公众号文章 HTML 转换器
│       ├── README.md              ← 用法 + 公众号限制清单 + 主题对照表
│       ├── pyproject.toml         ← 包元数据（依赖 markdown-it-py / pygments / pyyaml）
│       ├── md2wechat/             ← Python 包源码
│       │   ├── cli.py             ← argparse CLI（-i / --batch / --list-themes）
│       │   ├── themes.py          ← 3 套主题预设（sci-tech / science-popular / marketing）
│       │   ├── renderer.py        ← markdown-it 自定义渲染（18 个 token 类型 + Pygments）
│       │   ├── converter.py       ← 编排管线（frontmatter 剥离 + 外链图下载 + 渲染）
│       │   ├── __main__.py        ← python3 -m md2wechat 入口
│       │   └── __init__.py
│       └── tests/                 ← pytest 测试（45 passed）
│           ├── test_themes.py
│           ├── test_renderer_inline.py
│           ├── test_cli.py
│           └── fixtures/sample.md
└── assets/
    └── agent-observer/            ← GOSIM Agent Observer 公开素材
        ├── gosim-logo.svg
        ├── cosmos-*.jpg           ← 4 张实景图
        ├── survey-*.jpg           ← 5 张数据 / 示意图
        └── survey-night-sky.mp4   ← 主视觉视频
```

---

## 3. 核心约定

### 3.1 文件路径

- 所有 markdown 文档（含根目录软链）使用 **相对路径** 互链
- 跨文件链接：从 `references/` 出发用 `survey26_xxx.md`（同目录）；从根 `survey26.md` 软链出发同理
- 素材引用：固定格式 `../assets/agent-observer/<filename>`（所有 md 文件都在 `references/` 或根目录的 `references/` 链接下游）
- **禁止**使用绝对 URL（如 `https://create.gosim.org/...`）作为内链 —— 仅在外链/CTA/外部资源引用处使用绝对 URL
- 内部工具放 `tools/<name>/`，与文档代码隔离；命名同 Python 包（避免与 `references/` / `marketing/` 主题命名冲突）

### 3.2 文档命名

- 主文档：`survey26.md`、`survey26_brief.md`、`survey26_start.md`、`survey26_rules.md`
- 营销文档：放 `marketing/`，单数英文命名（如 `plan.md`、`copy-bank.md`）
- 新增主题时：在 `references/` 或 `marketing/` 下新增同前缀文件，并在 `README.md` 与相关 md 的目录中登记

### 3.3 文档风格

- **中文优先**（赛事是中文主办）；英文片段允许（如 `score = base_science + ...`）
- Markdown 渲染目标：GitHub + Vitepress + Hugo 通用兼容
- 表格用 GFM 标准语法（带表头分隔行）
- 代码块使用 ` ``` ` 三反引号（带语言标记）
- 关键数字 / 路径 / 警告用 `**粗体**` 突出
- 引述用 `> blockquote`，可叠加 emoji（📄 🚀 📜 ⚠️ 💡）

### 3.4 不要做的事

- ❌ 不要把 `references/` 文件搬到根目录（根目录 `survey26.md` 已经是软链）
- ❌ 不要修改 `assets/agent-observer/` 中的文件名（GOSIM 哈希文件名保留）
- ❌ 不要臆造数据 —— 所有数字、日期、奖金必须引用官方页面或 `references/` 文档
- ❌ 不要把比赛平台代码（Vue / Supabase）加到这个仓库 —— 那是 `BH3GEI/agent-observer` 的职责
- ❌ 不要在 md 中嵌入超长 base64 图片

---

## 4. 远程与协作

- **remote**：`https://github.com/cnbison/AgentObserver.git`（owner: `cnbison`）
- **分支**：`main`（单一主分支，GitHub Flow）
- **commit 作者**：默认 `cnbison`
- **commit 风格**：中文一句话标题 + 详细列表 + `Co-Authored-By: Claude <noreply@anthropic.com>`

### 4.1 Commit 模板

```
<一句话动作>

- 改动点 1
- 改动点 2
- 改动点 3

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 4.2 Push 策略

- 每个有意义的变更都 commit + push（不堆积）
- 软链（symlink）必须在仓库启用 `core.symlinks = true`
- 推送到 main 后无需开 PR

---

## 5. 常用工具速查

| 场景 | 命令 |
|---|---|
| 渲染 SPA 页面 | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-sandbox --virtual-time-budget=10000 --dump-dom "<URL>" > /tmp/<name>.html` |
| HTML → Markdown | turndown（`/tmp/node_modules/turndown`），脚本 `node convert.js` |
| 提取中文 | `LC_ALL=C grep -oE '[一-鿿]{3,}' file | sort -u` |
| 下载图片 | `curl -sL "<url>" -o "path"` |
| git 状态 | `git status --short` |
| 提交推送 | `git add -A && git commit -m "..." && git push origin main` |

---

## 6. 维护规则（重要）

> **每次任务执行完毕后**，Claude 必须：

### 6.1 必做动作

1. 在 [CHANGELOG.md](./CHANGELOG.md) 文末追加一条记录
2. `git add -A` + `git commit -m "..."` + `git push origin main`
3. 不要因为"改动小"而跳过 —— 即便是文档同步或小修正也要记录

### 6.2 记录格式

```markdown
### YYYY-MM-DD · <一句话任务名>

- 改动点 1
- 改动点 2
- ...

**Commit**: <short-sha>
```

- 日期使用**今天日期**（参考 system reminder 中的 currentDate）
- 任务名简洁（10–20 字）
- 改动点用要点列出
- 末尾给出 commit 短哈希

### 6.3 注意事项

- 已有记录按**倒序**排列（最新在上）
- 不要删除 CHANGELOG.md 中的历史记录（除非确认是错误条目）
- 同一会话连续多个小任务可以合并为一条记录，但每次会话结束前必须 push
- **CLAUDE.md 不再承载变更记录**：2026-09-18 之前的 14 条历史已迁移到 CHANGELOG.md

### 6.4 为什么变更记录要单独建文件

- CLAUDE.md 是给 Claude 看的会话指南，频繁追加变更记录会稀释指南本身的信号
- CHANGELOG.md 是项目级历史档案，独立、可独立引用、不会被规则文档污染
- 仓库维护者（人类）看 CHANGELOG.md 看演进；Claude 看 CLAUDE.md 看规则——职责分离

---

## 7. 变更记录（指针）

> ⚠️ **本节不再承载变更记录**——所有变更已迁移到独立的 [CHANGELOG.md](./CHANGELOG.md)。
>
> 历史脉络请查阅：
>
> - **[CHANGELOG.md](./CHANGELOG.md)** ← 全部历史 + 未来新增
> - 2026-09-18 之前的 14 条历史（含原始 commit 短哈希）已完整迁移保留
>
> 维护规则详见 §6。