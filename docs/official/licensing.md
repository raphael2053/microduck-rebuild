# 上游调研

调研日期：2026-09-14。所有条目按当时公开信息记录，使用前请复核。

## 开源边界

| 组件 | 是否开源 | 许可证 | 位置 |
|---|---|---|---|
| Rust 机器人栈（daemon 集合） | 是 | Apache-2.0 | `pollen-robotics/microduck` |
| RL 训练环境（mjlab / MuJoCo Warp） | 是 | Apache-2.0 | `pollen-robotics/microduck_rl` |
| 9 个出厂 ONNX policy | 是 | 开放 | Hugging Face Hub `microduck-policies` |
| GStreamer 插件（aarch64 预编译） | 是 | — | `pollen-robotics/microduck-gst-plugins` |
| MJCF 仿真模型 + 47 个 STL | 公开 | **CC BY-NC-SA 4.0** | 随 `microduck_rl` 发布 |
| RPI Robot HAT 电路板 | 是 | — | 完整 KiCad + gerber + BOM + pick-place |
| 机械 / 电子生产设计文件 | **否** | — | 未发布 |
| `imu_to_dxl` 板 | **否** | — | 未发布 |

结论：官方从未声称 Microduck 是开源硬件。软件栈开放，硬件设计文件封闭。

## 官方仓库

### pollen-robotics/microduck
机器人主控栈，Rust 单 workspace，Apache-2.0。

daemon：
- `robotd` —— 控制环 + 电机总线
- `updaterd` —— 签名发布与回滚
- `configd` —— WiFi 与身份
- `btd` —— 蓝牙
- `padd` —— 手柄输入
- `mediad` —— WebRTC 摄像头推流
- `tofd` —— 深度传感器

模块：`duck-control`、`duck-detect`、`duck-ether`、`kinematics`、`odometry`、`pet-detect`

进程间通信：Unix socket 上的 JSON-RPC。App、console、手柄、脚本走同一套调用。

仿真：`scripts/duck-sim` 让真实 daemon 跑在 MuJoCo 的身体上 —— 这是无实机开发的关键入口。

### pollen-robotics/microduck_rl
RL 训练环境，Apache-2.0（3D 模型部分 CC BY-NC-SA 4.0）。

- 仿真器：mjlab（MuJoCo Warp），PPO，50 Hz
- 任务：15 个，涵盖核心运动（速度跟踪、跌倒恢复、站姿控制）、技能（地面抓取、踢球、翻滚）、轮滑变体（速度、下蹲、斜坡、起身、旋转）；主要任务另有 backlash 变体，部分任务有平地/崎岖地形选项
- 训练硬件：需要 CUDA GPU，4096 并行环境下约 1–2 小时得到可用步态
- policy 导出：`scripts/export.py` 导出 ONNX，并把观测归一化器烘焙进计算图
- 不含预训练权重，需自行训练或从 checkpoint 恢复

Policy 接口：61 维输入 → 14 维动作。注意实机有 15 个电机 ID，但运动 policy 只控制 14 个关节。

## 社区项目

社区项目的导航、核实状态与对本项目的用处，统一见 [ecosystem.md](../rebuild/ecosystem.md)。本文件只管上游官方事实，不重复记录社区项目。

## 许可证约束

关键链条：**官方 3D 模型是 CC BY-NC-SA 4.0 → 任何从 MJCF/STL 衍生的 CAD 都继承该许可 → 非商用 + 相同方式共享**。

ShareAlike 条款要求衍生作品以相同许可证发布，这不是下游能选择的 —— 上游模型的版权不属于本项目，无权为其衍生物换证。

**命名。** 上游 README 写作 "BY-SA-NC"，三个要素顺序非标准（`creativecommons.org/licenses/by-sa-nc/4.0/` 返回 404）。规范标识是 **CC BY-NC-SA 4.0**，SPDX `CC-BY-NC-SA-4.0`，条款见 <https://creativecommons.org/licenses/by-nc-sa/4.0/>。指的是同一个证。

**本仓已采用分区许可**（2026-09-15 落实）：

| 范围 | 许可证 | 文件 |
|---|---|---|
| 仓库根 | Apache-2.0 | `/LICENSE` |
| `hardware/` | CC BY-NC-SA 4.0 | `/hardware/LICENSE` |

根目录选 Apache-2.0 而非 MIT，是为了与上游代码同证：混用无摩擦，且带专利授权条款。

**事实不受版权保护。** 尺寸数值、元件型号、BOM 数量、独立测量数据、文字描述均不构成衍生作品，即使写在 `hardware/` 下也适用根目录的 Apache-2.0。受 CC 约束的只有从官方模型导出或修改得到的几何。

自行从零绘制、不参考官方模型的零件不受此约束，但需要能证明独立来源。
