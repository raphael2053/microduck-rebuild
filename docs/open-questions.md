# 未知项与待验证清单

无实机路线下，这些是会直接卡住复刻进度的问题。按阻塞程度排序。

## 阻塞级

### 1. 结构件公差
官方 47 个 STL 是仿真网格，几何是对的，但没有制造公差、没有配合间隙、没有考虑打印收缩。直接打印大概率装不上。

- 需要：逐件加公差 → 试打 → 迭代
- 无实机意味着没有基准件可对照，只能靠装配关系（replica 项目称 0.1 mm 精度）反推
- 优先看 `microduck-replica-cad`（可编辑 SolidWorks）和 `microduck-hardware-replica`（FreeCAD），可编辑模型比 STL 好改得多

### 2. `imu_to_dxl` 板
官方从未发布。`pablo-mano/microduck-replica` 提供了第一份重建，但明确声明**从未流片、从未在硬件上验证**。

- 需要：审查重建原理图 → 自行打样 → 验证
- 这是整个硬件线风险最高的单点
- 目前有两份独立重建：`fanhao375/microduck-replica`（含嘉立创EDA 工程、原理图、PCB STEP、接线表）与 `pablo-mano/microduck-replica`。两份对上则可信度大增，对不上说明至少一份有问题
- ✅ **本项目已决定绕开它** —— 走 AI-FanGe 路线，用现成的 ROBOTIS OpenRB-150 做舵机总线，零自制 PCB。本条对当前路线**不再是阻塞项**，保留是为了将来若转向官方路线时能接着用。见 [roadmap.md](roadmap.md)

### 3. 线缆走线
完全无文档。15 个舵机的菊花链走向、传感器排线路径、电源分配，都要自己规划。

- 无实机 = 无法拆解对照
- 结构件内部走线空间是否够用，只能靠 CAD 推

## 需要确认

### IMU 数量与型号
`pablo-mano/microduck-replica` 列出 LSM6DSV16X（单数）；中文媒体报道称"两个惯性测量单元"。两者可能都对（如躯干 + 头部各一），也可能有一方有误。

- 核实途径：读 `pollen-robotics/microduck` 里 `robotd` 的 IMU 初始化代码，看实际打开几个设备

### NFC 读头型号
已知 2 个，型号未见公开。用途推测与配件识别或充电座有关。

- 核实途径：上游源码中搜 NFC 相关 daemon 或驱动

### 15 电机 vs 14 关节 —— 已有第三方答案，待自行核实
运动 policy 输出 14 维，但运行时有 15 个电机 ID。

`fanhao375/microduck-replica` 给出答案：第 15 个是**嘴**（`JOINT_NAMES[9] = "mouth"`，`MOUTH_INDEX = 9`），不进 policy 动作空间。该项目同时指出 ⚠️ MJCF 里根本没有这个关节 —— `robot_walk.xml` 只有 14 个 hinge joint / 14 个 actuator，嘴在所有 MJCF 中都是刚性并入 `jaw_soft` body。

- ⚠️ 这是第三方读源码的结论，本项目尚未自行核实
- 核实途径：读上游 `duck-control` 与 policy 加载逻辑，确认 `JOINT_NAMES` 与 `MOUTH_INDEX`

### 麦克风 / 扬声器型号
未见公开。影响音频链路的电气设计。

## 软件侧待摸清

- Policy 的 61 维观测具体构成（关节位置/速度/IMU/指令 的切分与顺序）—— 这决定了自制硬件的传感器布局能否直接复用出厂 policy
- `robotd` 与硬件的协议细节（`open-microduck` 有部分文档）
- 传感器标定流程 —— `open-microduck` 明确列为缺失项
- 出厂 policy 的 ONNX 输入是否对舵机型号/减速比有硬编码假设
