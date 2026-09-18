# AgentObserver

> 本仓库收纳 **GOSIM 巡天智能体黑客松（Agent Observer）** 的完整说明文档与展示素材。
> 数据来源：[create.gosim.org/survey26](https://create.gosim.org/survey26/) 及配套的比赛平台 [bh3gei.github.io/agent-observer](https://bh3gei.github.io/agent-observer/)。

---

## 📚 阅读路径

| # | 文档 | 用途 |
|---|---|---|
| 0 | **[survey26.md（仓库根）](survey26.md)** | 首页 / 总览 —— 愿景、赛题、如何参赛、奖项、排行榜入口 |
| 1 | [references/survey26.md](references/survey26.md) | 总览（与 `survey26.md` 同源；根目录的 `survey26.md` 是软链） |
| 2 | [references/survey26_brief.md](references/survey26_brief.md) | **赛题简报** —— 8 章完整解释：为什么 / 观测员职责 / 挑战赛制 / 规划尺度 / 参赛任务 / 计分 / 名词 / 时间线 |
| 3 | [references/survey26_start.md](references/survey26_start.md) | **新手上路** —— 6 步 + 卡住了速查表：注册 → 建队 → 下载入门包 → 改 `choose_action` → 上传 → 看分 |
| 4 | [references/survey26_rules.md](references/survey26_rules.md) | **比赛规则与评分** —— 9 节：资格 / 阶段 / 提交 / 平台运行 / **评分公式 (`challenge-score-v3`)** / 排名 / 奖项 / 准则 / 隐私 |
| 5 | [agent-observer-starter-kit-ANALYSIS.md](agent-observer-starter-kit-ANALYSIS.md) | **入门包源码深度分析** —— 协议 / 评分 / 仿真 / Agent 流水线 / 策略空间 / 7 条参赛建议（**进阶必读**） |
| 6 | [articles/agent-observer-promo.md](articles/agent-observer-promo.md) | **Agent Observer 黑客松推广长文** —— 1800 字 / 8 配图 / 对标兄弟赛事版本风格，可直接送 `gzh-design` 排版 |

> 💡 **推荐阅读顺序**：`survey26.md`（总览）→ `survey26_brief.md`（理解赛题）→ `survey26_start.md`（动手做）→ `survey26_rules.md`（核对细节）。
> 📰 **对外宣传**：`articles/agent-observer-promo.md` 是已发布的中文公众号长文稿。

---

## 🗂 仓库结构

```
AgentObserver/
├── README.md                    ← 本文件（入口与导航）
├── CLAUDE.md                    ← Claude Code 会话指南（含维护规则 + 近期变更）
├── survey26.md                  ← 软链 → references/survey26.md
├── references/
│   ├── survey26.md              ← 总览
│   ├── survey26_brief.md        ← 赛题简报（8 章）
│   ├── survey26_start.md        ← 新手上路（6 步）
│   └── survey26_rules.md        ← 比赛规则与评分（9 节）
├── marketing/                   ← 市场推广（4 份运营文档）
│   ├── plan.md                  ← 推广方案
│   ├── copy-bank.md             ← 文案库
│   ├── video-scripts.md         ← 视频脚本
│   └── production-workflow.md   ← 制作流程 SOP
├── articles/                   ← 推广文章（已发布稿件）
│   └── agent-observer-promo.md ← ★ Agent Observer 黑客松推广长文（约 1900 字 / 8 配图）
├── agent-observer-starter-kit-ANALYSIS.md ← ★ starter-kit 源码级深度拆解（11 节）
└── assets/
    └── agent-observer/          ← GOSIM Agent Observer 公开素材
        ├── gosim-logo.svg
        ├── cosmos-control-room-DALcRogD.jpg
        ├── cosmos-dome-D1P_eEvz.jpg
        ├── cosmos-instrument-CSD2molP.jpg
        ├── cosmos-observatory-hero-BV_aYwWD.jpg
        ├── survey-agent-strategy-XnSuOIcZ.jpg
        ├── survey-cosmic-web-DYzNpylI.jpg
        ├── survey-night-sky.mp4            ← 主视觉视频
        ├── survey-observed-universe-BvpCJuOC.jpg
        ├── survey-redshift-map-Bal3YYAj.jpg
        ├── survey-review-overlay-BD2bBt4R.jpg
        ├── fig5.1.png
        ├── fig8.1.png
        ├── pdf-fig-1-1-cosmic-web.jpg
        ├── pdf-fig-1-2-desi-redshift.jpg
        ├── pdf-fig-10-1-3d-universe.jpg
        ├── pdf-fig-10-2-review-overlay.jpg
        ├── pdf-fig-10-3-alpha-sweep.jpg
        └── pdf-fig-10-4-desi-butterfly.jpg
```

---

## 🔗 外部资源

- **官方赛事页**：[create.gosim.org/survey26](https://create.gosim.org/survey26/)
- **赛题简报（在线）**：[create.gosim.org/survey26/brief](https://create.gosim.org/survey26/brief)
- **比赛平台**：[bh3gei.github.io/agent-observer](https://bh3gei.github.io/agent-observer/)
- **新手上路（在线）**：[bh3gei.github.io/agent-observer/start](https://bh3gei.github.io/agent-observer/start)
- **规则（在线）**：[bh3gei.github.io/agent-observer/rules](https://bh3gei.github.io/agent-observer/rules)
- **排行榜（在线）**：[bh3gei.github.io/agent-observer/leaderboard](https://bh3gei.github.io/agent-observer/leaderboard)
- **GOSIM 主站**：[gosim.org](https://gosim.org/)

---

## 📦 数据来源说明

- 全部内容由本地渲染拉取自上述官方页面后整理为 Markdown。
- 所有图片 / 视频来自官方 `/survey26/assets/` 与 `/survey26/media/` 路径，原版权归属 GOSIM / DESI collaboration 等。
- 在线页面如有更新，本仓库的 Markdown 版本可能略有滞后；正式参赛请以比赛平台实时公告为准。

---

## 📝 编辑约定

- `references/` 下 4 个 Markdown 文件是**单一事实来源**，根目录的 `survey26.md` 是软链方便直达。
- 跨文件链接使用相对路径（如 `[赛题简报](survey26_brief.md)`）。
- 资源路径统一为 `../assets/agent-observer/<filename>`（不在引用文档里写绝对 URL，避免仓库迁移失效）。
- 新增素材请放入 `assets/agent-observer/` 并在对应文档中引用。

---

## 📣 市场推广

> 配套 4 份运营文档（≈ 1500 行 Markdown，可直接当工作手册）：

| 文档 | 内容 |
|---|---|
| [marketing/plan.md](marketing/plan.md) | **总体方案** —— 推广目标 / KPI / 受众画像 / 内容矩阵（30 选题）/ 内容日历 / 账号矩阵 / 视频大纲 / 风险预案 / 团队分工 / 预算 |
| [marketing/copy-bank.md](marketing/copy-bank.md) | **文案库** —— 30 条选题 × 多平台版本（公众号 / 知乎 / Medium / 微博 / X / 小红书 / 抖音）+ 发布日历 + 通用 CTA + 标签词库 |
| [marketing/video-scripts.md](marketing/video-scripts.md) | **视频脚本** —— 4 类片（概念片 / 教程片 / 深度片 / 颁奖片）+ 直播脚本 + 字幕与配乐规范 + Checklist |
| [marketing/production-workflow.md](marketing/production-workflow.md) | **制作流程 SOP** —— 7 阶段流水线 + 视觉规范 + 工具栈矩阵 + 紧急预案 + 起手组合（最小成本 < ¥200/月） |

### 一图流

```
marketing/
├── plan.md                  ← 推广方案（目标 / 选题 / 日历 / 团队）
├── copy-bank.md             ← 30 选题 × 多平台文案
├── video-scripts.md         ← 4 类视频 + 直播脚本
└── production-workflow.md   ← 7 阶段 SOP + 工具栈
```