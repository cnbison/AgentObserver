# 把夜空的下一步，交给你写的智能体

**GOSIM Agent Observer 黑客松 · 180 个观测夜 · \$5,500 奖金池 · 9 月报名 · 10 月深圳见**

> Human judgment · Machine speed · One shared sky

---

> **一句话摘要**：GOSIM 巡天智能体（Agent Observer）黑客松 2026 招募中——同一份巡天计划、同一个模拟器、同一种计分，**唯一的变量，就是你写的策略**。\$5,500 奖金池、6 个奖项、180 个观测夜、Python 3.12 沙箱，9 月起在线开战，10 月 17 日深圳颁奖。无论你是写过 LangGraph 的工程师、做过天文社的爱好者，还是刚刚跑通 `hello.py` 的初学者——**整个比赛你只需要改一个函数 `choose_action`**。

---

![图：GOSIM Agent Observer 黑客松主视觉——夜色中的观测台穹顶](../assets/agent-observer/cosmos-observatory-hero-BV_aYwWD.jpg)

## 目录

- §1 · 这场黑客松在做什么
- §2 · 为什么难：观测员不是旁观者
- §3 · GOSIM 这场有什么不同
- §4 · 怎么参加：20 分钟到排行榜
- §5 · 你能获得什么
- §6 · 现在就开始
- 附录 · 图片版权与署名

---

## §1 · 这场黑客松在做什么

过去十年，AI 已经能下围棋、能写代码、能写论文。但在天文台里，**下一个 900 秒**依然是人类观测员最难熬的 15 分钟——要在不确定的天气、滞后的预报、随时可能被打断的巡天计划之间，做出"现在观测哪个天区"的判断。

GOSIM Agent Observer 黑客松把这件事**变成了一道 AI 题目**：让你写的智能体，在 **180 个仿真观测夜**里，扮演天文台观测员，读懂天气与进度，给出下一个动作。

![图：巡天控制室——夜晚值班的主战场](../assets/agent-observer/cosmos-control-room-DALcRogD.jpg)

**几个关键数字，先放在前面：**

- **\$5,500 奖金池**：一等奖 \$2,000 / 二等奖 \$1,000 × 2 / 三等奖 \$500 × 3，共 **6 个奖项**
- **180 个观测夜**：基线智能体跑完一轮大约 15 秒，分数 **约 12,287**
- **900 秒时隙**：每一轮决策的"思考时间"，整夜如此
- **1–8 人队伍**：个人参赛也需建队

> 📅 **赛程三段**：10 月 1–4 日 线上培训 → 10 月 5–7 日 线上比赛 → 10 月 17 日 深圳 GOSIM 大会颁奖。练习赛现已开放，每队每天 50 次提交；线上比赛 10.04 16:00 UTC 起，每队每天 10 次。

---

## §2 · 为什么难：观测员不是旁观者

大多数人会把"看星星"想得很浪漫——把镜头指向天上，按下快门。但真实的巡天之夜，观测员要做 **9 件事**：

1. 制定当晚策略
2. 研判天气与云层
3. 在多个项目中选择优先级
4. 从候选天区中筛选
5. 排好天区顺序
6. 跟踪完成度
7. 一旦变天，立刻重规划
8. 持续质量监控
9. 写下每一步的理由

更关键的是，**这三件事同时发生在三个时间尺度上**——长期是整个巡天几年的产出规划，中期是月/周/日的项目分配，**短期是接下来 900 秒到底观测哪个天区**。本届黑客松同时考察这三个尺度。

![图：状态字典——智能体每 900 秒读一次的四个要素](../assets/agent-observer/fig8.1.png)

智能体每一步看到的，是一个 **4 维状态字典**：`weather` / `forecast` / `progress` / `available_tiles`，并要输出 `{observe | wait, tile_id, plan, reason}`。**比下围棋难的地方在于**：棋盘是确定的、天文台不是——降雨、森林火灾烟羽、火箭发射尾迹，都是仿真器会注入的**确定性扰动**，而**比赛天气与开发天气分离**，比的是泛化能力，不是过拟合。

![图：智能体在控制台权衡——这是 §2 想要的"现场感"](../assets/agent-observer/survey-agent-strategy-XnSuOIcZ.jpg)

---

## §3 · GOSIM 这场有什么不同

今年 10 月，GOSIM Shenzhen 2026 在深圳启幕，整套包括三场并行赛事——**智能体应用黑客松、智能体软件工厂黑客松，以及这场 Agent Observer 巡天智能体黑客松**。和兄弟赛事一样，我们守三条底线：

- ✅ **开放祛魅，零门槛赋能**：报名不查简历，提交不限资历。整场比赛只接收一个 Python 包——解压后不超过 50 MB，单文件不超过 20 MB。
- ✅ **公平竞技，实力论突破**：**同一份巡天计划、同一个模拟器、同一种计分**。唯一变量是策略。
- ✅ **真实落地，拒绝空壳 Demo**：赛题源自真实的天文观测决策流，评分公式 `score = base_science + program_bonus + request_reward − penalty_total`，并且把"开发天气与最终评测天气分离"——这是测**泛化能力**，不是比谁更会调参。

为了让你知道这件事到底有多"真"——**2024 年 DESI（暗能量光谱巡天）首批结果发布，测量了超过 5000 万个星系**，把宇宙膨胀的历史画到了最近 110 亿年。我们这场挑战的协议设计，正是借鉴 DESI 这样的真实巡天流程。

![图：DESI 5000 万星系红移地图——巡天的"成绩单"](../assets/agent-observer/pdf-fig-1-2-desi-redshift.jpg)
> *图片来源：Claire Lamman / DESI collaboration*

![图：宇宙网——巡天想看清的全景](../assets/agent-observer/pdf-fig-1-1-cosmic-web.jpg)
> *图片来源：NASA / ESA / Hubble 公共领域*

---

## §4 · 怎么参加：20 分钟到排行榜

很多人以为"参加个天文 AI 比赛"要先学天体物理、再装一整套环境、再读 200 页文档。**不是**。

整个比赛你只需要改一个函数——`choose_action`。整个流程 20 分钟跑通基线：

| 步骤 | 干什么 | 时间 |
|---|---|---|
| 1 | 注册账号 | 2 分钟 |
| 2 | 创建队伍（1–8 人） | 1 分钟 |
| 3 | 下载 `agent-observer-starter-kit` | 3 分钟 |
| 4 | 改 `choose_action` 函数 | 10 分钟 |
| 5 | 上传 `decisions.csv` 或程序包 | 2 分钟 |
| 6 | 看分数与回放 | 2 分钟 |

![图：Alpha 扫描——三种策略的视觉对比](../assets/agent-observer/pdf-fig-10-3-alpha-sweep.jpg)

练习赛阶段你可以走两条路：

- **轻装上阵**：把策略直接输出成 `decisions.csv`，每队每天 50 次提交，跑得快、改得快
- **正式赛模式**：把智能体打成 Python 程序包上传，每队每天 10 次（线上比赛阶段）

平台会用 Python 3.12 沙箱跑你的程序，**30 秒初始化预算**，跑完会给你三样东西：**分数分解、逐夜回放、运行日志**——你能精确看到"哪一夜、哪个 900 秒、哪个动作"扣了分、加了多少科学回报。

![图：复盘叠加图——两个智能体的策略差异一目了然](../assets/agent-observer/pdf-fig-10-2-review-overlay.jpg)

---

## §5 · 你能获得什么

- 💰 **\$5,500 奖金池，6 个奖项**——一等奖 \$2,000、二等奖 \$1,000 × 2、三等奖 \$500 × 3
- 🌐 **GOSIM Shenzhen 2026 大会曝光**——10 月 17 日深圳颁奖，与全球 150+ 讲师、2000+ 开发者同台
- 🏅 **完赛证书 + 官网留档**——所有完赛队伍均有官方证书，优胜者永久留档
- 💻 **排行榜 + 逐夜回放**——你的分数会被全球围观，每一份提交都有完整的可视化复盘
- 📦 **数据保留 90 天**——你有充足时间回头复盘自己的策略演化

> 🎯 **领奖不要求到场**——跨境参赛者线上领奖无障碍。

---

## §6 · 现在就开始

| 入口 | 链接 |
|---|---|
| **报名入口** | <https://bh3gei.github.io/agent-observer/register> |
| **赛题简报（8 章）** | <https://bh3gei.github.io/agent-observer/brief> |
| **新手上路（20 分钟跑通）** | <https://bh3gei.github.io/agent-observer/start> |
| **比赛规则（v1.0）** | <https://bh3gei.github.io/agent-observer/rules> |
| **实时排行榜** | <https://bh3gei.github.io/agent-observer/leaderboard> |
| **Starter Kit 源码** | <https://github.com/BH3GEI/agent-observer-starter-kit> |

**无需天文学背景，只需 Python 3.12。整个比赛你只需要改一个函数。**

10 月，深圳见。把夜空的下一步，交给你写的智能体。

---

![图：观测台主视觉——把镜头指向下一个 900 秒](../assets/agent-observer/cosmos-observatory-hero-BV_aYwWD.jpg)

---

## 附录 · 图片版权与署名

| 配图位置 | 文件 | 授权 / 来源 |
|---|---|---|
| 封面 / 文末收尾：观测台主视觉 | `cosmos-observatory-hero-BV_aYwWD.jpg` | GOSIM Agent Observer 公开素材 |
| §1 巡天控制室 | `cosmos-control-room-DALcRogD.jpg` | GOSIM Agent Observer 公开素材 |
| §2 智能体控制台权衡 | `survey-agent-strategy-XnSuOIcZ.jpg` | GOSIM Agent Observer 公开素材 |
| §2 状态字典示意图（FIG 8.1） | `fig8.1.png` | GOSIM Agent Observer 公开素材 |
| §3 DESI 5000 万星系红移地图 | `pdf-fig-1-2-desi-redshift.jpg` | Claire Lamman / DESI collaboration |
| §3 宇宙网 | `pdf-fig-1-1-cosmic-web.jpg` | NASA / ESA / Hubble · 公共领域 |
| §4 Alpha 扫描三面板 | `pdf-fig-10-3-alpha-sweep.jpg` | GOSIM Agent Observer 公开素材 |
| §4 复盘叠加图 | `pdf-fig-10-2-review-overlay.jpg` | GOSIM Agent Observer 公开素材 |

---

*本仓库维护者：cnbison · 配套工具：[`tools/md2wechat`](../tools/md2wechat/)（Markdown → 公众号 HTML 转换器）· 完整赛题见 [`references/survey26_brief.md`](../references/survey26_brief.md)*
