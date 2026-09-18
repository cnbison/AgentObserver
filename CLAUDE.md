# CLAUDE.md

> 本文件是 **Claude Code** 在本仓库的会话指南。每条任务执行完毕后，请在文末追加变更记录并推送（详见 §6）。

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

## 6. CLAUDE.md 维护规则（重要）

> **每次任务执行完毕后**，Claude 必须：

### 6.1 必做动作

1. 在本文件 §7「近期变更」追加一条记录
2. `git add CLAUDE.md` + `git commit -m "..."` + `git push origin main`
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
- 不要删除历史记录（除非确认是错误条目）
- 同一会话连续多个小任务可以合并为一条记录，但每次会话结束前必须 push

---

## 7. 近期变更

### 2026-09-18 · 替换 FIG 5.1 / FIG 8.1 为用户提供的 PNG

- 新增 `assets/agent-observer/fig5.1.png`（84 KB）与 `fig8.1.png`（107 KB），由用户提供
- 替换 `marketing/gosim_survey_agent_hackathon_intro.md` 第 162–174 行（FIG 5.1 ASCII → 图）
- 替换 `marketing/gosim_survey_agent_hackathon_intro.md` 第 221–243 行（FIG 8.1 ASCII → 图）
- 同步更新：
  - 文首摘要行（图数从「6 张」改为「8 张」）
  - 附录版权表新增 FIG 5.1 与 FIG 8.1 两条记录

**Commit**: 76cb837

### 2026-09-18 · 新增英文参赛者简报 PDF 的 md 整理版

- 新增 `marketing/gosim_survey_agent_hackathon_intro.md`（≈ 380 行 / 16 节 / 6 图）
  - 文首中文摘要 + 16 节中文标题对照表（方便中文参赛者定位）
  - 保留英文原文（与官方 PDF 一致）
  - 6 张配图从 PDF 提取到 `assets/agent-observer/pdf-fig-*.jpg`，按章节语义命名
  - 3 处 ASCII 图：FIG 5.1 数据流图、FIG 8.1 内容字典、§3 名词表（PDF 中为矢量框图，无独立光栅图）
  - 附录：6 张图的版权与授权清单（含 NASA Hubble 公共领域、DESI CC BY 4.0）

**Commit**: 1acb738

### 2026-09-17 · 新增 starter-kit 深度分析文档

- 新增 `agent-observer-starter-kit-ANALYSIS.md`（≈ 400 行）：源码级拆解，11 节
  - §1 仓库结构与代码地图
  - §2 协议层 `participant-agent-protocol-v1`（JSON-Lines + 时间安全 + 校验链）
  - §3 评分层 `challenge-score-v3`（质量带、终局惩罚、临时请求）
  - §4 仿真层（observing_calendar / tile_geometry / weather_simulator / observation_request_simulator）
  - §5 Agent 流水线 LangGraph `prepare → invoke_model → finalize`
  - §6 评测主循环 `ChallengeWorkflow.run` 6 步
  - §7 策略空间与瓶颈分析 + 进阶方向 7 个表
  - §8 本地 vs 平台 5 个差异点
  - §9 给参赛者的 7 条具体建议
  - §10 一句话架构图
  - §11 局限与下一步 + 附录 A 关键文件交叉索引 + 附录 B 评分契约快照
- 更新 `README.md`：仓库结构图加入新文档；阅读路径表加 #5 进阶必读项

**Commit**: 018b2aa

### 2026-09-17 · 新增 GOSIM 推广 PDF 与官方 starter kit 源码

- 新增 `.gitignore`：排除 `.DS_Store`、`run_output/`、`demo_week_output/`、`**/scratch/`、`__pycache__/`、IDE 配置等
- 新增 `marketing/gosim_survey_agent_hackathon_intro.pdf`（英文 2 MB）与 `gosim_survey_agent_hackathon_intro_cn.pdf`（中文 10.8 MB）
- 新增 `agent-observer-starter-kit/` 整个目录：BH3GEI/agent-observer 官方入门包源码
  - `agent/`：参赛智能体实现（`my_strategy.py` / `minimal_agent.py` / `decision_graph.py` / `state.py` / `protocol.py` / `model_factory.py` / `reference_strategy.py` 等）
  - `challenge/`：评分器 / 工作流 / 模拟器 / 复盘模板
  - `scenarios/dev-reference/`（180 夜）+ `scenarios/demo-week/`（7 夜）公开场景
  - 启动脚本 `run_baseline.command/.bat/.sh` + `run_demo_week.*`
  - 文档：`QUICKSTART.md` + `QUICKSTART_ZH.md` + `README.md` + `SKILL.md`

**Commit**: d466db5

### 2026-09-17 · 新增 CLAUDE.md 会话指南

- 新建 `CLAUDE.md`，作为本仓库的 Claude Code 会话指南
- 涵盖项目概述 / 仓库结构 / 核心约定 / Git 工作流 / 工具速查
- §6 定义"每次任务后追加变更记录并推送"的维护规则
- §7 作为滚动 changelog，后续任务在此追加

**Commit**: 3af61a3