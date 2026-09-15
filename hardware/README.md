# 硬件线

官方**没有**开源机械与电子设计文件。这条线才是真正的逆向工程。

## 状态

未开始。无实机，纯自制路线 —— 所有尺寸和电气细节只能靠社区逆向成果加仿真模型推导。

## 三个难点

按风险排序，详见 [../docs/open-questions.md](../docs/open-questions.md)：

1. **结构件公差** —— 仿真 STL 不是制造文件，直接打印装不上
2. **`imu_to_dxl` 板** —— 官方未发布，社区重建版从未流片验证
3. **线缆走线** —— 完全无文档，且无实机可拆解对照

## 好消息

- 主板是现成的 **Radxa Zero 3W**，不需要复刻，直接买
- **RPI Robot HAT 官方开源了**完整 KiCad + gerber + BOM + pick-place
- 电池是通用的 **Sony NP-F550** 摄像机电池，易采购
- 传感器都是常见型号：IMX219 摄像头、VL53L8CX ToF、LSM6DSV16X IMU

真正要自己搞的只有：结构件、`imu_to_dxl` 板、线束。

## 规划

### 阶段一：BOM 与成本核算
把 [bom.md](bom.md) 补全，比价，算出真实成本。先确认这件事值不值得做 —— 光舵机就 $359–629。

### 阶段二：CAD 基线
选一个社区可编辑模型作为起点（`microduck-replica-cad` 的 SolidWorks 或 `microduck-hardware-replica` 的 FreeCAD），而不是从 STL 硬啃。

### 阶段三：公差迭代
单件试打 → 测量 → 改 → 重打。先做最简单的配合件建立公差基准，再推到全机。

### 阶段四：电子
RPI Robot HAT 按官方文件打样；`imu_to_dxl` 审查社区重建原理图后自行打样验证。

## 许可证

本目录采用 [CC BY-NC-SA 4.0](LICENSE)，与仓库根目录的 Apache-2.0 不同。原因是从官方 MJCF/STL 衍生的 CAD 受 ShareAlike 条款强制继承。

受约束的只有衍生几何。尺寸、型号、BOM 数量、独立测量与文字描述属于事实，不构成衍生作品，适用根目录的 Apache-2.0。见 [../docs/upstream.md](../docs/upstream.md#许可证约束)。

## 看不懂术语

本目录的文档术语密度最高。[../docs/dictionary.md](../docs/dictionary.md) 是给软件工程师写的词典 —— 过孔、沉头孔、DNP、上拉、去耦、钳位这些都在里面。

## 参考

社区复刻项目的导航、核实状态与可用之处，见 [../docs/ecosystem.md](../docs/ecosystem.md)。

**路线已定：走 AI-FanGe 路线**，理由与执行计划见 [../docs/roadmap.md](../docs/roadmap.md)。这条路线零自制 PCB，本目录原先列的三大难点里，`imu_to_dxl` 与线束两项**直接消失**，只剩结构件打印。
