# microduck-rebuild

从零复刻 [Microduck](https://pollen-robotics.com/microduck/) —— Pollen Robotics / Hugging Face 于 2026-08-27 发布的 $399 双足鸭形机器人。软硬件双线并行。

## 这个项目到底要做什么

Microduck 的**软件是真开源**（Apache-2.0），**硬件不是**。所以"复刻"的实际含义是：

- **软件线** —— 不是逆向，是吃透并改造。上游 Rust 控制栈和 RL 训练环境可以直接用。
- **硬件线** —— 这才是真正的逆向工程。官方未发布机械/电子生产文件。

详见 [docs/upstream.md](docs/official/licensing.md) 的开源边界分析。

## 下一步做什么

看 **[docs/roadmap.md](docs/rebuild/roadmap.md)** —— 分七个阶段，从零成本的仿真验证到实机走路，每阶段有完成判据。

路线已定：**走 fanhao375 路线**（飞特 HD-1910）。跑官方 Rust 栈，舵机换国产，两块板自己打样。

原先选的 AI-FanGe 路线因 XL330 供货（Seeed 需 4–6 周、淘宝涨到 ¥700+）被推翻。⚠️ 代价是这条路线**没有人走通过**，且策略要全部重训。

## 当前状态

**规划阶段** —— 无实机。路线已定，尚未开始采购与实现。

| 线 | 目录 | 状态 |
|---|---|---|
| 软件 / 仿真 / RL | [software/](software/) | 未开始 |
| 机械 / 电子 | [hardware/](hardware/) | 未开始 |
| 研究与文档 | [docs/](docs/) | 上游调研已完成 |

## 三个真正的难点

1. **结构件公差** —— 官方 47 个 STL 是仿真网格，不是制造文件，直接打印大概率装不上，需要公差迭代。
2. **`imu_to_dxl` 板** —— 官方从未发布，社区重建版本从未流片验证过。
3. **线缆走线** —— 完全无文档。

## 成本提醒

15 个 Dynamixel XL330 舵机单买约 $359–629，已接近或超过整机 $399 售价。自制的价值在学习和可改造性，不在省钱。

## 文档

- [docs/roadmap.md](docs/rebuild/roadmap.md) —— **复刻路线图**：路线决定、九个阶段、风险清单
- [docs/architecture.md](docs/official/architecture.md) —— 官方架构完整参考：C4 图、状态机、时序图
- [docs/dictionary.md](docs/dictionary.md) —— **术语表**：给软件工程师看的机器人硬件词典，看不懂别的文档时先来这里
- [docs/upstream.md](docs/official/licensing.md) —— 上游官方事实：开源边界、许可证
- [docs/ecosystem.md](docs/rebuild/ecosystem.md) —— 生态导航：社区复刻项目与两条路线对比
- [docs/hardware.md](docs/official/hardware.md) —— 已知硬件规格
- [docs/open-questions.md](docs/rebuild/open-questions.md) —— 未知项与待验证清单

## 许可证

分区许可：

- **仓库根** —— [Apache-2.0](LICENSE)，与上游代码同证
- **`hardware/`** —— [CC BY-NC-SA 4.0](hardware/LICENSE)，因为衍生自官方 3D 模型，ShareAlike 强制继承

事实性内容（尺寸、型号、BOM 数量、测量数据、文字描述）不构成衍生作品，一律适用 Apache-2.0。详见 [docs/upstream.md](docs/official/licensing.md#许可证约束)。
