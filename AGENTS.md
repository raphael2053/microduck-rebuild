# AGENTS.md

> 本文件与 `.claude/skills/**` 由人维护，智能体不得编辑。需要变更时提出 diff 并停下。

## 产品

从零复刻 Microduck —— Pollen Robotics / Hugging Face 的 $399 双足鸭形机器人。无实机，纯自制路线。

- `software/` —— 控制栈与 RL 训练。上游开源，所以这条线是**改造**，不是逆向。
- `hardware/` —— 机械与电子。上游未发布设计文件，这条线是**真逆向**。
- `docs/` —— 两条线共享的上游调研事实基线。

## 技术

工具链跟随上游：**Rust**（控制栈）+ **Python**（RL 训练）。上游为 `pollen-robotics/microduck`（Apache-2.0）与 `pollen-robotics/microduck_rl`（Apache-2.0）。

当前仓库**无项目代码、无构建配置、无测试、无 CI**，处于规划阶段（`tools/checks/` 下有校验脚本，但不构成构建体系）。看到本节与实际不符时，说明代码已经开始落地 —— 按 harness-review 流程更新本文件。

检查脚本：`python3 tools/checks/check-links.py` 校验所有 markdown 的相对链接与锚点。

上游接入方式（submodule / fork / 脚本拉取）**尚未决定**，定了之后写进本节与目录地图。

## 结构

两条线并行，耦合点在 `docs/`：

- **软件线不依赖硬件线。** 上游 `scripts/duck-sim` 能让真实 daemon 跑在 MuJoCo 的身体上，所以无实机也能把软件线推到底。
- **硬件线部分依赖软件线。** 几个卡 BOM 的问题（IMU 数量、15 电机 vs 14 关节输出）只能靠读上游源码回答，不能靠推测。见 `docs/open-questions.md`。
- **许可证按目录分区**：根 Apache-2.0，`hardware/` CC BY-NC-SA 4.0。见下方「约定」。

## 目录地图

| 目录 | 用途 | 自有 AGENTS.md |
|---|---|---|
| `docs/` | 事实基线。`roadmap.md` 是执行计划与路线决定；`dictionary.md` 是术语表；`upstream.md` 只管上游官方事实；`ecosystem.md` 是社区项目的**唯一归属地**，别在两处重复记录；`hardware.md` 是已知规格；`open-questions.md` 按**阻塞程度**排序、不是追加序，插入新条目要重排。 | 无 |
| `software/` | 控制栈与 RL 训练线 | `software/AGENTS.md` |
| `hardware/` | 机械与电子线 | `hardware/AGENTS.md` |
| `tools/` | `checks/` 是校验脚本（L5），`hooks/` 是拦截脚本（L4）。 | 无 |
| `.claude/` | agent harness。`settings.json` 挂 hook，`skills/` 放 skill。人维护。 | 无 |

## 约定

**许可证是分区的。** 根 Apache-2.0，`hardware/` CC BY-NC-SA 4.0。

| 范围 | 许可证 | 为什么 |
|---|---|---|
| 仓库根（代码、文档、BOM、测量数据） | Apache-2.0 | 与上游代码同证，混用无摩擦，且带专利授权 |
| `hardware/` 下的 CAD / 网格 / 图纸 | **CC BY-NC-SA 4.0** | 衍生自官方 3D 模型，ShareAlike 强制继承 |

**事实不构成衍生作品。** 尺寸、型号、BOM 数量、独立测量、文字描述，即使写在 `hardware/` 里也适用根目录的 Apache-2.0。受 CC 约束的只有从官方 MJCF/STL 导出或修改得到的**几何**。

上游 README 把该证写作 "BY-SA-NC"，三要素顺序非标准；规范标识是 CC BY-NC-SA 4.0（SPDX `CC-BY-NC-SA-4.0`）。详见 `docs/upstream.md`。

**语言：以中文为主。** 文档、注释、commit message 用中文书写，但**专业名词保持英文原文，不做翻译** —— harness、MuJoCo、BOM、policy、daemon、ONNX、submodule、ShareAlike、sim2real 等一律用原文。中文承担叙述，英文承担术语。

**Commit。** Conventional Commits 前缀（`docs:`、`chore:` 等）+ 正文说明动机而非罗列改动 + 尾注 `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`。

**MCP 用个人 workspace。** 本机有两个 Linear MCP，本项目只允许 `mcp__linear-personal__*`，`mcp__linear-company__*` 禁止使用。详见 `CLAUDE.md`。这条**由 L4 hook 强制**（`tools/hooks/linear-guard.py`），不是靠自觉 —— 它同时校验 Linear 条目是否建在 `microduck-rebuild`（MDR）team 下。

**新术语要进术语表。** 本项目的维护者是软件工程师出身，机械与电子术语不是共识。文档里首次引入一个硬件/机械/电子术语时，在 `docs/dictionary.md` 补一条一句话解释 —— 没解释的术语等于没写。

**事实必须可追溯。** 写进 `docs/` 的任何上游事实都要标注来源与调研日期。来源冲突或未经硬件验证的条目用 `⚠️` 标注，不要抹平分歧。这个仓库的价值建立在"哪些是确证的、哪些是猜的"分得清楚上。
