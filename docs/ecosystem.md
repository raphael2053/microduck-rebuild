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

## 两条复刻路线的完整对比

核对日期 2026-09-16。⚠️ 标的是尚未验证或存疑项。

### 硬件

| | `fanhao375/microduck-replica` | `AI-FanGe/Microduck-build-tutorial` |
|---|---|---|
| **主控** | Radxa Zero 3W（RK3566，65×30mm） | Raspberry Pi Zero 2 W |
| **舵机** | 主线 **飞特 HD-1910-C001 ×15**；原版资料按 XL330 ×15 也齐全 | **Dynamixel XL330-M288-T ×14**（嘴为可选第 15 颗） |
| **总线适配器** | 集成在自制 **RPI Robot HAT** 上（官方已开源 KiCad） | 现成 **ROBOTIS OpenRB-150**，USB 接主控 |
| **自制 PCB** | **2 块**：Robot HAT + `imu_to_dxl` | **0 块** |
| **IMU** | LSM6DSV16X，**挂在舵机总线上**（id 200，与舵机同一次 `sync_read`） | BNO08x，**独立 I²C**（GPIO2/3） |
| **舵机 ID** | 左腿 20–24 / 颈头嘴 30–34 / 右腿 10–14 | **1–14 顺序**（右腿 1–5、左腿 6–10、头颈 11–14） |
| **接头间距** | 飞特 **2.0mm**（官方 XL330 是 2.5mm），`imu_to_dxl` 板上 J4/J5 两套并存 | Dynamixel **2.5mm**，JST EHR-03 |
| **电池** | Sony NP-F550（2S，6.6–8.4V） | 成品 **6V** 电池包 |
| **转动支撑** | 滚珠轴承 ×14（11× Ø22×16×4 + 3× Ø15×10×3） | **POM 垫片 + 钢垫片**（降成本） |
| **视觉/测距** | IMX219 摄像头 + VL53L8CX ToF | **无** |
| **结构件** | 上游 STL 直接打；飞特版 **8 个配合件要改模**（舵盘凹凸相反） | 自备 `.3mf`，67 件 / 5 板 |

### 软件

| | fanhao375 | AI-FanGe |
|---|---|---|
| **运行时** | 官方 Rust 栈（7 个 daemon） | **Python**，Marc Duclusaud 的部署代码 |
| **通信库** | 官方 `duck_control::bus`（Rust） | **`rustypot`** 的 `Xl330PyController`（Python 绑定） |
| **策略** | 官方 9 个 ONNX；⚠️ 飞特版**要按 HD-1910 重训** | 自训 `walk.onnx` |
| **观测维度** | **61**（13 维指令块） | **51**（3 维指令块，旧格式） |
| **仿真** | 上游 `microduck_rl`（mjlab） | ⚠️ 自带但**已损坏**（模型是 microban 人形机器人） |
| **部署方式** | 源码构建 + `robotctl update` | ⚠️ **预构建镜像** `microduck.img.xz`（733MB，已下载 455 次） |
| **许可证** | 脚本 Apache-2.0；CAD 与图纸 CC BY-NC-SA 4.0 | 根 MIT；**`microduck/` 控制软件 GPL-3.0**；`mjlab_microduck/` Apache-2.0 |

### 状态与文档

| | fanhao375 | AI-FanGe |
|---|---|---|
| **机械** | ✅ 整机装出实物（2026-09-13，15 颗 HD-1910 配好 ID 装机） | ✅ 有实机 |
| **电控** | 🔨 **台架通总线中**；`imu_to_dxl` 等打样 | ✅ 已验证 |
| **行走** | ❌ **尚未** | ✅ **有实机行走视频** |
| **策略可用性** | ⚠️ 飞特版需重训，提供了《HD-1910 训练前数据清单》 | ✅ 现成；⚠️ 但**不能移植到上游仿真器**（见 `../software/POSTMORTEM.md`） |
| **文档** | **31 份中文文档**：硬件入门、逆向推导、采购清单、构建日志、踩坑记录、调试记录 | README 一份 |
| **可编辑 CAD** | ✅ 配套仓库 `microduck-replica-cad`（SolidWorks，飞特版带 `-FT` 后缀，v2.0） | ⚠️ `microduck/cad/` **已于 2026-09-11 删除**，README 仍引用它 |

### 取舍

**AI-FanGe 的唯一但决定性的优势：有人走通了。** 实机行走视频 + 455 次镜像下载。零自制 PCB 让 `imu_to_dxl` 和线束两个最大阻塞项直接消失。

**fanhao375 的优势在资料密度与成本。** 文档是另一个量级，飞特方案舵机成本约为 XL330 的 1/2–1/5（取决于 XL330 走哪个渠道），且 HD-1910 在额定电压内工作（XL330 在这台机器上是超压 37% 运行）。代价是**没有人用它走通过**，且策略要重训。

**本仓已选定 AI-FanGe 路线**，决定过程与执行计划见 [roadmap.md](roadmap.md)。

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
