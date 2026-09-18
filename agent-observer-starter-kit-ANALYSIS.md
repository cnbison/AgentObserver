# agent-observer-starter-kit · 深度分析

> 本文档对 `agent-observer-starter-kit/`（BH3GEI/agent-observer 官方入门包）做源码级拆解。
> 目标读者：希望从「改一行就跑通」走向「真正理解评分 + 设计可获奖策略」的参赛者。
> 配套阅读：[references/survey26_rules.md § 5 评分](references/survey26_rules.md)（用户面规则）、[agent-observer-starter-kit/README.md](agent-observer-starter-kit/README.md)（入门包自述）。

---

## 0. 一句话总结

starter-kit 是一份 **「评测平台镜像」**：本地 `local_runner.py` 用与官方平台**完全相同的协议、子进程隔离、超时与计分引擎**，让参赛者在自己电脑上跑出与提交后**逐分一致**的结果。代码层面只有两个核心约定需要理解——**participant-agent-protocol-v1**（JSON-Lines 子进程协议）与 **challenge-score-v3**（公开评分公式）。其它都是它们的实现细节。

---

## 1. 仓库结构与代码地图

starter-kit 本身 ≈ **5000 行 Python**（`.py` 文件合计 ~4669 行 + 文档与配置），拆为两条平行的依赖链：

```
agent-observer-starter-kit/
├── README.md / QUICKSTART.md / QUICKSTART_ZH.md / SKILL.md     # 文档
├── local_runner.py                                              # 本地评测入口（镜像平台）
├── pack_agent.py / sac_submit.py                                # 提交打包 + 官方 sac 客户端
├── fetch_scenario.py / make_scenario.py / score_decisions.py    # 场景生成 + 复盘工具
├── run_baseline.{command,bat,sh} / run_demo_week.{...}          # 一键脚本
│
├── agent/                          # 参赛者编辑区 —— 8 个 .py
│   ├── my_strategy.py              # ★ 唯一需要改的文件（用户面入口）
│   ├── minimal_agent.py            # 子进程入口：JSON-Lines I/O 循环
│   ├── decision_graph.py           # LangGraph 决策流水线（prepare → model → finalize）
│   ├── state.py                    # DecisionState TypedDict
│   ├── protocol.py                 # 协议常量与协议校验
│   ├── scoring_preview.py          # 本地预评分（与 challenge/scoring_preview.py 行为一致）
│   ├── model_factory.py            # 多 LLM provider 工厂（8 家）
│   └── reference_strategy.py       # 范例策略（≈ 与基线打平）
│
├── challenge/                      # 评测基础设施 —— 11 个 .py（参赛者一般不改）
│   ├── contracts.py                # 版本化的文件 schema（v1/v2/v3）
│   ├── observing_calendar.py       # 夜晚 × 时隙（slot）生成
│   ├── weather_simulator.py        # 方向性天气（含 5 类事件 × 5 类空间范围）
│   ├── tile_geometry_simulator.py  # 天区几何（高度、方位、气团、月光因子）
│   ├── observation_request_simulator.py  # 临时观测请求（mission）
│   ├── scoring_core.py             # ★ 权威 ChallengeScorer.replay()
│   ├── scoring_preview.py          # 公开当前预评分
│   ├── challenge_workflow.py       # ★ 评测主循环（ChallengeWorkflow.run）
│   ├── run_challenge.py            # JsonLineAgentProcess 传输层
│ └── replay.py                     # 复盘 HTML 渲染（可选）
│
└── scenarios/
    ├── dev-reference/              # 180 夜 / 7,928 时隙 / 64 tiles —— 完整开发场景
    │   ├── config/                 # 6 个 JSON：scenario / calendar / tile / weather / request / workflow / score
    │   └── outputs/reference/      # 15 个 CSV + 4 个 JSON 元数据
    └── demo-week/                  # 7 夜 / 294 时隙 —— 调试场景
```

> **职责边界**：`agent/` 是「参赛者可改」区域；`challenge/` 是「评测基础设施」，参赛者最多只读。

---

## 2. 协议层：`participant-agent-protocol-v1`

### 2.1 消息形式

平台与 Agent 之间**长期保持一个子进程**，所有消息是**一行一 JSON**（JSON-Lines），三种类型：

| 方向 | `message_type` | 含义 |
|---|---|---|
| platform → agent | `initialize` | 一次性，载荷为 `initial_publication`（完整公开目录 + 评分契约）。Agent **不应回复**。 |
| platform → agent | `decision_request` | 每个时隙一次，载荷为 `decision_snapshot`（当前候选 + 进度 + 周预报 + 临时请求）。 |
| agent → platform | `decision_response` | 每个 request 一条回应，必带 `decision_sequence`，动作只能是 `observe` 或 `wait`。 |

`minimal_agent.py` 的主循环只有 ~30 行就实现了这个协议（读取 `initialize` → 循环读取 `decision_request` → 写 `decision_response`），证明协议设计**刻意做得极简**：任何语言都能接入。

### 2.2 协议中的「时间安全」

`challenge_workflow.py:188-209` 的 `decision_snapshot` 有一个不显眼但关键的设计：

- **当前天气**：`self.scorer.weather.get_effective_conditions(slot.slot_id)` —— 用 `slot_id` 当 key，**只能查到已经发生的 slot**。
- **候选天区**：从 `self._night_windows(slot.night_id)` 中过滤出 `start ≤ moment < end`。
- **每周预报**：只在「`night_index % weekly_horizon_days == 0`」且「该夜首 slot」才发布（`challenge_workflow.py:195`）。

也就是说：Agent **拿不到任何未发布时隙的真值天气**。这强制了「基于当前 + 公开预报」的策略空间，并防止了「偷看未来」式解。

### 2.3 动作约束

`challenge_workflow.py:212-228` 的 `_decision_from_response` 在 `validate-then-mutate`：

1. `protocol_version` 必须匹配（否则 `ValueError`）；
2. `message_type` 必须是 `decision_response`；
3. `decision_sequence` 必须匹配当前 request；
4. `action ∈ {observe, wait}`，否则 `ValueError`；
5. 若 `wait`，清空 `tile_id/program/request_id`。

校验失败 → workflow 立即终止为 `agent_error`，**不会回滚已提交动作**（已 commit 的保留）。这要求 Agent **任何一行 Python 异常都会让成绩作废**——本地跑通 ≠ 提交安全。

---

## 3. 评分层：`challenge-score-v3`

### 3.1 三档质量带

定义在 `scoring_preview.py:59-65`：

```
combined_quality = (instrument_efficiency * transparency * sky_quality)
                   / (seeing_arcsec * airmass ** airmass_exponent)
capped at maximum_weather_quality
capped at lunar_quality_factor

combined ≥ dark   threshold (0.65)  →  DARK  （+25% bonus）
combined ≥ bright threshold (0.40)  →  BRIGHT（+15% bonus）
否则                                →  BACKUP（+8% bonus）
```

**关键观察**：

- 三个 quality 字段都是 `[0,1]` 区间的小数；`seeing` 越小越好、`airmass` 越大越差（最常见的 `airmass^1` 衰减）。
- 月光因子是**外生惩罚**（最高 -75%），它按月相角与目标天区的高度/角距计算（详见 `tile_geometry_simulator.py`）。
- `airmass_exponent` 与 `maximum_weather_quality` 在 `weather_config.json` 的 `score_interface` 段里，参赛者可读但不可改。

### 3.2 单次观测的价值

```
base_science  = V_tile × combined_quality                （若已观测过则为 0）
program_bonus = base_science × bonus[band]               （DARK 0.25 / BRIGHT 0.15 / BACKUP 0.08）
science       = base_science + program_bonus
              = base_science × (1 + bonus[band])
```

`V_tile` 来自 `tile_config.json` 中的 `target_models`（`LRG/ELG/QSO/BGS` 四类），按星系/类星体计数 + 红移分布 + 流量权重生成（参考 [survey26_brief.md § 6](references/survey26_brief.md) 名词解释）。**`V_tile` 不在公开评分合同里给数字**，但**它固定在 scenario 里**（同 seed 同 scenario → 同 V_tile）—— 参赛者可以在本地解算后做离线缓存。

### 3.3 终局惩罚（必须躲）

`scoring_preview.py:172-185` + `scoring_core.py` 把它们落到 `score["penalties"]`：

| 触发条件 | 罚款 | 备注 |
|---|---|---|
| `unsafe_observation` | **2000** | 单次天文台禁区的动作（如太阳天区），**单条就足以毁灭全场** |
| `invalid_action` | 100 | 选了不存在的 tile/program/request |
| `avoidable_wait_per_second` | 0.001/s | 在 weather 明显 wrong 时仍然 wait |
| `required_miss` | **1000/tile** | 必做天区（REQUIRED）整场没观测 |
| `flexible_shortfall_per_tile` | **100/tile** | 每 region 的 FLEXIBLE 没做满 quota（默认 4） |

> **赢的关键不是「能拿多少 bonus」，而是「能躲开多少罚」**。基线 12.287 已经接近「无罚满分」，上面提升 1% 很难，下面掉 5% 极容易（一个 unsafe observation 就 -2000）。

### 3.4 临时观测请求（请求奖励）

`observation_request_simulator.py` 模拟「导师半夜扔过来的紧急任务」，规则：

- `request_id`、`available_from` ~ `deadline` 时间窗；
- `completion_mode ∈ {ALL, AT_LEAST_N}`：要么做齐所有 `tile_requirements`，要么至少 N 个；
- 每个 tile 有 `required_visits`（一般 1 次）；
- 奖励 = `completion_reward - miss_penalty`（完成 +X，未完成 −Y），按 remaining required tiles 平摊到 preview。

> 范例策略不处理请求也能跑通基线，但**真实高分策略必须持续跟踪请求**——尤其是 deadline 紧的 `time_limited_required` 类。

---

## 4. 仿真层：`challenge/` 三件套

### 4.1 观测日历（`observing_calendar.py`）

- 站点经纬 `31.9634°, -111.599°`，时区 UTC-7，太阳高度阈值 `-12°`（民用昏影）。
- 每个 `night` 是一段 **太阳在地平线下超过阈值的连续时段**；每夜切成 ~44 个 `slot`，每个 `slot` 长 **900 秒**（15 分钟）。
- `slots_by_night` 是按时间排序的扁平列表；workflow 用 `_offset_seconds = elapsed % 900` 切出当前 slot。

### 4.2 天区几何（`tile_geometry_simulator.py`）

对每个 tile，每秒可查 `altitude_deg / azimuth_deg / airmass / lunar_quality_factor`：

- `altitude_deg < minimum_altitude_deg (30°)` → 该 tile 不可观测，从候选剔除。
- 月光模型：`lunar_quality_factor = max(1 − penalty × decay(angular_distance, scale=35°), 1 − maximum_penalty=0.75)`——简单衰减，满月压顶时所有目标基本打 25% 折。

### 4.3 天气仿真（`weather_simulator.py`）

这是整包最有意思的一段——它模拟的是**真实望远镜运行的天气，不是简化随机**：

**事件类**：`rainy / cloudy / smoggy / rocket_launch / cold_wave / tornado`，每类有：

- `count`：总事件数；
- `duration_slots`：持续 slot 数范围；
- `scope_weights`：空间范围类型权重；
- 各自的 `seeing/transparency/sky_quality/instrument_efficiency` 乘子。

**空间范围**（**5 类**，每个事件只能选其一）：

| `spatial_scope_type` | 含义 | payload |
|---|---|---|
| `ALL` | 全球（主天气 + 关闭） | `{}` |
| `REGION_SET` | 命中 region 子集 | `region_ids` |
| `TILE_SET` | 命中 tile 子集 | `tile_ids` |
| `SKY_CAP_ICRS` | 天球内某锥形区域 | `ra_deg / dec_deg / radius_deg` |
| `HORIZON_SECTOR` | 地平面某扇区 | `azimuth_start / azimuth_end / min_altitude / max_altitude` |

后两类是**动态判定**——会在请求时按当前 slot 中点的 tile 高度/方位实时算 `_applies()`。这意味着**预报与真值之间存在几何不确定性**，贴近真实预报。

**预报**：每个事件对若干 nights 发出 forecast，`closeness` 越接近 0（领先 ≥ horizon），`uncertainty` 越大（≥900s，最大 ~7 小时），有 `miss_probability` 直接丢事件，还有 `false_positive_count` 个**永远不发生**的预报——这都在逼 Agent **不能盲信预报**。

**季节性**：`seasonal_phase_day + amplitude` 给 seeing/transparency/sky_quality 加正弦波动；`night_correlation / slot_correlation` 用 AR(1) 让相邻夜、邻 slot 的状态有相关性（真实天气也不是独立同分布）。这就是为什么一个 900 秒窗口内的策略不会比另一个差太多——**天气的「噪声带」天然很大**。

### 4.4 临时观测请求（`observation_request_simulator.py`）

- 每 `issue_every_n_nights` 夜有概率发布新请求（受 `occurrence_probability` 调控）；
- 每请求的 tile 子集与每 tile `required_visits` 由 `tiles_per_request` 范围随机；
- `deadline_class` 给三类固定窗口（如 7/14/30 天）+ 出现权重；
- `completion_reward / miss_penalty` 在 `request_config.json` 里给定。

---

## 5. Agent 流水线：LangGraph `prepare → invoke_model → finalize`

`decision_graph.py` 用 LangGraph 串起三个节点（`prepare` / `invoke_model` / `finalize`），把所有状态放进 `DecisionState`（`state.py`）：

```
snapshot_in → [prepare] → prompt
prompt → [invoke_model] → raw_response
raw_response → [finalize] → action_out → snapshot_in (next)
```

### 5.1 `prepare`（`decision_graph.py:78-115`）

把当前 `decision_snapshot` 序列化进 prompt：

- 候选 tiles（最多 Top-K=12，按 `preview_actions` 已排好序）；
- 当前 active_requests（去重后按 deadline 升序）；
- `progress`（已完成 tile、每 region 的 FLEXIBLE 完成数）；
- 最近 N 次动作历史（最近 8 条 `memory`）。

为了控制 token，`prepare` 主动**截断**长字段、用 emoji 标签简化结构，并加 `KEY_RULES` 段把「不能 unsafe / 必须 JSON / 必须返回合法 tile」写死。

### 5.2 `invoke_model`（`decision_graph.py:118-159`）

调用 LangChain `ChatModel.invoke(messages)`：

- `temperature=0.1`（接近 greedy，但不绝对）；
- 单 slot **超时硬上限**：`agent_command_timeout_seconds = 30s`；
- 异常一律 fallback 到 `score_aware_fallback()`。

**8 个 provider**（`model_factory.py` 的 `PROVIDER_ALIASES`）：

```
openai / chatgpt        → langchain_openai.ChatOpenAI（支持 responses / chat completions）
anthropic / claude      → langchain_anthropic.ChatAnthropic
xai / grok              → langchain_openai + MODEL_BASE_URL
zai / glm               → langchain_openai + MODEL_BASE_URL
deepseek                → langchain_openai + MODEL_BASE_URL
moonshot / kimi         → langchain_openai + MODEL_BASE_URL
dashscope / qwen        → langchain_openai + MODEL_BASE_URL
minimax                 → langchain_openai + MODEL_BASE_URL
deterministic           → 不调外部 API，按 preview_actions 第 1 名返回（默认）
```

> OpenAI / Anthropic 走原生 adapter，其他 6 家走 **OpenAI-compatible 模式**——意味着只要厂商提供 `/v1/chat/completions` 端点就能接入。这对国内开发者极友好（DeepSeek / 智谱 / Qwen / Kimi 都在支持列表内）。

### 5.3 `finalize`（`decision_graph.py:162-220`）

是 Agent **最容易出 bug** 的一段，做 5 件事：

1. **协议校验**：`protocol_version / message_type / decision_sequence`；
2. **JSON 解析**：宽容解析（容忍 markdown 包裹、多余逗号）；
3. **白名单过滤**：候选 tile 必须出现在「给 LLM 的 Top-K」里——避免 LLM 幻觉出当前不可观测的 tile；
4. **非法动作检查**：`observe` 必须带 `tile_id` + `program ∈ {DARK,BRIGHT,BACKUP}`；`wait` 必须空；
5. **降级**：任何异常都 fallback 到「按 `preview_actions` 第一名 observe」，再不行就 `wait`。

> 也就是说，即使你完全不动 `my_strategy.py`，它也会按官方评分公式的预排序自动选 tile。这就是**基线 12.287 是怎么来的**。

### 5.4 `my_strategy.py`（用户面唯一入口）

53 行，包含一个 `choose_action(candidates, snapshot, memory) → Decision | None`：

- `candidates` 是已经按 `preview_actions` 排好序的 Top-K；
- `snapshot` 是当前 `decision_snapshot`（含候选进度 + 请求）；
- `memory` 是 LLM 上一次决策的记忆（最近 8 条）。

**4 个常见改法**（注释里都写好了）：

```python
# 改法 #1：优先 DARK 质量带
if cand.program == "DARK":
    return cand

# 改法 #2：必做天区优先
if cand.scheduling_class == "REQUIRED":
    return cand

# 改法 #3：避免凌晨恶劣天气
if cand.window_end_utc - now < timedelta(minutes=20):
    return None  # wait

# 改法 #4：处理临时请求
for req in snapshot.active_requests:
    if cand.tile_id in [r.tile_id for r in req.tile_requirements]:
        return cand
```

---

## 6. 评测主循环：`ChallengeWorkflow.run`（`challenge_workflow.py`）

整个回放逻辑 ~120 行，是理解「Agent 究竟在跑什么」的关键：

```python
while scorer.current_slot() is not None:
    if now >= deadline: break                  # 1. 全局超时
    snapshot = decision_snapshot(seq)         # 2. 时间安全的快照
    response = provider(snapshot, deadline)   # 3. 调 Agent
    if completed_at >= deadline:              # 4. 提交后才超时 → 丢这次
        termination = "global_wallclock_expired"
        ignored_in_flight_response = True
        break
    decision = _decision_from_response(...)    # 5. 协议 + 动作校验
    result = scorer.apply_decision(decision)   # 6. 提交到 scorer
    committed.append(decision)
    seq += 1
```

六步里最容易踩坑的是 **#4**：在 `deadline` 前**发起**了 LLM 调用，但 LLM 实际返回在 deadline 后——这种**飞行中的请求会被丢弃且计为超时**。这要求 Agent **任何一次推理都要控制时间**——这也是 LangGraph 加 30s 单 slot 超时的原因。

**`ChallengeWorkflow` 与 `local_runner.py` 的关系**：

- `ChallengeWorkflow.run(provider, deadline)` 用的是「抽象 provider」接口（`Callable[[snapshot, deadline], response]`）。
- `local_runner.py` 把这个 provider 替换为 `LocalAgentProcess`，它**和官方平台完全一致**：独立 cwd、`PATH/HOME/TMPDIR` 重写、`.env` 注入、`stderr → agent.log`、进程组 kill（避免僵尸子进程）、30s 初始化超时。
- 这就是「本地跑出 12.287 ≈ 上传后平台跑出 12.287」的根本保证。

---

## 7. 策略空间与瓶颈分析

### 7.1 参考策略（`reference_strategy.py`）为什么「打平基线」？

参考策略的注释里写：

> 在 5 个新 seed 上跑 30 夜场景，与 greedy 基线打平。

原因很直接：

- 当前 `dev-reference` 场景 **7200 秒 wallclock / 7,928 时隙 ≈ 每个时隙 0.91 秒**——这其实**够用**。
- 但 180 夜里大部分是**晴夜 + 简单目标**——「按预评分第一名 observe」就能拿 ~95% 的分数。
- 真正能拉开差距的是：**临时请求**（参考策略没专门处理）+ **恶劣天气窗口**（参考策略没专门 wait）+ **FLEXIBLE region 均衡**（参考策略没主动补齐）。

### 7.2 进阶策略的几个方向

| 方向 | 难度 | 预期增益 | 风险 |
|---|---|---|---|
| DARK 优先 + REQUIRED 收尾 | ★☆☆ | +200~500 | 漏掉 BRIGHT 高 tile_science_value |
| 跟踪临时请求 + deadline 倒计时 | ★★☆ | +500~1500 | 误判 deadline 被罚款 |
| 月光回避（满月不打亮目标） | ★★☆ | +300~800 | 错过低空高价值目标 |
| 预报驱动的 wait（看到 cloud 就停） | ★★☆ | +500~1200 | 误信 false positive 被罚 avoidable_wait |
| FLEXIBLE region 均衡器 | ★★☆ | +200~600 | 没考虑优先级 |
| LLM 多步 reasoning（结合 memory） | ★★★ | +1000~3000 | 30s 超时 + LLM 幻觉 → agent_error |
| 强化学习 / 在线策略 | ★★★★ | +?? | 跑不完 180 夜 → 全场 0 |

**最高 ROI 方向**：**「预报驱动的 wait」+「deadline-aware 请求处理」**——两个都是「减罚」类策略，比「加 bonus」更稳。

### 7.3 评测确定性 = 同分保证

starter-kit 同一份提交，本地跑和平台跑**应当**逐分一致。但有一个隐藏的不确定性：LLM 调用的温度（`temperature=0.1` 而非 0）——同一 prompt 两次可能产生不同 action。**真实提交里要把 temperature 设为 0**，或者用 `deterministic` provider 跑基线。

---

## 8. 本地 vs 平台：5 个差异点

| 差异 | 平台行为 | `local_runner.py` 镜像 |
|---|---|---|
| 子进程 cwd | Agent 自己目录 | `cwd=str(agent_dir)` |
| 环境变量 | 仅 `.env` 内容（`SAFE_ENV_KEYS` 过滤）+ 受保护白名单 | 同 |
| stderr | 平台日志 | `agent.log` |
| `PATH / HOME / TMPDIR` | 重写到隔离目录 | `scratch = out_dir / "scratch"` |
| 全局超时 | 7200s 后强杀 | `provider.close(force=True)` |

**真正的「不一致风险」**：

- LLM 网络抖动（平台会重试 3 次，本地默认 1 次）；
- 时间偏移（LLM 返回时间计入 wallclock）；
- `decision_replay.html` 的渲染差异（可选功能，缺失则无影响）。

---

## 9. 给参赛者的 7 条具体建议

1. **先跑基线** —— `python3 local_runner.py --scenario scenarios/dev-reference` 确认 12.287 + 64/64 tiles + 17/18 requests（这是健康基线）。
2. **不要改 `my_strategy.py` 之外的任何文件** —— 平台只接受这一个文件（`pack_agent.py --no-env` 会打包必需文件但提交页面上传单文件）。
3. **temperature 必须设 0** —— 不然同一提交两次跑分不一样。
4. **本地 wallclock 设 600s 而非默认 7200s** —— 调试时省 12 倍时间，逻辑一致。
5. **debug 时加 `--show-agent-stderr`** —— 能看到 prompt/response；正式跑时关掉（写入日志）。
6. **重视 `--init-timeout 30`** —— LLM 第一次握手若卡死，**整个提交 0 分**。
7. **超时防御**：在 `finalize` 里加 `len(memory) < 8000` token 限制；超长 prompt 直接 fallback。

---

## 10. 一句话架构图

```
┌─────────────────────────────────────────────────────────────┐
│  Platform / local_runner.py                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ChallengeWorkflow.run(provider, wallclock)               │ │
│  │   while current_slot:                                    │ │
│  │     snapshot = decision_snapshot(seq)    ← 时间安全     │ │
│  │     response = provider(snapshot, deadline)              │ │
│  │     scorer.apply_decision(decision)        ← 权威裁判   │ │
│  └─────────────────────────────────────────────────────────┘ │
│           ▲                                                   │
│           │ JSON-Lines (participant-agent-protocol-v1)        │
│           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ minimal_agent.py  (子进程入口)                            │ │
│  │   for line in stdin:                                     │ │
│  │     if line.type == initialize: state = line.payload    │ │
│  │     if line.type == decision_request:                    │ │
│  │       action = decide(state, line.snapshot)              │ │
│  │       print(action.to_jsonl)                            │ │
│  └─────────────────────────────────────────────────────────┘ │
│           ▲                                                   │
│           │ decide(state, snapshot)                           │
│           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ decision_graph.py (LangGraph)                            │ │
│  │   prepare → invoke_model → finalize                      │ │
│  │     prepare:   serialize snapshot + Top-K + memory       │ │
│  │     invoke:    LLM (or deterministic fallback)           │ │
│  │     finalize:  protocol validate + whitelist + fallback  │ │
│  └─────────────────────────────────────────────────────────┘ │
│           ▲                                                   │
│           │ uses public score_config                          │
│           ▼                                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ scoring_preview.py  (公开当前预评分)                      │ │
│  │   preview_actions(snapshot, scoring_contract)            │ │
│  │     → list[CandidatePreview]  (sort by gain/sec)         │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 11. 局限与下一步

starter-kit 的设计哲学是 **「评测即真相」**：

- ✅ 协议透明（JSON-Lines，单文件可改）
- ✅ 评分公开（`challenge-score-v3` 全公开）
- ✅ 本地镜像（无平台独占代码）
- ⚠️ **但没提供「可视化诊断」**——为什么这次 observe 失败？是因为 airmass 高，还是因为 weather？看 `decisions.csv` + `score_report.json` 需要自己写分析脚本。
- ⚠️ **没提供「强化学习」接口**——`scoring_core.replay()` 只接受完整决策序列，不支持在线增量。

**对官方团队的建议（不在本仓库范围内）**：

1. 加一个 `agent/strategy_debugger.py`，画出 `cumulative_score_over_time` + `band_distribution`；
2. 把 `reference_strategy.py` 注释里说的「5 个 seed 30 夜」公开成 regression 测试集。

---

## 附录 A · 关键文件交叉索引

| 主题 | 文件 | 行号（大致） |
|---|---|---|
| 协议常量 | `challenge/contracts.py` | `PARTICIPANT_PROTOCOL_VERSION = "participant-agent-protocol-v1"` |
| 评分常量 | `scenarios/dev-reference/config/score_config.json` | `schema_version: challenge-score-v3` |
| 时间安全发布 | `challenge/challenge_workflow.py` | `decision_snapshot()` 全文 |
| 权威评分 | `challenge/scoring_core.py` | `ChallengeScorer.replay()` |
| 公开预评分 | `challenge/scoring_preview.py` | `preview_actions()` |
| 用户入口 | `agent/my_strategy.py` | `choose_action()` |
| LangGraph 流水线 | `agent/decision_graph.py` | `prepare / invoke_model / finalize` |
| 多 LLM 工厂 | `agent/model_factory.py` | `PROVIDER_ALIASES` |
| 本地评测 | `local_runner.py` | `LocalAgentProcess` |
| 方向性天气 | `challenge/weather_simulator.py` | `WeatherSimulator._applies` / `generate_forecasts` |

## 附录 B · 官方评分契约（公开值快照）

来自 `scenarios/dev-reference/config/score_config.json`：

```json
{
  "schema_version": "challenge-score-v3",
  "quality_thresholds": { "dark": 0.65, "bright": 0.40 },
  "program_bonus":      { "DARK": 0.25, "BRIGHT": 0.15, "BACKUP": 0.08 },
  "penalties": {
    "unsafe_observation":         2000.0,
    "invalid_action":             100.0,
    "avoidable_wait_per_second":  0.001,
    "required_miss":              1000.0,
    "flexible_shortfall_per_tile":100.0
  },
  "flexible_quota_per_region": 4
}
```

```
⚠️ 本仓库不修改这些值，但参赛者在「自我对练」时可在自己的 scenario 副本里调参做消融。
```