# CHANGELOG · AgentObserver 仓库变更记录

> 本文件按**倒序**记录仓库所有有意义的变更（最新在上）。
>
> **历史来源**：2026-09-17 至 2026-09-18 早段共 14 条记录从 `CLAUDE.md §7` 迁移而来；此后所有任务变更均按 [CLAUDE.md §6](./CLAUDE.md) 规则追加到本文件，不再写回 `CLAUDE.md`。

---

### 2026-09-19 · 新增 GOSIM Agent Observer 50s 宣传片工程（videos/）

- 用 `guizang-product-video-skill` 把 `articles/agent-observer-promo-03-修正.md` 做成 50 秒宣传片，落到 `videos/agent-observer-promo/`
  - **风格**：default（暖白/炭黑，用户 2026-09-19 确认），1920×1080 / 30 fps / 中文
  - **结构**：9 镜头（intro 封面 + 7 个信息镜头 + CTA），每镜 4–7 秒，总时长 50.000s
  - **视觉**：9 个 React 组件（HeroIntro / CoreLoop / DecisionBadge / PrizeBoard / AudienceList / Requirements / Schedule / StartSteps / CTA），全部接入 plan.json 的 `shot.component` 路由
  - **声音**：代码原创 BGM（120 BPM / 50s，Python `assets/music-src/make-music.py` 生成）+ 4 类动作音效（whoosh / click / pop / ding-dong），混音脚本输出 24-bit master.wav 并做 music ducking
  - **关键约束**：所有数字、日期、奖金、CTA 链接来自 articles/agent-observer-promo-03-修正.md 对应行号（plan.json 的 `source` 字段），与 CLAUDE.md §3.4「不要臆造数据」一致
  - **验收**：`scripts/check_delivery.py` 跑通，`errors: []`、`ok: true`，仅 3 项可接受 review warning（shot5 阅读速度 + 标准听感）
  - **交付**：`renders/final.mp4`（H.264+AAC / 1920×1080 / 50.000s / 2.4MB）
- 工程根加 `.gitignore`：`node_modules/`（37M）+ `dist/`（79M）+ `assets/music-src/build/` + `assets/music-ducked.wav` + `assets/sfx-stem.wav`——均为可重新生成的构建/混音中间产物
- **保留入库**：源码（src/ + plan.json + BRIEF.md + scripts/）、最终音频（assets/master.wav / music.wav / sfx/）、3 张实景图（public/images/）、最终 MP4 + 关键静帧（renders/ + renders/evidence/）、文档（LICENSE / NOTICE.md / evidence/）
- 总入库体积 28.9MB（不含 .gitignore 屏蔽项）
- **不在视频里的素材**：assets/agent-observer/ 下还有 5 张其他图与 1 段主视觉视频（survey-night-sky.mp4），本片按 BRIEF 选用 3 张图；其余资产保留原位不动（CLAUDE.md §3.4「不要修改 assets/agent-observer/ 中的文件名」）

**Commit**: e7e303a

### 2026-09-19 · 新增 Guide/OperatingGuide.md（md 转公众号速查）

- 新增 `Guide/OperatingGuide.md`（334 字节）
  - 用户手写的内部速查卡：「md 文件 → 公众号格式」的两条路径
  - 路径 A：`gzh-design` skill（主题库 + 排版 + 校验）
  - 路径 B：`tools/md2wechat` CLI（`python3 -m md2wechat -i ... -o ... -t marketing`）
  - 给出的命令示例直接以 `articles/agent-observer-promo-03-修正.md` 为输入，便于团队成员复用
- 单独建 `Guide/` 目录而非塞进 `marketing/`，因为这是工作流速查而非营销内容

**Commit**: e7e303a

### 2026-09-19 · 新增 promo-03-修正.md 公众号排版 HTML

- 用 `gzh-design` 技能（红白色系主题）把 `articles/agent-observer-promo-03-修正.md` 排版成公众号 HTML
  - `articles/agent-observer-promo-03-修正_排版_红白色系(red-white).html`（58KB）—— 主交付，校验脚本 `validate_gzh_html.py` 通过
  - `articles/agent-observer-promo-03-修正_排版_红白色系(red-white)_预览.html`（61KB）—— `wrap_preview.py` 加的预览外壳（含「复制到公众号」按钮；按钮在 section 外，粘到公众号的仍是干净合规正文）
- 用 `tools/md2wechat` CLI（marketing 主题）补一份
  - `articles/agent-observer-promo-03-修正-m2w-2.html`（27KB）——marketing 主题变体，记录在 `Guide/OperatingGuide.md` 作为示例命令的输出
- 未提交：`articles/agent-observer-promo-03-修正-m2w.html` 与 `-m2w-1.html`（sci-tech / science-popular 主题变体，本次仅供挑选主题、未采用）+ `.pdf`（1.7MB，单文件偏大且可由 markdown 重新导出）

**Commit**: e7e303a

### 2026-09-19 · 回填两条 2026-09-19 记录的 commit 哈希

- 上一条 amend commit 后哈希从 `246b3c2` 变为 `b66a8c2`，把当日两条记录的 `**Commit**` 字段同步更正
- 为避免再次 amend 造成哈希循环，本回填单独作为一个 commit 落地

**Commit**: 4f0b945

### 2026-09-19 · 新增 promo-03 修正版推广文（降 AI 味）

- 新增 `articles/agent-observer-promo-03-修正.md`
  - 用户确认"赛事未开始无故事素材"后，基于 `articles/agent-observer-promo-02-正式.md` 做的**克制型降 AI 味修正版**——结构骨架、数据、CTA、图片、链接全部保留，只调整措辞与节奏
  - **金句引述从 8 处砍到 2 处**（仅保留开篇 L3 + 结尾 L475 两处 `>` 块引述；中间的伪金句全部内联到正文）
  - **删除"先贬低一般做法"模板**（第 04 节 ② 小节不再用"很多 AI 黑客松最终展示的是一个漂亮的 Demo"做对比性贬低）
  - **同一观点的三次复述压缩成两次**（"Agent 在变化环境里做连续决策"原本在 01 / 02 / 11 节各讲一遍，新版 01 只讲赛制、02 只讲挑战本质、11 节用紧凑并列短语表达）
  - **"真正 / 核心 / 重要"等 AI 强调词降频**（promo-02 出现 7–8 次的"真正"降到 3 次，删除"真正重要的是"等"上价值"模板）
  - **句尾不再一律短句收束**——混入"也" "可能" "比如"等弱连接词，节奏更像人话
  - **修复 L468 的多星号 bug**——`****GOSIM Shenzhen 2026 官网：**` 改成正常的 `**GOSIM Shenzhen 2026 官网：**`
  - **删除表格后的冗余文字复述**（奖金表后的 `**奖金池总计：$5,500。**` 删了，赛程表后的 `**练习赛已经开放。**` 改为自然衔接段落）
  - **第 09 节流程改回编号列表**——promo-02 用了 6 个等距小节标题像流程图，新版用 `1. **报名**：` 形式更像操作步骤
  - **emoji 从均匀分布改为有重心地分布**——头部信息栏 + 每个大节标题少量点缀，正文段内不再每段一个图标
- **保留不动的部分**：所有数字、日期、奖金金额、3 张配图、CTA 链接、12 节骨架、品牌词（GOSIM / Agent Observer / 巡天）——按赛事方与 CLAUDE.md §3.3 必须一致
- 用户决策点：明确指出"赛前无故事素材"——所以**不去补真人故事**，只做降 AI 味的措辞优化；如果赛后有真实团队参赛反馈，可再追加第 13 节"团队实战故事"
- **未做的事**：未对 promo-03-修正.md 做公众号排版 HTML（按用户当前任务范围仅输出 md 源文件）

**Commit**: b66a8c2

### 2026-09-19 · 修正 promo-02-正式.md CTA 链接（统一主入口）

- 修订 `articles/agent-observer-promo-02-正式.md` 第 12 节"立即开始"区块
  - 旧：5 条 bh3gei.github.io 子链接（报名入口 / 比赛平台 / 入门工具包 / 比赛规则 / 联系方式）
  - 新：2 条 GOSIM 官方主入口（create.gosim.org/survey26/ 主站报名入口 + shenzhen2026.gosim.org/ 大会官网）
  - 理由：CLAUDE.md §1 已明确主站为 `https://create.gosim.org/survey26/`，统一对外口径，避免分散到 bh3gei 子链接
- **Commit 上下文**：上一条 commit `71d5908` 推送后本地修改未自动 add；本次合并到下一个 commit 一起推送

**Commit**: b66a8c2

### 2026-09-19 · 调整 promo-02-正式.md 标题措辞

- 修订 `articles/agent-observer-promo-02-正式.md` 标题第 1 行
  - 旧：`GOSIM 2026 巡天智能体黑客松正式启动：让 AI 决定望远镜下一步看哪里`
  - 新：`GOSIM 2026 巡天智能体黑客松正式启动：让 AI 决定巡天望远镜下一步看哪里`
  - 变更：在「决定」与「望远镜」之间插入「巡天」二字，强化"巡天 = Agent Observer"主题关联
  - 行数无变化（486 行），正文、引用块、配图、CTA 全部不变
- **Commit 上下文**：上一条 commit `6a630ee` 推送后，本地修改未自动 add；本次 commit 补上

### 2026-09-19 · 新增 promo-02 正式版推广文 + 早期版本归档

- 新增 `articles/agent-observer-promo-02-正式.md`（14915 字节 / 3 张配图）
  - 用户最终采用的 v2 正式版本，标题：`GOSIM 2026 巡天智能体黑客松正式启动：让 AI 决定望远镜下一步看哪里`
  - 文首摘要 5 项 emoji 速览：全球开放 / 个人团队均可参加 / $5,500 奖金池 / 6 个现金奖项 / 10 月线上比赛 / 10 月深圳颁奖
  - 3 张图全部本地化、全部存在：
    - L9 `survey-agent-strategy-XnSuOIcZ.jpg`（观测智能体把天气、天区与巡天进度权衡成一份观测计划）
    - L65 `cosmos-control-room-DALcRogD.jpg`（巡天控制室——观测员面对不断变化的天空条件）
    - L482 `cosmos-observatory-hero-BV_aYwWD.jpg`（观测台主视觉——把镜头指向下一个 900 秒）
  - 无外部 CDN 引用；图片路径全部走 `../assets/agent-observer/` 相对路径
- 新增 `articles/bak/agent-observer-promo-02.md`（14915 字节）—— promo-02 早期版本归档（与正式版同字节数，标题相同，作为版本对照保留）
- 更新 `README.md`
  - 阅读路径表新增 #9：`articles/agent-observer-promo-02-正式.md`（用户最终采用版本）
  - 仓库结构图登记 `articles/bak/` 目录与 promo-02-正式.md 条目
- 校验：3 张图全部存在于 `assets/agent-observer/`，0 个外部 CDN 引用
- **未做的事**：未对 promo-02-正式.md 排版为公众号 HTML（按用户要求只更新并推送源文件，未排版）

### 2026-09-18 · 修正红白色系排版 HTML 第一张图（搞混了 promo-01 / promo）

- 修复 `articles/agent-observer-promo-01_排版_红白色系(red-white).html` 第 1 张图错误引用
  - 错：用了 `cosmos-observatory-hero-BV_aYwWD.jpg` + 图注「夜色中的观测台穹顶」（来自 `agent-observer-promo.md` 封面）
  - 对：改回 `survey-agent-strategy-XnSuOIcZ.jpg` + 图注「观测智能体把天气、天区与巡天进度权衡成一份观测计划」（promo-01.md L7 原引用）
- §03 控制室图（`cosmos-control-room-DALcRogD.jpg`）和文末收尾图（`cosmos-observatory-hero-BV_aYwWD.jpg`）原本就正确，**未改动**
- 重新跑 `validate_gzh_html.py`：ERROR=0 + WARNING=0，209 处 `<span leaf>` 包裹完整
- 重新生成预览页 `articles/agent-observer-promo-01_排版_红白色系(red-white)_预览.html`（覆盖前版）

**Commit**: 48653cf（已修正）+ 待 push 的 bug fix

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