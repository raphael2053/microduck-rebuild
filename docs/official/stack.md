# 官方技术栈

核对自源码，日期 2026-09-16。✅ 是在源码/清单里直接读到的，⚠️ 是设计文档所述但未逐条核对源码的。

---

## 一、机上软件：Rust

✅ **一个 Cargo workspace，22 个 crate 平铺在仓库顶层**（不是 `crates/` 子目录）。

### 可执行的 daemon 与工具

| crate | 是什么 |
|---|---|
| `robotd` | 控制环 + 电机总线。**唯一能碰电机的进程** |
| `configd` | WiFi、身份、配对、重启 |
| `updater` | 发布校验、安装、切换、健康门、回滚 |
| `btd` | BLE 传输 |
| `padd` | 手柄传输 |
| `mediad` | 摄像头与音频管线，WebRTC |
| `robotctl` | CLI —— **必须能在坏掉的机器人上工作** |
| `duckctl` | 另一个 CLI（⚠️ 与 `robotctl` 的分工未逐条核对） |

### 库 crate

| crate | 是什么 |
|---|---|
| `duck-control` | **控制核心**：model、bus、sensing。舵机协议、观测拼装、策略推理、安全层都在这里 |
| `duck-ipc-proto` | IPC 协议定义。✅ `JOINT_NAMES` 这个 15 元数组就在这里（`src/lib.rs:436`） |
| `duck-ether` | 通信层 |
| `duck-detect` / `pet-detect` | 视觉检测（找其它鸭子 / 找宠物） |
| `kinematics` / `odometry` | 运动学 / 里程计 |
| `tof` | ToF 传感器 |
| `pad-imu` | 手柄 IMU |
| `sounds` | 音频 |
| `uyvy` | 图像格式转换 |
| `robotd-params` | 配置解析。✅ 默认值 `port = "/dev/ttyS2"`、`hz = 50` |
| `test-support` / `xtask` | 测试辅助 / 构建任务 |

命名沿用 Unix 传统，daemon 以 `d` 结尾 —— `robotd` 读作 "robot daemon"。

### `duck-control` 的关键依赖（✅ 读自 `Cargo.toml`）

| 依赖 | 版本 | 为什么是它 |
|---|---|---|
| **`rustypot`** | `1.6.0` | 舵机协议库。✅ **1.6.0 是下限不是偏好** —— 它修了"protocol 2.0 状态包载荷含 `FF FF FD` 时被反转义"的 bug，在此之前这类读取会返回超长包、让固定长度的 `sync_read` 解出垃圾。*一个 -1 的电流读数就足以触发* |
| **`serialport`** | `4.8` | ✅ 关掉了 `libudev` feature —— 那个 feature 只用于枚举端口，而这里是按路径打开固定的一个；且 `libudev-sys` 需要交叉编译时的 pkg-config sysroot，板子的 aarch64 构建没有 |
| **`ort`** | `=2.0.0-rc.11` | ONNX Runtime 绑定。✅ 用 **`load-dynamic`** —— 首次使用时 `dlopen` 而非链接 |
| `libloading` | `0.8` | 在碰 `ort` 之前先探测 ONNX Runtime 动态库是否存在 |
| `sha2` | `0.11` | 热插拔策略时识别未变化的网络 |

✅ **ONNX Runtime 是板级预装，不进发布包。** 设计文档原话：每个制品里塞 ~20 MB 是白费。这也让笔记本上没装 libonnxruntime 时照样能编译、能跑不创建 session 的全部测试。

### 异步与控制环

⚠️ 设计文档所述：控制环是一个 **`tokio`** 任务，跑在自己的 runtime 上，用 `interval` 配 **`MissedTickBehavior::Skip`**。

- `Burst` 会把积压 tick 连发，把电机指令摞在一起
- `Delay` 在每个 tick 后把下次安排在 *now + period*，于是每次唤醒延迟都加进周期，环越跑越慢
- `Skip` 保持原定时刻表、丢掉错过的 tick

### 进程间通信

⚠️ **unix socket 上的 JSON-RPC 2.0，一行一个对象**（NDJSON）。App、console、手柄、脚本走**同一套调用** —— 新增客户端不需要新协议。

---

## 二、媒体管线：GStreamer

⚠️ `mediad` 用 GStreamer，✅ 根 `Cargo.toml` 的注释提到它依赖 **Rockchip MPP**（硬件编解码）与 **`webrtcsink` / `webrtcsrc`** —— **这两样在任何 Debian 套件里都不存在**，所以官方单独发了 `pollen-robotics/microduck-gst-plugins`（aarch64 预编译）。

⚠️ 720p30 H.264 硬件编码 + WebRTC 推流；GStreamer 的拥塞控制占约 7.6% 一个核。

---

## 三、操作系统

⚠️ **Armbian**（Debian 系），headless，vendor 内核 **6.1.115**。

⚠️ `/var/log` 是 zram 设备 —— **日志吃 RAM 不吃盘**。

⚠️ **NPU（0.8–1 TOPS INT8）Armbian 默认关闭**，要刷设备树 overlay 才能用。而且 `duck_detect.onnx` 跑的是 CPU 不是 NPU（`.rknn` 才上 NPU，仓库里没有 `.rknn` 版本）。

---

## 四、策略训练：Python

在隔壁仓库 `pollen-robotics/microduck_rl`（Apache-2.0）。

| 项 | 值 |
|---|---|
| 仿真器 | **mjlab**（MuJoCo Warp） |
| 算法 | **PPO**（rsl_rl） |
| 频率 | 50 Hz，与机上控制环一致 |
| 包管理 | **uv** |
| 训练硬件 | CUDA GPU；4096 并行环境约 1–2 小时得可用步态 |
| 导出 | `scripts/export.py` → ONNX |

⚠️ **必须用 `export.py`，不能手工转 checkpoint** —— 观测归一化被烘进 ONNX 计算图（`Sub` / `Div` 算子），手工转的会让策略在运行时看到未归一化的观测。

⚠️ 仓库**不含预训练权重**。9 个出厂策略在 Hugging Face Hub 的 `pollen-robotics/microduck-policies` 单独发布，每个约 775 KiB。

无 CUDA 时有社区移植：PyTorch 原生、JAX/MJX、AMD ROCm、Intel GPU、Apple Silicon —— 见 [../rebuild/ecosystem.md](../rebuild/ecosystem.md)。

---

## 五、电路设计

✅ `elec_RPI_Robot_HAT` 用 **KiCad 9**。仓库里有 `main.kicad_sch`、`audio.kicad_sch`、`dynamixel.kicad_sch`、`elec_RPI_Robot_HAT.kicad_pcb`，以及每颗主要器件的 datasheet PDF。

---

## 六、构建与测试

⚠️ 需 **Rust 1.89+**。`cargo test --workspace` 无需硬件、网络或 Docker。

⚠️ **`mediad` 是 `cfg(target_os = "linux")`**，Mac 上不编译该 crate；`configd` 的 NetworkManager 客户端与 `btd` 的 BlueZ 客户端同样是 Linux-only —— 所以**本机测试全绿说明不了它们**，要按板子的 target 做 clippy。
