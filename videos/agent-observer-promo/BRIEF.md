# 视频 brief

- 状态：分镜已就绪（plan.json demo:false），待写 React 视觉组件 + 配乐 + 验收
- 风格选择：default（暖白/炭黑，用户 2026-09-19 确认）
- 输入：articles/agent-observer-promo-03-修正.md（GOSIM Agent Observer · 巡天智能体黑客松 2026 推广文）
- 仓库：未指定（无产品代码库可接入，default 风格包装推广文素材）
- 产品 / 更新范围：GOSIM Agent Observer 黑客松 2026 启动宣传
- 发布平台：待记录（默认公众号 + B 站）
- 平台 / 画幅 / 时长 / 语言：1920×1080 / 30 fps / 50 秒 / 中文
- 品牌资源：assets/agent-observer/ 下 3 张实景图已复制到 public/images/
- 字体：英文 Georgia · 中文 PingFang SC（无衬线）
- 是否允许链接：是（create.gosim.org/survey26/ + shenzhen2026.gosim.org/）
- 声音：代码原创音乐（120 BPM / 50 秒）+ 独立动作音效（whoosh / click / pop / ding-dong）
- 例外：visualExceptionReason 与 audioExceptionReason 已在 plan.json 登记

## 已完成

- [x] evidence/feature-evidence.md（5 组卖点 + 来源行号）
- [x] evidence/style-audit.md（色板 / 字体 / 素材授权）
- [x] plan.json（50s / 9 镜头 / 双语标题 / 10 音效 cue）
- [x] public/images/（3 张实景图：cover-strategy / control-room / observatory-hero）
- [x] src/FilmVisual.jsx（9 个视觉：HeroIntro / CoreLoop / DecisionBadge / PrizeBoard / AudienceList / Requirements / Schedule / StartSteps / CTA）
- [x] src/presentations.jsx（按 shot.component 路由到 FilmVisual 子组件）
- [x] npm run build 验证编译（已通过）
- [x] assets/music.wav（50.000s / 立体声 / 120 BPM，DURATION 从 48 改为 50，节奏点对齐 shot 切点）
- [x] assets/sfx/（whoosh / click / pop / ding-dong × 4，从 skill 内置复制）
- [x] assets/master.wav（50.000s / BGM + 9 cue / 24-bit / music ducking）
- [x] renders/evidence/frame-{04,11,24,35,46}.png（关键静帧验证视觉）
- [x] renders/final.mp4（1920×1080 / H.264 + AAC / 50.000s / 2.4MB）
- [x] check_delivery.py 通过：errors=[], 仅 shot5 阅读速度 + 标准听感 review 警告
