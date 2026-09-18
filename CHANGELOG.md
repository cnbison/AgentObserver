# CHANGELOG · AgentObserver 仓库变更记录

> 本文件按**倒序**记录仓库所有有意义的变更（最新在上）。
>
> **历史来源**：2026-09-17 至 2026-09-18 早段共 14 条记录从 `CLAUDE.md §7` 迁移而来；此后所有任务变更均按 [CLAUDE.md §6](./CLAUDE.md) 规则追加到本文件，不再写回 `CLAUDE.md`。

---

### 2026-09-18 · 把 agent-observer-promo-01.md 排版成红白色系公众号 HTML

- 用 `gzh-design` skill（主题 `theme-red-white`，红白色系）把用户修正版 `articles/agent-observer-promo-01.md` 渲染为公众号合规 HTML
  - 骨架：开头引言卡（白底红色光晕 / `900 秒` + `180 个夜` 红底白字高亮）+ 封面图 + 开场白（2 段，每段 1~3 处淡粉下划线）+ 本文看点 3 列 + 6 章编号章节（HOW IT WORKS / KEY NUMBERS / SCHEDULE / THREE PRINCIPLES / WHAT YOU GET / GET STARTED）+ 结语章（∞ + THE END + 版权表 + 维护者信息）+ END 分割线 + 尾部签名占位
  - §02 数字速览：2 行 × 4 列数据卡组（$5,500 / 6 奖 / 180 夜 / 900s / 1–8 人 / 12,287 / Python 3.12 / 90 天）+ 奖项结构表
  - §03 赛程：阶段表 + 9a 红色提示条（练习赛 50 次 / 正式赛 10 次）+ cosmos-control-room 控制室图（含图注）
  - §04 三大原则：11b pill-list（红点前缀 + 浅红底深红字标签）
  - §05 你能获得什么：11a 红色圆标数字编号列表 + 8c 灰底旁注（领奖不要求到场）
  - §06 现在就开始：20 分钟跑通基线钩子 + 官方入口链接卡 + 8d 居中金句分隔 + 封面图复用收尾
- 智能处理：209 处 `<span leaf>` 包裹完整；每段 1~3 处淡粉下划线关键词；红色加粗锚点 ≤5 处（产品名 / 关键数据 / CTA）；签名区用 `{{作者名}}` 占位由用户替换
- 全角弯引号：将原文 5 处英文直引号 `"..."` 替换为「...」（符合公众号排版规范）
- 校验：`validate_gzh_html.py` ERROR=0 + WARNING=0 ✅ 完全合规
- 预览：`wrap_preview.py` 生成带「复制到公众号」按钮的预览页
- 输出两份文件：
  - `articles/agent-observer-promo-01_排版_红白色系(red-white).html`（干净正文，粘贴用）
  - `articles/agent-observer-promo-01_排版_红白色系(red-white)_预览.html`（预览页，推荐）

---

### 2026-09-18 · 删除 references/ 下两份兄弟参考文 HTML（已转 md）

- 删除 `references/GOSIM Shenzhen 2026 智能体软件工厂...html`（3.6 MB）
- 删除 `references/GOSIM Spotlight Shenzhen 2026 全球 AI 项目...html`（3.8 MB）
- 原因：两份 HTML 已被对应 md 替代（内容无新增）
  - `marketing/gosim_factory_hackathon_intro.md`（11.8 KB / 6 节 / 4 配图）
  - `marketing/gosim_spotlight_intro.md`（16.4 KB / 5 节 / 6 配图）
- 全仓扫描引用：仅 CLAUDE.md §7 历史 changelog 提及 html 文件名，按 §6.3 "不删历史记录"保留不动；正文（README / 兄弟赛事 md）**无任何对 references/ html 的引用**——两份兄弟赛事 md 内引用的都是 create.gosim.org / spotlight.gosim.org 外链，不受影响
- 历史 changelog（L225-228 / mhtml→html 那条）保留不动作为事实记录

### 2026-09-18 · 将 Spotlight 兄弟赛事 HTML 转 md 并优化显示

- 新增 `marketing/gosim_spotlight_intro.md`（16440 字节 / 5 节 + 附录 A–B）
  - 文首中文摘要 + 5 节 TOC
  - §1 何为 Spotlight（6 大主题论坛 + 千名参会者 + 7 条产品方向 + "品类重构"）
  - §2 为何参加（4 大支持：20 个项目 + 100 美元原型补助 + 6 项现场支持 GFM 表
    + 5 类现场指导 GFM 表 + 全球传播）
  - §3 如何参赛（2 条路径 + 7 项 Agent OS 能力 + 3 个关注问题 + 5 个特征
    + 8 个推荐方向 + 3 类产品形态）
  - §4 首轮 9 月 13 日截止（5 阶段流程图 + 5 项核心材料 + 8 道必答题
    + 3 大评审维度：主观 60% + 客观 40% + 7 项最终评选）
  - §5 同期赛事与大会入口（Spotlight / Factory / 黑客松 / 讲师 / 早鸟票 4 链接）
  - 附录 A：兄弟赛事三场表（Spotlight + Factory + Agent Observer 互链）
  - 附录 B：6 张图版权与署名
- 新增 `assets/sibling-spotlight/`：6 张图全下载到本地
  - spotlight-img-01.jpg（78 KB 装饰横幅）
  - spotlight-img-02.jpg（150 KB 项目提交引导）
  - spotlight-img-03.jpg（128 KB 5 阶段流程图）
  - spotlight-img-04.jpg（589 KB 现场活动支持图）
  - spotlight-img-05.jpg（9 KB 早鸟票引导图）
  - spotlight-img-06.jpg（2.5 KB 官方二维码）
- 关键数据校对（17 项全部命中）

### 2026-09-18 · 将 Factory 兄弟赛事 HTML 转 md 并优化显示

- 新增 `marketing/gosim_factory_hackathon_intro.md`（11828 字节 / 6 节 + 附录 A–D）
  - 文首中文摘要 + TOC + §1–§6 一级标题
  - §1 国际化舞台 / §2 关于赛事 / §3 三大核心原则 / §4 六周赛程（GFM 表格）
  - §5 你能获得什么（4 福利 GFM 表格）/ §6 即刻报名
  - 附录 A：同期 GOSIM Shenzhen 2026 大会信息 + 3 条入口链接
  - 附录 B：限时早鸟观众票福利（8.24–8.26）
  - 附录 C：兄弟赛事速览（Factory + Agent Observer 互链）
  - 附录 D：4 张图片版权与署名
- 新增 `assets/sibling-factory/`：4 张图全下载到本地
  - factory-img-01.jpg（2.6 KB 报名二维码）/ 02.jpg（178 KB 大会主视觉）
  - factory-img-03.jpg（72 KB 早鸟海报）/ 04.jpg（80 KB 早鸟二维码）
  - meta.json 记录图片元信息
- 关键数据校对（21 项全部命中）：24,000 美元 / 20 奖 / 6 周赛程 / Top 20 晋级 /
  150+ 讲师 / 2000+ 开发者 / 35 高校 / 48 企业 / 15 城市 / 87 名 / 249 支 / 8.24–8.26 早鸟福利

### 2026-09-18 · 重写 Agent Observer 推广长文（更醒目标题 + 简明告知）

- 重写 `articles/agent-observer-promo.md`（6796 字节 / 约 1400 中文字）
  - **标题改为 Factory 同款句式**：`GOSIM Agent Observer 黑客松重磅启动！180 个观测夜，$5,500 奖金池，等你来战！`
  - **写作重心调整**：从"9 项职责 / 状态字典 / 评分公式 / Python 3.12 沙箱技术细节" → "简明告知：这是什么比赛 / 谁参加 / 给什么 / 怎么开始"
  - **6 节骨架**：开场白 → 数字速览表 → 赛程表 → 三大原则 → 你能获得什么 → CTA 表
  - 数字密度提升：每节至少 1 个硬数据点（$5,500 / 6 奖 / 180 夜 / 900 秒 / 12,287 / 50+10 次 / 90 天）
  - 配图从 9 张减到 3 张（封面 + §03 控制室 + 结尾），聚焦读者注意力
  - DESI/NASA/Hubble 第三方图片本次未引用，无需署名
- 同步**替换 references/ 下两份兄弟参考文**为更干净的纯 HTML（mhtml → html）
  - `GOSIM Shenzhen 2026 智能体软件工厂黑客松重磅启动！...html`（3.6 MB）
  - `GOSIM Spotlight Shenzhen 2026 全球 AI 项目火热征集中...html`（3.8 MB）
  - 删除对应两份 `.mhtml`（base64 内嵌图噪音大）
- 全文 13 项关键事实校对过 `references/` 5 个文档，全部命中

### 2026-09-18 · 新增 Agent Observer 黑客松推广长文

- 新增 `articles/agent-observer-promo.md`（约 1900 字中文 / 8 张配图 / 6 节骨架）
  - 文首中文摘要 + TOC + 英文副标语 *Human judgment · Machine speed · One shared sky*
  - §1 这场黑客松在做什么（\$5,500 / 6 奖项 / 180 夜 / 900 秒时隙 / 12,287 基线）
  - §2 为什么难（9 项观测员职责 / 4 维状态字典 / 三层时间尺度 / FIG 8.1 状态字典）
  - §3 GOSIM 这场有什么不同（开放祛魅 / 公平竞技 / 真实落地 + DESI 5000 万星系借势）
  - §4 怎么参加（20 分钟跑通基线 / 6 步表 / 练习赛 csv vs 正式赛包 / Alpha 扫描 / 复盘叠加图）
  - §5 你能获得什么（奖金 + 深圳颁奖曝光 + 完赛证书 + 排行榜 + 90 天数据保留 + 领奖不要求到场）
  - §6 现在就开始（5 条 bh3gei.github.io 官方入口 CTA 表）
  - 附录 · 图片版权与署名：DESI Claire Lamman + NASA/Hubble 公共领域 + GOSIM 公开素材
- 全部 12 项关键事实校对过 `references/` 5 个文档（奖金池 / 奖项数 / 赛程 / 时隙 / 提交限制 / 每日次数 / 队伍规模 / 基线分数 / 评分公式 / Python 3.12 / 领奖要求 / 数据保留 90 天）
- 配图全部走 `../assets/agent-observer/` 相对路径，**零**外部 CDN 引用
- 对标兄弟项目推广文风格（学 Agentic Factory 的"赛事化 + 三大原则"骨架 + Spotlight 的"多漏斗 CTA + 降门槛金句"做法）
- 同步更新 `README.md`：仓库结构图加 `articles/` 目录与新增配图；阅读路径表加 #6 推广文入口

### 2026-09-18 · 新增 md2wechat 工具（Markdown → 微信公众号文章 HTML）

- 新增 `tools/md2wechat/`：Python 3.10+ 独立 CLI，把项目里的 `.md` 转成可直接粘贴到公众号草稿箱的 HTML
  - 核心：所有样式强制内联（公众号会剥离 `<style>` / `<link>` / `<script>` 与 `class=`）
  - 3 套主题预设（与 `marketing/production-workflow.md §4.3` 视觉规范对齐）：
    - `sci-tech`（默认）：深空蓝 `#18242f` + 暖橙 `#edb28b`
    - `science-popular`：海军蓝 `#1f4e79` + 沙金 `#f4a261`
    - `marketing`：大红 `#d62828` + 琥珀 `#fcbf49`
  - 围栏代码块走 Pygments 内联高亮（剥掉 Pygments 的 `<div class="highlight">` 包装）
  - 可选 `-d` 下载外链图到本地（避免公众号拦截）
  - `--batch` 批量转换；`--strict` 用于 CI 严格模式
  - 修复 markdown-it-py's `add_render_rule` `__get__` 绑定陷阱：所有回调必须 `staticmethod`
  - 修复 image `alt` 文本从 `token.content`（非 `token.attrs["alt"]`）取
  - 启用 `md.enable(["table", "strikethrough"])`（commonmark 默认未开）
- 新增 `marketing/dist/.gitkeep`：`--batch` 默认输出目录占位
- 新增 45 个 pytest 测试（themes 9 + renderer 19 + cli 10 + 7 个 parametrize），全部通过
- 真实 e2e：`marketing/gosim_survey_agent_hackathon_intro.md`（496 行中英双语，4 张表 100+ 单元格，8 张图）
  → 71 KB HTML，**0 个 `class=`**，**0 个 `<style|<link|<script>`**，3 套主题颜色与字号可见差异

**Commit**: b511e2a

### 2026-09-18 · §1–§16 主标题改为中英双语

- `marketing/gosim_survey_agent_hackathon_intro.md` 第 §1–§16 共 16 个 `## N.` 标题
  从「英文单语」改为「英文 · 中文」双语格式（与正文保持一致）
- 中文译名与 TOC 表一致，避免重复定义

**Commit**: 769ee89

### 2026-09-18 · 删除中文译版 PDF（已被双语 md 替代）

- 删除 `marketing/gosim_survey_agent_hackathon_intro_cn.pdf`（10.8 MB）：其内容已由双语版 `gosim_survey_agent_hackathon_intro.md` 完整覆盖
- `marketing/gosim_survey_agent_hackathon_intro.md` 文首引用块：移除该 PDF 的链接，改为说明「已替代」+ 删除日期
- `CLAUDE.md` 历史 changelog（line 215）中提及该 PDF 的条目**保留不动**：按 §6.3 「已有记录按倒序排列，不要删除历史记录（除非确认是错误条目）」，该条目是当时确实添加过的事实记录
- 全仓检索 `intro_cn` 仅命中：live 引用（已改）+ CLAUDE.md 历史记录（保留）。其余 `intro_cn` 字样均为「video-scripts.md 中文版视频脚本」无关引用

**Commit**: 6645abe

### 2026-09-18 · GOSIM 简报正文改为中英双语格式

- `marketing/gosim_survey_agent_hackathon_intro.md` 第 64–341 行（§1–§16 主体）从英文单语改为中英双语
- 段落与句子为单元：英文在前，中文紧随其后
- 保留英文原文的项目：§7 JSON 接口示例代码块、§12 评分公式代码块（按用户要求「不适合翻译」）、§16 URL 列表
- 表格双语化（§3 名词表、§13 控制划分表）
- 图注双语化（FIG 5.1 / 8.1 / 10.1–10.4）
- 文首摘要、TOC、附录保留中文/双语固定格式
- 文首说明行更新为「§1–§16 采用中英双语格式」
- 文件总行数：355 → 496（净增 141 行）

**Commit**: 2c5408f

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