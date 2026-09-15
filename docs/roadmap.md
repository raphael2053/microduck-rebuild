# 复刻 Roadmap

目标：**做出一台会走路的 Microduck**。不是做出最忠于官方的那台。

制定日期 2026-09-15，依据是两个社区项目当时的实际进度。上游生态变化快，超过一个月请重新核实。

---

## 路线决定：走 AI-FanGe 路线

两条路线**不是平级选择** —— 一条被证明走通了，另一条还没有。

| | `AI-FanGe/Microduck-build-tutorial` | `fanhao375/microduck-replica` |
|---|---|---|
| 实机行走 | ✅ **有视频，有 GIF** | ❌ 尚未 |
| 电控状态 | 全现成模块 | `imu_to_dxl` 等打样，台架通总线进行中 |
| 自制 PCB | **0 块** | 2 块 |
| 软件 | **预构建镜像**（733 MB，已被下载 455 次） | 需自行搭建 |
| 主控 | Raspberry Pi Zero 2 W | Radxa Zero 3W |
| 舵机总线 | ROBOTIS OpenRB-150（现成） | 自制 HAT + `imu_to_dxl` |
| IMU | BNO08x 走 I²C | LSM6DSV16X 挂舵机总线 |
| 舵机数 | 14 | 15（含嘴） |
| 许可证 | MIT | 分区，CAD 为 CC BY-NC-SA |

**为什么选它**：它把本仓 `open-questions.md` 里排名第一和第二的阻塞项**整个删掉了** —— 不用打板、不用验证 `imu_to_dxl`、不用啃线束。对硬件零经验的人，失败模式少一个数量级。

**代价**：与官方 Rust 软件栈不兼容，用不了出厂的 9 个 ONNX policy。但第一台的目标是**走起来**，不是复用官方软件。

**什么情况下改变这个决定**：fanhao375 的电控走通并公开验证结果；或者你的目标从"做一台能走的"变成"做一台与官方软件兼容的"。

> ⚠️ 别在第一台上换飞特舵机省钱。fanhao375 实测：**HD-1910 舵盘凸、XL330 舵盘凹，8 个配合件要改模重打**，而且 AI-FanGe 的代码是按 Dynamixel 写的。降成本和降风险在这里直接冲突。

---

## 关键路径：采购有交期

舵机和 OpenRB-150 可能要等一到两周。**先下单，等货期间做阶段 0**。

---

## 阶段 0 · 仿真先跑通（0 元，本周）

不花钱、不等货，先确认工具链是对的。**用官方栈 + 官方策略。**

```bash
brew install uv
git clone https://github.com/pollen-robotics/microduck_rl && cd microduck_rl && uv sync
```

官方策略在 Hub 的 `pollen-robotics/microduck-policies`。拿到后：

```bash
uv run mjpython scripts/infer_policy.py \
    --walking <策略目录>/alpha_walking.onnx --new-cmd-obs
```

三个要点，缺一个就跑不起来：

- ⚠️ **macOS 必须用 `mjpython` 而非 `python`** —— `launch_passive` 的线程归属限制
- ⚠️ **`--new-cmd-obs` 不能省** —— 出厂策略是 61 维观测（13 维指令块），不加维度不匹配
- ⚠️ **按键打进启动它的终端，不是 MuJoCo 窗口** —— 脚本用 `termios` 读 stdin

按 `↑` 前进，`A`/`E` 转向（不是 A/D），`SPACE` 归零，`Q` 退出。

**完成判据**：屏幕上的鸭子能走。

**为什么不能跳**：一次验证三件事 —— Python 环境、MuJoCo、ONNX 推理。任一有问题，硬件装好也跑不起来，而那时你分不清是硬件还是软件的锅。

⚠️ **不要用 AI-FanGe 的 `walk.onnx` 做这一步。** 它的 51 维接口与官方 legacy 模式相容、加载完全不报错，但在上游模型上站不住 —— 策略权重编码的是它训练时那具身体的动力学。实测对照：官方策略 `trunk_z=118mm` 并前进 1.09m，AI-FanGe 的 42mm 趴下。详见 [../software/POSTMORTEM.md](../software/POSTMORTEM.md)。它在**实机**上的有效性是另一个命题（有视频背书），留到阶段 6 验。

## 阶段 1 · 下单

按 AI-FanGe 的 BOM。价格是量级参考，**未核价**。

| 件 | 数量 | 量级 | 备注 |
|---|---|---|---|
| Dynamixel XL330-M288-T | 14 | ¥2800± | **成本大头**，别在第一台上替换 |
| ROBOTIS OpenRB-150 | 1 | ¥350± | 舵机总线控制板 |
| Raspberry Pi Zero 2 W | 1 | ¥120± | 主控 |
| BNO08x IMU 模块 | 1 | ¥100± | BNO080 / 085 / 086 都行 |
| 成品 6V 可充电电池包 | 1 | ¥50± | 不用自制 2S 电池组 |
| 高耐久 microSD 64G | 2 | ¥180± | 买两张，一张备份 |
| 电源开关、Dynamixel 3-pin 线、M2/M2.5 自攻螺丝 | 若干 | ¥100± | 螺丝多备 |
| 3D 打印件 | 1 套 | ¥50 自打 / ¥300± 代打 | 见阶段 2 |

**合计约 ¥3700**，高于官方整机 $399。自制的价值在学习和可改造性，不在省钱。

---

## 阶段 2 · 打印结构件

⚠️ **AI-FanGe 的 README 说"使用 `microduck/cad/` 中的模型"，但那个目录已于 2026-09-11 被删除。** 现在唯一的打印文件是仓库根目录的 `microduck3D打印.3mf`（5 MB）。

- 用 Bambu Studio 或 PrusaSlicer 打开 `.3mf`，里面已含打印参数
- 材料 PLA
- 没有打印机：淘宝代打印，或拓竹 MakerWorld 一键发送

**完成判据**：全部结构件打印完成，目测无明显翘边分层。

**已知的好消息**：fanhao375 在 2026-09-02 实测 **M2 螺丝能装进去、孔位可用** —— 说明这套几何的孔位是能用的，不必预期大规模返工。

---

## 阶段 3 · 舵机配 ID（最容易翻车的一步）

新手在这里翻车的概率最高，单独列一个阶段。

- 用 **Dynamixel Wizard** 逐个设置 ID
- ⚠️ **一次只接一颗**。出厂 ID 相同，同时接上全都应答，分不出谁是谁
- 改完立刻贴标签，写上关节名 + ID，拔掉，换下一颗
- ID 映射见 AI-FanGe README 的表：右腿 1–5、左腿 6–10、头颈 11–14

推荐参数（AI-FanGe 给的）：Protocol 2.0、1 Mbps、Return Delay Time 0、PWM Slope 255、Shutdown 去掉输入电压错误触发项。

**完成判据**：14 颗舵机各自 ID 正确，贴了标签，Wizard 能逐个点亮。

---

## 阶段 4 · 装配

按结构件把舵机装进去。参考 fanhao375 的 `构建日志.md` 和 `踩坑记录.md` —— 虽然路线不同，但机械部分通用。

**完成判据**：整机组装完成，关节能手动活动无干涉。

---

## 阶段 5 · 接线与台架测试

**不要装好就直接上电跑。** 先在桌面上测。

- 电源链：6V 电池 → 开关 → OpenRB-150 → 舵机总线
- Pi 由 5V 稳压单独供电，**两侧必须共地**
- BNO08x 走 I²C 接 Pi 的 GPIO2/GPIO3
- ⚠️ 上电前用万用表确认正负极
- ⚠️ 焊点要用热缩管或热熔胶绝缘

**完成判据**：上电不冒烟，OpenRB-150 能被 Pi 枚举到，14 颗舵机全部在总线上应答。

---

## 阶段 6 · 刷镜像与首次行走

这一步 AI-FanGe 已经替你做完了绝大部分。

1. 下载 `microduck.img.xz`（733 MB），`sha256sum` 校验
2. 用 Raspberry Pi Imager 刷进 SD 卡，OS customization 选 No
3. 编辑 `bootfs/network-config` 配 Wi-Fi。⚠️ Pi Zero 2 W **只支持 2.4GHz**
4. 首次启动等 1–3 分钟（自动扩展分区、重生成 SSH key）
5. `ssh user@microduck.local`，默认密码 `password`，**登录后立刻 `passwd` 改掉**
6. 扶住机器人，跑：

```bash
cd ~/microduck && PYTHONPATH=src .venv/bin/python src/main.py
```

程序会打开扭矩、平滑回到 neutral pose、加载 `walk.onnx`、接收键盘或手柄输入。

**完成判据**：鸭子走起来了。**到这里复刻目标达成。**

---

## 阶段 7 · 之后往哪走（可选）

走通之后才谈得上这些，现在不用想：

- **自己训 policy** —— 用 `mjlab_microduck/`，需要 CUDA GPU。本仓 `software/README.md` 列了无 CUDA 时的社区退路
- **加视觉** —— AI-FanGe 路线没有摄像头和 ToF，要自己加
- **转官方路线** —— 等 fanhao375 的电控验证完成，届时再评估
- **换国产舵机降成本** —— 有了第一台的经验再动，参考 fanhao375 的飞特改件记录

---

## 风险清单

| 风险 | 概率 | 后果 | 对策 |
|---|---|---|---|
| 阶段 0 跑不起来 | 中 | 阻塞，但零成本 | 先解决再买东西 |
| `.3mf` 打印件装不上 | 低 | 返工重打 | fanhao375 已实测孔位可用 |
| 舵机 ID 配错 | **高** | 关节乱动，难排查 | 一次一颗 + 贴标签 |
| 接线错误烧件 | 中 | 烧舵机或 Pi | 上电前万用表量正负极 |
| 电池供电不足 | 中 | 舵机抖动、掉电重启 | 确认电池能提供足够瞬时电流 |
| 上游仓库变动 | 中 | 文档与实际不符 | `.3mf` 和镜像先下载存本地 |

> ⚠️ 最后一条不是假想 —— AI-FanGe 已经删过 `microduck/cad/`、`microduck/docs/` 和两个 README，而主 README 至今仍引用着已删除的目录。**先把需要的文件存到本地。**
