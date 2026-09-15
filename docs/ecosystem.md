# 生态导航

Microduck 生态里值得跟的项目。**这是导航，不是清单** —— 只收已核实、且对本项目有明确用处的条目，每条说清楚"它有什么"和"我们能用到什么"。

完整的生态索引见上游的 `joeynyc/awesome-microduck`（100+ 项目），这里不复制。

本文件出现的硬件术语，解释见 [dictionary.md](dictionary.md)。

收录标准：已直接查阅过仓库内容（不是只看检索摘要），且能说出对本项目的具体用处。未核实的放在最后一节，不与已核实条目混排。

调研日期：2026-09-15。star 数与更新时间会变化，使用前请复核。

---

## fanhao375/microduck-replica

★727 · 更新 2026-09-13 · 脚本 Apache-2.0，`assembly-drawings/` 与 `cad/` 为 CC BY-NC-SA 4.0

最完整的中文逆向工程项目，许可结构与本仓相同（代码宽松证 + CAD copyleft 分区）。

**有什么**

- `cad/` —— 16 个 STL，已应用世界变换，导入即装配态（不可编辑）
- `hardware/imu_to_dxl/` —— **完整电控方案**：原理图 PDF、PCB PDF、PCB STEP、板框 DXF、嘉立创EDA 专业版工程（`.eprj2`）、接线表
- `BOM.md` / `BOM.en.md` —— 中英双语，数量取自上游 `robot_walk.xml` 的 geom 引用计数（38 种网格 / 75 个实例），每项标依据
- `docs/电控采购清单.md`、`docs/机械采购清单.md` —— 国内淘宝实链
- `docs/执行器选型.md`、`build-log/` —— 选型推导与构建日志

**对我们的用处**

1. **`imu_to_dxl` 的完整设计文件** —— 这是 `open-questions.md` 里风险排第二的单点，这个项目是目前唯一的公开方案。
2. **BOM 基线** —— 比本仓 `hardware/bom.md` 严谨得多，且补上了我们漏掉的**轴承（14 个）**和 **PCB 打样成本（$60–150 含 SMT）**。
3. **回答了我们的一个 open question** —— 第 15 个电机是**嘴**（`JOINT_NAMES[9] = "mouth"`，`MOUTH_INDEX = 9`），不进 policy 动作空间，所以 policy 是 61 维观测 / 14 维动作。该项目同时指出 ⚠️ MJCF 里根本没有这个关节，嘴在所有 MJCF 中都是刚性并入 `jaw_soft` body。
4. **一个我们完全没记录的硬件事实** —— ⚠️ **XL330 被超压运行**：额定 3.7–6.0 V，而 Microduck 供给 6.6–8.2 V。官方 HAT 原理图里 Dynamixel 接口直接接 `+BATT`，板上唯一的 5 V 降压是给主控的。该项目判断这是官方的有意选择，不是笔误。

**注意**

- ⚠️ 舵机型号 XL330-**M288-T** 是该项目的**推断** —— 上游源码只有 `motor_name="xl330"`，无后缀。
- ⚠️ 该项目自陈上游基线存疑：其 STL 对应 `microduck_rl` 的 `d424a0c`（2026-08-27），更早的基线在本地对象库中不存在，因此"重导出前后 geom 计数相同"未能验证。
- `cad/` 只有 STL，不可编辑。可编辑源在下面的配套仓库。
- 仓库根有 `tools/飞特/`（飞特 = FeeTech，国产舵机品牌），但 BOM 正文仍以 Dynamixel XL330 为准。国产替代路线是否可行，⚠️ 未核实。

## fanhao375/microduck-replica-cad

★28 · **无许可证声明** · 图纸作者 机械行者Robo

上一个项目的配套仓库，**可编辑 SolidWorks 三维图纸 + 21 页装配安装说明书**。

**对我们的用处** —— 目前唯一公开的完整可编辑机械模型。公差迭代（`open-questions.md` 排第一的阻塞项）从可编辑模型改，比从 STL 硬啃现实得多。

**注意** —— ⚠️ **该仓库没有任何许可证声明**。按默认规则即保留所有权利，使用前需要先取得授权。这与主仓明确的 CC BY-NC-SA 4.0 不同，别把两者的授权状态混为一谈。

## AI-FanGe/Microduck-build-tutorial

★853 · 更新 2026-09-11 · MIT

端到端构建教程，走的是一条**与官方不同的简化路线**。

**有什么**

- `microduck3D打印.3mf` —— 可直接切片的打印文件
- `mjlab_microduck/` —— 训练环境
- `bno08x_calibrate_ui.py` 等标定脚本
- URDF 描述、导出的 ONNX policy

**对我们的用处** —— 见下方路线对比。它最大的价值是**证明 `imu_to_dxl` 这个阻塞项可以绕开**。

**注意**

- 仓库里的 `.part` 文件**继承自上游** —— `microduck_rl` 本身就有 54 个 `.part` 与 STL 成对（onshape-to-robot 导出物），不是该项目的建模产物。
- 10 个 `.scad`（OpenSCAD）上游没有，是该仓库新增的。
- README 未给出总成本，也未推荐任何 CAD 软件。

## pablo-mano/microduck-replica

脚本 Apache-2.0；图纸与 CAD CC BY-NC-SA 4.0

从官方 MJCF 重建机械与电子：47 个 STL / 15 个刚体，装配关系精度 0.1 mm，7 张爆炸图与装配视图，BOM，以及 `imu_to_dxl` 板的重建。

**对我们的用处** —— `imu_to_dxl` 的第二份独立重建，可与 fanhao375 的方案交叉比对。两份独立重建对上则可信度大增，对不上则说明其中至少一份有问题。

**注意** —— ⚠️ 该项目明确声明其 `imu_to_dxl` 重建**从未流片、从未在硬件上验证**。

## SaberOnGo/open-microduck

独立逆向工程与文档项目，分 `control/` `hardware/` `learning/` `simulation/` `tools/` 五个分区，明确标注未解决项。

**对我们的用处** —— `robotd` 硬件协议、控制环、运动学与里程计的文档化程度最高。软件线摸接口时优先查这里。

**注意** —— ⚠️ 硬件部分自陈不完整，传感器标定流程明确列为缺失项。

---

## 两条复刻路线的对比

这是本文件最该记住的部分。

| | 官方 / fanhao375 路线 | AI-FanGe 路线 |
|---|---|---|
| 主控 | Radxa Zero 3W (RK3566) | Raspberry Pi Zero 2 W |
| 舵机总线 | 自制 Robot HAT + `imu_to_dxl` | **ROBOTIS OpenRB-150**（现成模块） |
| IMU | LSM6DSV16X | BNO080 / BNO085 / BNO086 |
| 舵机 | Dynamixel XL330 × **15**（含嘴） | Dynamixel XL330-M288-T × **14**（10 腿 + 4 头颈，无嘴） |
| 需自制 PCB | 2 块（Robot HAT + `imu_to_dxl`） | **0 块** |
| 与官方软件栈 | 兼容（同主控、同传感器） | 不兼容，需自行适配 |
| 难度 | 高 —— 打样 + 验证 `imu_to_dxl` | 低 —— 全现成模块 |

**但两条路线不是平级的** —— 截至 2026-09-15，AI-FanGe 路线有实机行走视频，fanhao375 路线的电控尚未走通（其作者的进度表显示台架通总线仍在进行中、`imu_to_dxl` 还在等打样）。

**本仓已选定 AI-FanGe 路线**，决定过程与执行计划见 [roadmap.md](roadmap.md)。

---

## 仿真与训练移植

上游 `microduck_rl` 需要 CUDA GPU。以下是社区提供的退路，均未逐一核实：

| 项目 | 平台 |
|---|---|
| `microduck-rl-torch` | PyTorch 原生，无需 CUDA |
| `microdux` | JAX / MJX |
| `microduck-rl-genesis` | AMD / ROCm |
| `mjlab-sycl` | Intel GPU |
| `microduck-lab`（Apple Silicon 版） | Mac 原生 |

---

## 待核实

从 `awesome-microduck` 索引中筛出、尚未直接查阅的：

- **ChinaMicroDuck** —— 制造路线对比 + 许可审计 + 验证报告
- **microduck-hardware-replica** —— FreeCAD 装配 + 可打印网格 + BOM
- **microduck-diy** —— 从仿真网格到可打印件的一个月构建日志
核实后按上面的格式移入正文，并注明查阅日期。
