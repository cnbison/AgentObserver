# 风格审计 · Agent Observer 推广宣传片

> 输入类型：markdown 推广文（非产品代码仓库）
> 风格选择：default（用户已确认）
> 来源：`articles/agent-observer-promo-03-修正.md` + `assets/agent-observer/*`

## 色板与语义（从推广文与素材提取）

| 用途 | 色值 | 来源 |
|---|---|---|
| 背景 | 暖白 `#FAFAF7` / 极淡星蓝 `#0F1A2E`（夜空收尾图） | default fallback |
| 主文字 | 近黑 `#1C1917` | 推广文标题色 |
| 弱文字 | 中灰 `#9CA3AF` | 推广文图注色 |
| 强调（CTA / 数字） | 深空蓝 `#18242f` | 兄弟主题 sci-tech 主色 |
| 暖色点缀 | 暖橙 `#edb28b` | 兄弟主题 sci-tech 辅色 |
| 红色警示 | 浅红 `#DC2626`（仅"提示"标） | md2wechat marketing 主题色 |

字体：
- 英文：`Georgia`（衬线，气质稳重）
- 中文：`PingFang SC` / `Noto Sans CJK SC`（无衬线）

空间：
- 容器圆角 12px / 标签圆角 6px / 数字徽章 999px
- 章节之间留白 32–48px
- 阅读时间：每秒约 6–9 个中文字

## 素材来源（保留 attribution）

| 素材 | 来源 | 授权 |
|---|---|---|
| `survey-agent-strategy-XnSuOIcZ.jpg` | assets/agent-observer/（GOSIM 公开） | 公开素材，保留署名 |
| `cosmos-control-room-DALcRogD.jpg` | assets/agent-observer/（GOSIM 公开） | 公开素材，保留署名 |
| `cosmos-observatory-hero-BV_aYwWD.jpg` | assets/agent-observer/（GOSIM 公开） | 公开素材，保留署名 |
| `assets/fallback/preview.png` 等 | skill 默认 fallback | BSL-1.1（见 SOURCE.md） |
| `assets/audio/codepilot-score-example.py` | skill 示例 | 按 skill 授权改编 |

## 镜头适配决策

- **不接入**：无产品 UI 组件可接
- **可用素材**：3 张实景图作为静态/缓动镜头背景或字卡后景
- **替代镜头**：用 default 样式的字卡 + 数字徽章 + 流程条呈现"卖点"
- **保留品牌识别**：标题文案 / GOSIM · Agent Observer / 巡天智能体

## 风格选择理由

- default + 暖白/炭黑：与推广文 `assets/agent-observer/cosmos-observatory-hero-BV_aYwWD.jpg` 的"夜空观测台"视觉基调吻合
- 中英标题分工：英文（Georgia）作气质锚点，中文（PingFang SC）说人话
- 视觉例外原因已在 feature-evidence.md 登记
