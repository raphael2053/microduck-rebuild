# software/ AGENTS.md

## 产品

控制栈与 RL 训练线。上游是 Apache-2.0 真开源，所以这里的工作是**吃透与改造**，不是逆向。

这条线**不依赖硬件线**：上游 `scripts/duck-sim` 让真实 daemon 跑在 MuJoCo 的身体上，无实机也能完整推进。阶段规划见 `README.md`，此处不重复。

## 技术

| 用途 | 工具 |
|---|---|
| 控制栈 | Rust（上游单 workspace） |
| RL 训练 | Python + mjlab（MuJoCo Warp），PPO @ 50 Hz |
| policy 导出 | 上游 `microduck_rl` 的 `scripts/export.py` → ONNX，观测归一化器烘焙进计算图 |
| 仿真入口 | 上游 `microduck` 的 `scripts/duck-sim` |

训练需要 **CUDA GPU**（上游称 4096 并行环境约 1–2 小时得可用步态）。无 CUDA 时的社区退路见 `README.md`。

上游不含预训练权重，只能自训或从 checkpoint 恢复；9 个出厂 ONNX policy 在 Hugging Face Hub 上单独发布。

## 结构

上游运行时的形状 —— 动手前需要知道的：

- **进程模型**：一组 Rust daemon（`robotd` 控制环与电机总线、`mediad` WebRTC 推流、`tofd` 深度、`updaterd` 签名发布与回滚、`configd`、`btd`、`padd`）
- **IPC**：Unix socket 上的 JSON-RPC。App、console、手柄、脚本走**同一套调用** —— 新增客户端不需要新协议
- **控制环**：50 Hz
- **policy 接口**：61 维观测 → 14 维动作。实机有 **15 个电机 ID**，第 15 个是嘴、不进动作空间 —— ⚠️ 这是第三方读源码的结论，本项目尚未自行核实，见 `../docs/open-questions.md`

## 目录地图

| 文件 | 内容 |
|---|---|
| `README.md` | 阶段规划 |
| `POSTMORTEM.md` | 排查记录。**动手前先扫一遍**，确认不是已知问题。仅追加，绝不改已有条目 |

尚无子包 —— 代码未开始。

## 约定

**不要 vendor 上游代码。** 本仓根与上游同为 Apache-2.0，复制本身不构成许可冲突，但会丢失来源追溯、让上游更新难以合并。接入方式（submodule / fork / 脚本拉取）**尚未决定** —— 需要引用上游代码时先问，不要擅自选一种并落盘。确实要引入时，须保留上游 LICENSE 与版权声明，并按 Apache-2.0 第 4 条标注改动。

**不要假设 61 维观测的构成。** 各分量（关节位置/速度/IMU/指令）的切分与顺序尚未摸清，而这直接决定自制硬件的传感器布局能否复用出厂 policy。要用到时去读上游源码确认，别推测。

**读源码是回答硬件问题的手段。** `../docs/open-questions.md` 里有几个卡 BOM 的问题（IMU 数量、第 15 个电机）标注了"核实途径"，都指向上游源码。查到结论后回填 `../docs/`，并标注来源与日期。
