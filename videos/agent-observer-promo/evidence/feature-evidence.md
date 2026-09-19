# 卖点证据 · Agent Observer 推广宣传片

> 输入：`articles/agent-observer-promo-03-修正.md`（GOSIM Agent Observer · 巡天智能体黑客松 2026 正式推广文）
> 状态：published（赛事已官宣，10/5–10/7 正式比赛）
> 版本/日期：2026-09-19 截图；推广文自 2026-09-19 起作为正式版
> 来源：articles/agent-observer-promo-03-修正.md L1–L222
> 风格：default（暖白/炭黑包装，无原 UI 组件可接入）

## 核心卖点（宣传片承载项）

| # | benefit | source | demoState | limits |
|---|---------|--------|-----------|--------|
| 1 | 比赛命题：让 AI 决定巡天望远镜下一步看哪里 | promo L1 | 标题主字幕 | 无（已官宣） |
| 2 | 奖金池 $5,500 + 6 个现金奖项 | promo L7, L280–L283 | 数据卡 | 无 |
| 3 | 决策时隙 900 秒 = 15 分钟 | promo L33 | 数字 + 节拍点 | 无 |
| 4 | 一台电脑 + Python + 6 步跑通 | promo L102, L155–L159 | 流程条 | 无 |
| 5 | 赛程：10/1–4 培训 / 10/5–7 比赛 / 10/17 深圳颁奖 | promo L324–L326 | 时间线 | 无 |

## 受众与场景

- 主体受众：AI/Agent 开发者、Python 开发者、天文 / AI for Science 爱好者、学生与初学者
- 影片任务：让 30 秒到 1 分钟内理解"这是什么比赛 + 数字 + 怎么开始"
- 不需要呈现：技术细节（评分公式、协议 JSON、DESI 数据细节）

## 不展示的功能

- 无产品代码库可接入；视觉用默认样式（assets/fallback/）包装
- 不展示报名流程的网页 UI（无真实组件）
- 不展示比赛平台登录/提交页

## 例外声明

### visualExceptionReason
- **原因**：输入是 markdown 推广文章（articles/agent-observer-promo-03-修正.md），不是有 UI 组件的代码仓库。Skill 默认约束"原组件 + 真实功能"无法满足；改为 default 风格包装，以推广文 3 张实景图 + 关键数字为主视觉。
- **保留的产品识别**：使用推广文实际标题与文末品牌色（深空蓝 + 暖橙），保留 GOSIM / Agent Observer / 巡天智能体 三处官方表述。
- **依据**：用户 2026-09-19 确认路线 A；README 推广文为公开材料。

### audioExceptionReason
- 默认按硬约束"完整声音"：代码原创配乐 + 独立动作音效。
- 配乐沿用 skill 示例（48s / 120 BPM / PingFang SC 风格无衬线，欢快不过度），按本片 50 秒改编。
- 音效先找 Pixabay；找不到的类目回退到 skill 内置 WAV。
