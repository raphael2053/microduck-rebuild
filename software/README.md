# 软件线

上游软件是 Apache-2.0 真开源，所以这条线不是逆向，是**吃透 + 改造**。无实机也能完整推进 —— `scripts/duck-sim` 能让真实 daemon 跑在 MuJoCo 的身体上。

## 状态

未开始。

## 规划

### 阶段一：跑通仿真
把上游的 `pollen-robotics/microduck` 和 `microduck_rl` 接进来，在 MuJoCo 里让鸭子走起来，用出厂的 9 个 ONNX policy。

目标产出：一条从 policy 文件到仿真里迈步的完整可复现路径。

### 阶段二：摸清接口
把 JSON-RPC 契约、50 Hz 控制环、policy 的 61 维观测构成写成文档。这些是自制硬件能不能复用出厂 policy 的前提 —— 见 [../docs/open-questions.md](../docs/rebuild/open-questions.md)。

### 阶段三：自己训
搭起 RL 训练环境，从零训一个步态出来。上游称 4096 并行环境下约 1–2 小时可得可用步态，但需要 CUDA GPU。

无 CUDA 时的退路（均来自社区）：`microduck-rl-torch`（PyTorch 原生）、`microdux`（JAX/MJX）、`microduck-rl-genesis`（AMD/ROCm）、`mjlab-sycl`（Intel GPU）、`microduck-lab` 的 Apple Silicon 版。

### 阶段四：适配自制硬件
等硬件线有实物后，把控制栈跑到自制机身上。这一步之前所有工作都在仿真里。

## 上游接入方式（待定）

三个选项，还没定：

| 方式 | 优点 | 缺点 |
|---|---|---|
| git submodule | 版本锁定清晰，不污染本仓历史 | 协作时容易忘记 `--recursive` |
| fork 后作为独立仓库 | 可以自由改动并提 PR 回上游 | 跨仓库同步麻烦 |
| 只写文档 + 脚本拉取 | 本仓最干净 | 复现依赖网络和上游可用性 |

倾向 submodule，但等阶段一实际动手时再定。

## 上游参考

- `pollen-robotics/microduck` —— Rust 控制栈，Apache-2.0
- `pollen-robotics/microduck_rl` —— RL 训练环境，Apache-2.0
- Hugging Face Hub `microduck-policies` —— 9 个出厂 ONNX policy

详见 [../docs/upstream.md](../docs/official/licensing.md)。
