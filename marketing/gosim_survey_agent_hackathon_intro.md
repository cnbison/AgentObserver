# GOSIM Hackathon · Open Agent Observer Challenge（参赛者简报）

> 原文 PDF：[`marketing/gosim_survey_agent_hackathon_intro.pdf`](gosim_survey_agent_hackathon_intro.pdf)（A4 / 12 页 / 英文）
> 出品方：GOSIM · 副标题「A GOSIM Hackathon for Intelligent Survey Operations」
> 渲染引擎：WeasyPrint 69.0
> 本仓库整理时间：2026-09-18

> **本文 §1–§16 采用中英双语格式**（已替代原中文译版 PDF `gosim_survey_agent_hackathon_intro_cn.pdf`，该 PDF 于 2026-09-18 删除）：英文段落 / 句子在前，中文翻译紧随其后；代码块（如 §7 接口示例、§12 评分公式）和 URL 列表保持英文原文。配 8 张图与版权标注。文首中文摘要、章节对照表仍用纯中文。

---

## 中文摘要

GOSIM 在 2026 年发起 **Open Agent Observer Challenge**——让参赛者**当一晚上天文学家的主值观测员**：每 900 秒（15 分钟）做一次决定，把望远镜对准哪个天区。

**为什么这件事重要**：现代巡天望远镜（DESI、Rubin/LSST 等）每晚产生海量观测数据，决定「下一束光看哪里」本身就是科研产出的一部分。把这个决策自动化、并可解释、可审计，是 AI for Science 落地的一个重要切面。

**怎么做**：组织方提供
- 固定的 **Survey Mission Card**（科学目标 + 巡天区域 + 时间预算 + 站点 + 项目集）；
- 公开的 **tile 目录、天气回放、开发场景、可视化报告**；
- 共享的 **评测仿真器 + 评分公式**。

参赛者只需提交**一个 agent 项目**——接收当前 snapshot，返回 `observe(tile_id, program, reason)` 或 `wait`。**评测时所有参赛者跑同一份天气回放 + 同一份计分规则**，最终按分数排名。

**核心挑战**（详见 §2–§9）：
1. 天气变化（seeing / transparency / 天空亮度）；
2. 目标可见性随时间变化（airmass / sky position）；
4. 巡天策略之间要兼顾 DARK / BRIGHT / BACKUP 三档条件；
3. 大尺度覆盖必须均匀，不能厚此薄彼；
5. 高优先级 tile vs 差一次曝光就完成的 tile vs 覆盖落后的 region——三者竞争同一批时隙；
6. 一次糟糕的战术决定会消耗真正的观测时间，改变后续排程；
7. 夜间操作既要「有效」也要「可解释」。

**与中文资料仓库的关系**：本 md 仅是 PDF 的本地化版本，订阅与复核以官方 PDF 为准。参赛者真正的策略设计请阅读 [references/survey26_brief.md](../references/survey26_brief.md)（赛题简报中文版）与 [agent-observer-starter-kit-ANALYSIS.md](../agent-observer-starter-kit-ANALYSIS.md)（入门包源码深度分析）。

---

## Table of Contents · 目录

| § | 英文标题 | 中文译名 |
|---|---|---|
| 1 | Survey telescopes and cosmology | 巡天望远镜与宇宙学 |
| 2 | Why survey operations are hard | 为什么巡天操作很难 |
| 3 | What the human leading observer does | 人类主值观测员做什么 |
| 4 | Why Agent Observers matter now | 为什么 Agent Observer 现在很重要 |
| 5 | How the challenge is run | 比赛如何运行 |
| 6 | Planning horizons: long, middle, and short term | 规划的时间尺度 |
| 7 | Participant job | 参赛者任务 |
| 8 | The four important aspects behind every decision | 每个决策背后的四个要素 |
| 9 | Weather-aware replanning is the core stress test | 天气感知重规划——核心压力测试 |
| 10 | Result visualization | 结果可视化 |
| 11 | Participant workflow | 参赛者工作流 |
| 12 | How scoring works | 评分如何计算 |
| 13 | Scored scope | 评分范围 |
| 14 | Open science design | 开放科学设计 |
| 15 | Why this matters | 为什么这件事重要 |
| 16 | Public science references | 公开科学参考文献 |

---

## Cover · 封面

> **GOSIM HACKATHON · PARTICIPANT BRIEFING**
>
> **GOSIM 黑客松 · 参赛者简报**

> # Open Agent Observer Challenge
> # 开放智能体观测员挑战赛

> ### A GOSIM Hackathon for Intelligent Survey Operations
> ### GOSIM 黑客松：面向智能巡天操作

> Build a future agent observer for survey nights: read the sky state, reason like a leading observer, and choose the next observation **every 900 seconds**.
>
> 为未来的巡天夜晚构建一个智能体观测员：读懂天空状态，像资深主值观测员一样推理，**每隔 900 秒**做出下一个观测决定。

---

## 1. Survey telescopes and cosmology · 巡天望远镜与宇宙学

A survey telescope maps large areas of the sky in a systematic way. Instead of spending the whole night on a single object, a survey observes thousands of sky fields over many nights and builds statistically powerful samples of galaxies, quasars, stars, and other sources.

巡天望远镜以系统化方式扫描大面积天区。它不会把整个夜晚都花在一个目标上，而是在许多夜晚里观测数千个天区，构建对星系、类星体、恒星与其他天体具有统计意义的大样本。

Cosmology depends on these large, uniform, well-calibrated samples. Wide-field surveys reveal the large-scale structure of the Universe, constrain the expansion history, support dark-energy measurements, and connect galaxy evolution to cosmic time. **The observing plan shapes the final science sample.**

宇宙学依赖于这些**大面积、均匀、良好校准**的样本。广域巡天揭示宇宙的大尺度结构、约束膨胀历史、支持暗能量测量，并把星系演化与宇宙时间联系起来。**观测计划决定最终的科学样本。**

![FIG 1.1 — A visual reminder that wide-field surveys are ultimately sampling the cosmic web: galaxies trace large-scale structure shaped by dark matter.](../assets/agent-observer/pdf-fig-1-1-cosmic-web.jpg)

> **FIG 1.1** — Wide-field surveys are ultimately sampling the cosmic web: galaxies trace large-scale structure shaped by dark matter.
> **图 1.1** —— 广域巡天本质上是在采样宇宙网：星系勾勒出由暗物质塑造的大尺度结构。
> Source: <https://science.nasa.gov/asset/hubble/probing-the-cosmic-web>
> Credit: **NASA Science / Hubble, Probing the Cosmic Web**. NASA media and page attribution retained.
> 版权：NASA 科学 / Hubble「Probing the Cosmic Web」项目；NASA 媒体与页面署名保留。

A spectroscopic survey adds a third dimension: redshift. With sky position plus redshift, a survey can build a three-dimensional map of cosmic structure. **DESI** is a concrete public example of this goal: it measures spectra for large samples of galaxies and quasars to map the expanding Universe and study dark energy.

光谱巡天加入了第三维——**红移**。结合天区位置与红移，巡天能构建出宇宙结构的三维地图。**DESI**（暗能量光谱仪）正是这一目标的一个公开范例：它对大量星系和类星体进行光谱测量，绘制膨胀中的宇宙并研究暗能量。

---

## 2. Why survey operations are hard · 为什么巡天操作很难

![FIG 1.2 — DESI's public science motivation: spectra of galaxies and quasars build a three-dimensional map of cosmic structure and expansion history.](../assets/agent-observer/pdf-fig-1-2-desi-redshift.jpg)

> **FIG 1.2** — DESI's public science motivation: spectra of galaxies and quasars build a three-dimensional map of cosmic structure and expansion history.
> **图 1.2** —— DESI 的公开科学动机：星系与类星体的光谱共同构建出宇宙结构与膨胀史的三维地图。
> Source: <https://desi.lbl.gov/2024/04/04/first-cosmology-results-from-desi>
> Credit: **Claire Lamman / DESI collaboration**; custom colormap package by cmastro. Used with source and credit for educational hackathon materials.
> 版权：Claire Lamman / DESI 合作组；cmastro 自定义配色包；用于本教育性黑客松素材。

- **Weather changes** the value of a 900-second exposure through seeing, transparency, and sky brightness.
  **天气**通过视宁度（seeing）、大气透明度（transparency）和天空背景亮度（sky brightness）改变每个 900 秒曝光的价值。
- **Target visibility** changes with time through airmass and sky position.
  **目标可见性**随时间变化，受气团（airmass）和天区位置影响。
- **Different programs** prefer different sky conditions, such as DARK, BRIGHT, and BACKUP modes.
  **不同观测项目**偏好不同的天空条件：DARK（暗夜）、BRIGHT（亮夜）和 BACKUP（备用）三种模式。
- **The footprint** must be completed broadly and evenly to support reliable science analyses.
  **巡天区域（footprint）**必须被广泛且均匀地覆盖，才能支撑可靠的后续科学分析。
- **Every observing slot** forces a trade-off among high-priority tiles, nearly complete tiles, and under-covered footprint regions.
  **每个观测时隙（slot）**都迫使你在「高优先级天区」「差一次曝光就完成的 tile」「覆盖落后的区域」之间做出取舍。
- **A single poor tactical choice** spends real observing time and changes the future plan.
  **一次糟糕的战术选择**会消耗真实的观测时间，并改变后续排程。
- **Night operations** require decisions that are both effective and explainable.
  **夜间操作**要求决策既「有效」又「可解释」。

---

## 3. What the human leading observer does · 人类主值观测员做什么

> 📘 **Note for non-astronomers.** Every term in this section answers one practical question: *how visible and valuable is a given target right now?*
>
> 📘 **给非天文学专业读者的提示。** 本节的每个术语都回答同一个实际问题：**此刻某个目标的可见性与科学价值有多大？**

> | 术语 | English / 英文 | 中文释义 |
> |---|---|---|
> | **Seeing / 视宁度** | how much atmospheric turbulence blurs the image; lower is better. | 大气湍流把图像模糊的程度；越低越好。 |
> | **Transparency / 大气透明度** | how clear the atmosphere is along the line of sight; higher is better. | 视线方向大气的清澈程度；越高越好。 |
> | **Sky brightness / 天空背景亮度** | the background glow of the night sky (moonlight, twilight, light pollution); darker is better for faint targets. | 夜天的背景辉光（月光、昏影、光污染）；对暗弱目标而言越暗越好。 |
> | **Airmass / 气团** | how much atmosphere a target's light must pass through, defined as 1 at the zenith (directly overhead); it grows as the target sinks toward the horizon, so lower is better, and it changes through the night as targets rise and set. | 目标的光必须穿过的大气量；天顶处定义为 1，越靠近地平线越大，因此越小越好；它会随着目标升落在一夜中持续变化。 |
> | **DARK / BRIGHT / BACKUP** | observing programs matched to sky conditions: DARK spends the best dark time on faint targets; BRIGHT tolerates background glow, focusing on bright targets but not faint ones; BACKUP keeps the telescope useful in poor conditions. | 与天空条件匹配的观测项目：DARK 把最好的暗夜时段用于暗弱目标；BRIGHT 容许一定的背景辉光，专注于亮目标而非暗目标；BACKUP 让望远镜在条件差时仍保持生产力。 |
> | **Tile** | one patch of sky the telescope observes in a single pointing; the survey divides the footprint into tiles, and every observing decision picks one tile at a time. | 望远镜一次指向所观测的一块天区；巡天把整个 footprint 切成 tile，每次观测决定只在其中选一个。 |
> | **Footprint** | the full sky area the survey must cover, completed broadly and evenly. | 巡天必须覆盖的完整天区，要求广泛且均匀地完成。 |
> | **High-priority / nearly complete / under-covered tiles** | respectively, tiles with extra scientific weight, tiles one exposure away from done, and regions lagging behind in the footprint; all three compete for the same observing slots. | 分别指：科学权重更高的 tile、还差一次曝光就完成的 tile、以及 footprint 中明显落后的区域；这三类 tile 同时争夺同一批观测时隙。 |

Together these terms define **target visibility in the broad sense**: the atmosphere sets image quality (seeing, transparency, sky brightness), geometry sets whether a target is up at all (airmass, sky position), the program mode decides which targets fit the current conditions, and the survey state decides which tiles matter most (priority, completion, footprint balance). **A good observer reads all of these before spending the next 900-second slot.**

这些术语合在一起定义了**广义上的「目标可见性」**：大气决定成像质量（视宁度、透明度、背景亮度），几何决定目标此刻是否在地平线之上（气团、天区位置），观测项目模式决定哪些目标适配当前条件，而巡天状态决定哪些 tile 此刻最重要（优先级、完成度、覆盖均衡）。**优秀的观测员会在花掉下一个 900 秒时隙之前，把这一切全部读懂。**

On a real survey night, the leading observer answers the challenges above through a repeating set of duties:

在真实的巡天之夜里，主值观测员通过一组反复执行的任务来应对上述挑战：

1. **Night strategy:** interpret the science goal and decide the tactical emphasis for the night.
   **夜间策略：** 解读科学目标，决定当晚的战术重点。
2. **Weather interpretation:** read seeing, transparency, sky brightness, and short-term forecast.
   **天气判读：** 阅读视宁度、透明度、背景亮度，以及短期天气预报。
3. **Program selection:** decide when the night favors DARK, BRIGHT, or BACKUP observations.
   **项目选择：** 决定当晚适合走 DARK、BRIGHT 还是 BACKUP。
4. **Candidate filtering:** pick out the currently visible, legal, and useful sky tiles.
   **候选筛选：** 挑出当前可见、合规、有科学价值的 tile。
5. **Tile ranking:** trade science yield, priority, airmass, footprint balance, and time waste.
   **Tile 排序：** 在科学产出、优先级、气团、覆盖均衡、时间浪费之间做权衡。
6. **Completion management:** finish tiles when completion value beats overshoot cost.
   **完成度管理：** 当「完成一块 tile」的收益高于「过度曝光」的代价时，就收尾它。
7. **Replanning:** react to disruption blocks and shifting observing efficiency.
   **重排程：** 对突发干扰与观测效率波动做出反应。
8. **Quality monitoring:** use fast validation signals to calibrate future decisions.
   **质量监控：** 利用快速验证信号校准后续决策。
9. **Reason logging:** explain why the observer chose this action in this slot.
   **理由留痕：** 解释为什么观测员在这个时隙选择了这个动作。

---

## 4. Why Agent Observers matter now · 为什么 Agent Observer 现在很重要

The duties above are demanding even for experienced observers: they require judgment under uncertainty, **every 900 seconds, all night long**. Modern AI systems now create a path toward assistants that read the state, call computational tools, reason with physical constraints, propose plans, monitor quality, and explain each choice.

这些任务对资深观测员来说也并不轻松：它们要求在不确定性下做出判断，**每 900 秒、整夜如此**。现代 AI 系统正在开辟一条新路——打造能读懂状态、调用计算工具、基于物理约束推理、提出方案、监控质量、并解释每一次选择的助手。

The goal is **an agent observer that can participate in real survey operations**: reading the same state as a human leading observer, proposing the next move, and explaining why.

目标是打造**一个能参与真实巡天操作的智能体观测员**：它读取与人类主值观测员相同的状态，提出下一步动作，并解释为什么。

This hackathon offers a focused benchmark: participants design the observer logic system, while the organizers provide the mission definition, sky tiles, observing constraints, weather scenarios, simulator, and evaluation protocol.

这场黑客松提供了一个聚焦的基准测试：参赛者负责设计观测员的逻辑系统，组织方则提供任务定义、天空 tile、观测约束、天气场景、仿真器与评测协议。

---

## 5. How the challenge is run · 比赛如何运行

This document describes the challenge design and the reasoning concept behind it. Each challenge instance starts from a **Survey Mission Card**. The card describes the science goal, footprint size, time budget, telescope site, available programs, target classes, observing constraints, and scoring rule. The Survey Mission Card and the public development data will be released to participants before the hackathon begins.

本文档介绍赛题设计及其背后的推理思路。每个挑战实例都从一张**Survey Mission Card（巡天任务卡）**开始。任务卡描述科学目标、覆盖面积、时间预算、望远镜站点、可用的观测项目、目标类别、观测约束和评分规则。任务卡和公开的开发数据将在黑客松开始前发放给参赛者。

- **Mission definition:** what sky area to cover, which targets matter, and how much time is available.
  **任务定义：** 要覆盖哪些天区、哪些目标重要、可用时间是多少。
- **Telescope / site:** latitude, visibility limits, slot length, and airmass constraint.
  **望远镜 / 站点：** 纬度、可见性限制、时隙长度、气团约束。
- **Public development data:** tile catalog, example weather scenarios, initial states, and visual reports.
  **公开开发数据：** tile 目录、示例天气场景、初始状态、可视化报告。
- **Final evaluation data:** organizer-provided weather replays run through the same simulator.
  **最终评测数据：** 由组织方提供、跑在同一仿真器上的天气回放。
- **Participant product:** an agent observer that reads state and returns an observing action.
  **参赛者产出物：** 一个读取状态、返回观测动作的智能体观测员。

### Same exam for every participant

Evaluation fixes one shared scenario — the overall survey plan, the per-night seeing and weather replay, ad-hoc observing requests, and predictable mid-term disruptions such as rain, forest fire smoke plumes or scheduled rocket launches — together with a single scoring rule. Working from this information, the agent produces the next observing plan every 900 seconds.

评测时使用**同一份共享场景**——整体巡天计划、每夜的视宁度与天气回放、临时插入的观测请求、以及可预见的中期干扰（如降雨、森林火灾烟雾羽流或例行的火箭发射）——以及**同一套评分规则**。基于这些信息，智能体每 900 秒产出一份下一步的观测计划。

> **FIG 5.1** — The data flow: fixed inputs feed the agent state, the reasoning agent returns an action, the simulator updates fast metrics, the run yields final metrics and a complete audit log.
>
> **图 5.1** —— 数据流：固定输入喂养智能体状态，推理智能体返回动作，仿真器更新快速指标，一轮运行产出最终指标与完整审计日志。

![FIG 5.1 — The data flow: fixed inputs feed the agent state, the reasoning agent returns an action, the simulator updates fast metrics, the run yields final metrics and a complete audit log.](../assets/agent-observer/fig5.1.png)

---

## 6. Planning horizons: long, middle, and short term · 规划的时间尺度

Real survey operations plan on three timescales, and this challenge maps onto them deliberately:

真实的巡天操作会在三个时间尺度上做规划，而本挑战也刻意与之对应：

### Long term (whole survey)
### 长期（整个巡天）

The organizers provide the overall survey plan — which sky areas and which targets to observe — as part of the mission card, while the agent manages that plan in flight. Final scoring includes survey completeness and completion quality.

组织方在任务卡中给出整体巡天计划——要观测哪些天区与目标——智能体负责在运行中**管理**这份计划。最终评分包括巡天完成度与完成质量。

### Middle term (month, week, day)
### 中期（月、周、日）

A flexible plan built from completion progress and forecast conditions, absorbing predictable disruptions (weather systems, forest fire smoke plumes, scheduled launches) and newly inserted observing requests. **This layer belongs to the evaluation scope; the agent should manage the plan and observation window.**

基于完成进度和预报条件构建的弹性计划，吸收可预见的干扰（天气系统、森林火灾烟雾羽流、例行发射）以及临时插入的观测请求。**这一层属于评测范围；智能体应负责管理计划与观测窗口。**

### Short term (tonight, every 900-second slot)
### 短期（今夜、每个 900 秒时隙）

Immediate tactical adjustments based on the middle-term plan, driven by real-time measured seeing and transparency. **This layer is the focus of the scored benchmark.**

基于中期计划、依据实时测得的视宁度与透明度做出的即时战术调整。**这一层是计分基准测试的核心。**

> 💡 From Section 7 to 10, the document presents a reference implementation to illustrate a sample design. These examples are intended to guide your thinking, **not to constrain your creativity**. Please remember that the authoritative input/output formats and the interface contract are strictly defined by the Survey Mission Card.
>
> 💡 从第 7 节到第 10 节，文档给出一个**参考实现**用于展示样例设计。这些示例旨在启发思路，**绝不限制你的创造力**。请记住：权威的输入/输出格式与接口契约，严格由 Survey Mission Card 定义。

---

## 7. Participant job · 参赛者任务

The participant job is to submit **a concrete, reproducibly runnable agent project**. The programming language is not restricted, as long as the project implements the observer interface: the simulator repeatedly hands your agent the current situation, and the agent returns next action (like "observe" or "wait").

参赛者的任务是提交**一个具体、可复现运行的智能体项目**。编程语言不限，只要项目实现了观测员接口：仿真器把当前局面反复交给你的智能体，智能体返回下一步动作（例如 "observe" 或 "wait"）。

Every 900-second slot, the agent should return one observing plan in a format like:

每 900 秒时隙，智能体应按以下格式返回一份观测计划：

```python
return {"action": "observe", "tile_id": 100123, "plan": "DARK",
        "reason": "good weather and highest useful gain"}
```

which gives the basic command for the next move. The **reason field** is in free form, its content is not restricted.

这条返回值给出了下一步动作的基本指令。**reason 字段**为自由文本，不限定内容。

In the hackathon, we demand **a full trace logging**: the project must save the complete record of every agent turn into files, including but not limited to each turn's input, output, tool calls, and tool results for organizer review.

黑客松要求**完整的轨迹记录**：项目必须把每一次智能体轮次的完整记录保存到文件中，至少包括每轮的输入、输出、工具调用与工具结果，供组织方复盘。

**Submit:** the agent project + a short note explaining the observer architecture.

**提交物：** 智能体项目 + 一份简要说明观测员架构的笔记。

---

## 8. The four important aspects behind every decision · 每个决策背后的四个要素

Every slot, the agent should be provided with information about **four aspects** — weather, forecast, progress, and available tiles. The agent weighs all four together rather than reacting to any one of them alone. The diagram below shows how these inputs are structured.

每个时隙，智能体应能获取**四个维度**的信息——天气、预报、进度、可选 tile。智能体需要把四者联合权衡，而不是孤立地对单一维度做出反应。下图展示了这些输入的结构。

> **FIG 8.1** — The content dictionary is small enough for non-astronomers to inspect and reason about. The **donefrac** here refers to survey completion of each single tile: 0 means just started, 1 means complete.
>
> **图 8.1** —— 内容字典足够简洁，让非天文专业读者也能检视与推理。这里的 **donefrac** 指的是每个 tile 的巡天完成度：0 表示刚刚开始，1 表示已完成。

![FIG 8.1 — The content dictionary is small enough for non-astronomers to inspect and reason about. The donefrac here refers to survey completion of each single tile: 0 means just started, 1 means complete.](../assets/agent-observer/fig8.1.png)

The agent should handle several recurring situations:

智能体应能处理若干反复出现的情形：

- In **excellent dark conditions**, it should use the slot for high-value faint targets.
  在**极佳的暗夜条件**下，应把时隙用于高价值的暗弱目标。
- In **marginal conditions**, it may finish nearly complete tiles or switch to more suitable programs.
  在**边缘条件**下，可收尾快完成的 tile，或切换到更合适的观测项目。
- When **the forecast improves soon**, it can preserve the best dark-time targets.
  当**预报显示天气即将转好**时，可以把最好的暗夜目标留给后面。
- When **one footprint region lags behind**, it can accept a slightly lower immediate yield to keep the survey balanced.
  当**某块 footprint 区域明显落后**时，可接受略低的即时产出以保持巡天均衡。

> **How to weigh these factors is left to each participant's design.**
>
> **如何权衡这些因素，由参赛者自行设计。**

---

## 9. Weather-aware replanning is the core stress test · 天气感知重规划——核心压力测试

The weather replay includes deterministic disruption blocks (rain, forest fire, rocket launch, etc.). During poor conditions, **a naive agent may waste time, wait too much, or spend good targets in bad sky**. A stronger agent can:

天气回放里包含若干确定性的干扰块（降雨、森林火灾、火箭发射等）。在恶劣条件下，**天真的智能体可能浪费时间、过度等待，或把好目标浪费在糟糕的天空下**。更聪明的智能体能够：

- use the forecast,
  **使用预报**，
- switch programs when appropriate,
  在合适时**切换项目**，
- finish near-complete tiles, and
  **收尾即将完成的 tile**，并且
- preserve valuable dark-time targets for better conditions.
  把宝贵的暗夜目标**留给更好的条件**。

---

## 10. Result visualization · 结果可视化

The test data also contain a deterministic mock target-coordinate catalog. Each tile's target counts are bound to fixed mock coordinates by seed, tile_id, and target class. After an agent run, the simulator converts completed tile fractions into an observed-target map.

测试数据还包含一份确定性的 mock 目标坐标目录。每个 tile 的目标数量由 seed、tile_id 与目标类别绑定到固定坐标上。一次智能体运行结束后，仿真器把已完成的 tile 比例转换为一张「已观测目标地图」。

The map can show how many mock galaxies and quasars the agent observed. The plotted coordinates show RA, Dec, and mock redshift for result visualization.

该地图可以显示智能体观测到了多少 mock 星系与类星体。绘制的坐标展示 RA、Dec 与 mock 红移，用于结果可视化。

- **Three-dimensional plots** show the observed mock universe as a spatial sample.
  **三维图**把观测到的 mock 宇宙作为空间样本展示。
- **Two-dimensional butterfly plots** show sky position folded with mock redshift, DESI-style.
  **二维蝴蝶图**把天区位置按 mock 红移折叠展示，DESI 风格。
- **Review overlays** place the fixed target catalog in a tunable alpha background and the participant's observed sample in color.
  **复盘叠图**把固定的目标目录作为可调透明度的背景层，将参赛者的观测样本用彩色高亮。
- **Alpha sweep figures** compare multiple target-layer transparencies side by side for judging and presentation.
  **Alpha 扫描图**把多个目标层透明度并排展示，便于评审与汇报。

Different observer policies produce different visible cosmic-structure maps. The visualization helps teams explain strategy, footprint balance, and missed regions. The map is a benchmark visualization layer; the scored loop remains the planning task.

不同的观测策略会产生不同的可见宇宙结构图。可视化帮助队伍解释策略、覆盖均衡与遗漏区域。该地图是一层基准可视化；计分回路仍然是规划任务本身。

The reference implementation includes utilities that regenerate these figures for any agent run.

参考实现里包含一些工具函数，能为任意一次智能体运行重新生成这些图。

![FIG 10.1 — Example challenge output from the built-in balanced observer. The three-dimensional view keeps the spatial mock-universe sample visible for presentation.](../assets/agent-observer/pdf-fig-10-1-3d-universe.jpg)

> **FIG 10.1** — Example challenge output from the built-in balanced observer. The three-dimensional view keeps the spatial mock-universe sample visible for presentation.
> **图 10.1** —— 内置 balanced observer 的样例挑战输出。三维视图保留空间 mock 宇宙样本，便于演示。

![FIG 10.2 — Example review overlay. Gray points show the fixed target catalog with target alpha 0.11; colored points show the participant observed sample with observed alpha 0.38.](../assets/agent-observer/pdf-fig-10-2-review-overlay.jpg)

> **FIG 10.2** — Example review overlay. Gray points show the fixed target catalog with target alpha 0.11; colored points show the participant observed sample with observed alpha 0.38.
> **图 10.2** —— 复盘叠图示例。灰色点为固定目标目录（目标 alpha = 0.11），彩色点为参赛者的观测样本（观测 alpha = 0.38）。

![FIG 10.3 — Example alpha sweep. The three panels compare target alpha values 0.035, 0.11, and 0.22 while keeping the observed layer fixed.](../assets/agent-observer/pdf-fig-10-3-alpha-sweep.jpg)

> **FIG 10.3** — Example alpha sweep. The three panels compare target alpha values 0.035, 0.11, and 0.22 while keeping the observed layer fixed.
> **图 10.3** —— Alpha 扫描示例。三幅面板分别使用目标 alpha = 0.035、0.11、0.22，观测层保持不变。

![FIG 10.4 — A DESI Data example of how sky coordinates and redshift become a map-like view; the challenge's observed-universe map is a lightweight benchmark analogue.](../assets/agent-observer/pdf-fig-10-4-desi-butterfly.jpg)

> **FIG 10.4** — A DESI Data example of how sky coordinates and redshift become a map-like view; the challenge's observed-universe map is a lightweight benchmark analogue.
> **图 10.4** —— DESI 数据示例，展示天区坐标与红移如何变成一张地图视图；挑战里的「观测宇宙图」是其轻量级基准类比物。
> Source: <https://data.desi.lbl.gov/doc>
> Credit: **David Kirkby / DESI collaboration**. DESI data are licensed under **CC BY 4.0**.
> 版权：David Kirkby / DESI 合作组；DESI 数据采用 **CC BY 4.0** 授权。

---

## 11. Participant workflow · 参赛者工作流

1. **Read** the Survey Mission Card.
   **阅读** Survey Mission Card。
2. **Study** the public development scenarios and their visual reports.
   **研究** 公开的开发场景与可视化报告。
3. **Prototype** an agent against the observer interface described above.
   **原型** 一个能对上文观测员接口的智能体。
4. **Evaluate** it on the development scenarios, and inspect the trace logs and observed-universe maps to understand its behavior.
   在开发场景上**评估**它，并检查轨迹日志与观测宇宙地图，理解其行为。
5. **Submit** the agent project, the observer architecture note, and the full trace logs of every agent turn.
   **提交** 智能体项目、观测员架构笔记，以及每一轮的完整轨迹日志。

> The reference implementation ships a starter template and concrete commands for each step; see the participant guide in the repository.
>
> 参考实现提供了入门模板与每一步的具体命令；详见仓库中的参赛者指南。

---

## 12. How scoring works · 评分如何计算

The score is computed by the organizers after the run. It rewards weighted effective targets and penalizes uneven footprint coverage, wasted time, rule violations, and incomplete high-priority tiles.

分数由组织方在比赛结束后计算。它奖励加权后的有效目标，并对覆盖不均、时间浪费、违规、以及高优先级 tile 未完成进行惩罚。

```
score = science_score
      − uniformity_penalty
      − wasted_time_penalty
      − violation_penalty
      − incomplete_priority_penalty
```

Your agent may use any internal decision logic; shaping that logic to anticipate the scoring terms is one natural strategy, since a good agent ends up trading immediate yield against completion, uniformity, weather risk, and operational discipline.

你的智能体可以使用任何内部决策逻辑；让该逻辑去「预测」评分项是一种自然策略——优秀的智能体最终会在「即时产出」与「完成度、覆盖均匀、天气风险、操作纪律」之间进行权衡。

---

## 13. Scored scope · 评分范围

- **Primary evaluation:** short-term observation planning, scored as described in §12.
  **主要评测：** 短期观测规划，按 §12 计分。
- **Middle-term planning:** part of the intended evaluation scope, enabled at organizer discretion as the mission cards evolve.
  **中期规划：** 属于设计中的评测范围，由组织方按任务卡演进酌情启用。
- **Validation extensions:** real DESI log replay, z > 5 QSO planning, and LBG planning as separate mission cards.
  **验证扩展：** 真实 DESI 日志回放、z > 5 类星体规划、LBG 规划作为独立任务卡。

**Control split:**

**权限划分：**

| 参赛者可控 / Participant Control | 组织方可控 / Organizer Control |
|---|---|
| agent policy, reasoning logic | simulator, data, weather replay, constraints, score |
| 智能体策略、推理逻辑 | 仿真器、数据、天气回放、约束、评分 |

---

## 14. Open science design · 开放科学设计

This challenge is built so that its results can be trusted, checked, and extended by the community:

本挑战的构建原则是：其结果必须能被社区**信任、核查、扩展**：

- **Reproducible:** fixed seeds, fixed data, fixed score — any submission can be rerun and verified by a third party.
  **可复现：** 固定的 seed、固定的数据、固定的评分——任何提交都能被第三方重跑与验证。
- **Inspectable:** the state dictionary, run histories, and the full per-turn trace logs are all readable, so every decision can be audited after the fact.
  **可检视：** 状态字典、运行历史、每一轮的完整轨迹日志都是可读的，事后的每一个决策都能被审计。
- **Hard to overfit:** development weather and final evaluation weather are separated, so the score compares generalization rather than tuning to a known scenario.
  **难以过拟合：** 开发期天气与最终评测天气分离，分数衡量的是泛化能力，而不是「针对已知场景调参」。
- **Extensible:** the same observer-agent interface carries future mission cards — real survey-log replay, z > 5 QSO planning, LBG planning, or target-of-opportunity inserts — and the community is invited to propose new fixed datasets as follow-up tracks.
  **可扩展：** 同一套观测员-智能体接口可承载未来的任务卡——真实巡天日志回放、z > 5 类星体规划、LBG 规划、或机遇目标插入；欢迎社区提议新的固定数据集作为后续赛道。

---

## 15. Why this matters · 为什么这件事重要

Intelligent telescope systems need more than model accuracy. They need to reason under changing conditions, explain decisions, respect constraints, and remain useful to scientists. This hackathon gives the community a concrete place to build and compare those capabilities.

智能望远镜系统需要的不仅仅是模型精度。它们需要在变化条件下推理、解释决策、尊重约束，并保持对科学家的可用性。这场黑客松为社区提供了一个具体场所，去构建并比较这些能力。

> **The goal is to make intelligent observing decisions testable, open, and scientifically grounded.**
>
> **目标是让智能观测决策变得可测试、开放、科学严谨。**

---

## 16. Public science references · 公开科学参考文献

- DESI official site — <https://www.desi.lbl.gov/>
- DESI science overview — <https://www.desi.lbl.gov/science/>
- NASA Science image page, Probing the Cosmic Web — <https://science.nasa.gov/asset/hubble/probing-the-cosmic-web/>
- DESI first cosmology results image page — <https://www.desi.lbl.gov/2024/04/04/first-cosmology-results-from-desi-most-precise-measurement-of-the-expanding-universe/>
- DESI Data documentation and license — <https://data.desi.lbl.gov/doc/>

---

## 附录 · 版权与图片归属

| 图 | 出处 | 授权 |
|---|---|---|
| FIG 1.1 Cosmic Web | <https://science.nasa.gov/asset/hubble/probing-the-cosmic-web/> | NASA / Hubble（公共领域） |
| FIG 1.2 DESI 红移图 | <https://desi.lbl.gov/2024/04/04/first-cosmology-results-from-desi> | Claire Lamman / DESI collaboration；cmastro colormap；教育用 |
| FIG 5.1 数据流图 | GOSIM Agent Observer 官方 PDF（`assets/agent-observer/fig5.1.png`，用户提供） | GOSIM Agent Observer 团队 |
| FIG 8.1 内容字典 | GOSIM Agent Observer 官方 PDF（`assets/agent-observer/fig8.1.png`，用户提供） | GOSIM Agent Observer 团队 |
| FIG 10.1 3D 宇宙图 | GOSIM Agent Observer 参考实现 balanced observer | GOSIM Agent Observer 团队 |
| FIG 10.2 Review overlay | 同上 | 同上 |
| FIG 10.3 Alpha sweep | 同上 | 同上 |
| FIG 10.4 DESI 蝴蝶图 | <https://data.desi.lbl.gov/doc/> | DESI collaboration / David Kirkby · **CC BY 4.0** |

> 本 md 仅供中文资料仓库内部使用；PDF 原文版权归 GOSIM 与各图片原始权利人所有。