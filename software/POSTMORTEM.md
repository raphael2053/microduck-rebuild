# software — Post-Mortems

软件线的排查记录。**仅追加**，新条目加在最上面，绝不修改已有条目。

排查流程见 `troubleshoot` skill。动手前先扫一遍本文件，确认不是已知问题。

## 事故

### 2026-09-15：AI-FanGe 的策略在官方仿真器里不工作 —— 接口相容不等于可用

**影响**：阻塞 → 已解除（换官方策略）
**环境**：仿真，macOS arm64
**发现方式**：按上一条 postmortem 的修法实跑

**现象**：官方 `infer_policy.py` 加载 AI-FanGe 的 `walk.onnx` **完全没有报错** —— 日志显示 `Observation size: 51 (expected: 51)`、默认姿态与 `NEUTRAL_POSE` 逐项一致。但鸭子一进 viewer 立刻趴下，`trunk_z` 稳定在 44mm（站立基准 120mm）。

**排查步骤**：

1. 比对两边重力向量的约定。官方 `get_projected_gravity()` 用 `[0,0,-1]`，AI-FanGe 的 `observer.py:85` 用 `[0,0,+1]` —— 符号相反。同时注意到日志里 `kp_fw=200`，而 AI-FanGe 跑 RL 用 `KP_RL=125`。

2. 用官方脚本自身做无头扫描（stub 掉 viewer 使其跑固定帧数后退出，BAM、standby、decimation 全走真实路径），2×2 扫这两个变量。

   结果：`trunk_z` 分别为 42.2 / 40.0 / 30.7 / 48.1 mm，**四种组合全部趴下**。两个假设都被证伪。

3. **对照实验**：同一套脚手架跑官方 `alpha_walking.onnx`（加 `--new-cmd-obs`）。

   结果：`trunk_z=118.4mm`、`x=+1.093m` —— 站着并前进。**脚手架无误，问题在策略本身。**

**根因**：**接口相容不等于可用。** 51 维观测契约对得上，所以加载不报错；但策略权重里编码的是**它训练时那具身体的动力学** —— 质量、惯量、执行器参数、摩擦、关节限位。AI-FanGe 的训练模型已于 2026-09-11 从其仓库删除（`mjlab_microduck/src/mjlab_microduck/robot`），无从比对差异。

这**推翻了上一条 postmortem 的修法**（那条写的是"换官方运行时、只替换 policy 文件"，并已标注未验证）。

**影响范围**：阶段 0 改用官方策略即可完成，无阻塞。**不影响路线选择** —— AI-FanGe 的策略在他们**自己的实机**上有视频背书，"在上游仿真器里不工作"与"在实机上不工作"是两个命题。

**修法**：阶段 0 用官方栈 + 官方策略。

```bash
cd ~/Workspace/opensource/microduck_rl && uv run mjpython scripts/infer_policy.py     --walking ~/Workspace/opensource/microduck-policies/alpha_walking.onnx --new-cmd-obs
```

**预防**：

- **维度对得上只说明能加载，不说明能用。** 策略是权重不是纯函数契约，它隐含了训练时的那具身体。跨项目换策略前，先问"两边的机器人模型是不是同一个"
- 判断"是我的脚手架有问题还是被测对象有问题"，**跑一个已知good的对照**。本次两次扫描共 4 组都失败，但一个对照就定了性

**死胡同**（已证伪，别重走）：

- **重力符号相反** —— 约定确实不同（官方 −1，AI-FanGe +1），但翻转后 `trunk_z=40.0mm`，没有改善
- **`kp_fw` 不匹配** —— 官方 200、AI-FanGe RL 用 125，改成 125 后 `trunk_z=30.7mm`，更差
- 两者叠加 —— 48.1mm，仍然趴下

**可复用的验证手段**：

```bash
# 无头驱动官方 infer_policy.py：stub 掉 viewer，is_running() 跑够帧数返回 False
# 让 main() 自己退出。BAM / standby / decimation 全走真实路径，不重新实现。
# 完整脚本见本次排查，要点：
#   mujoco.viewer.launch_passive = lambda m,d,**kw: Stub(m,d)
#   ip.TerminalInput = NoInput   # 非 tty 下 termios 会炸
```


### 2026-09-15：AI-FanGe 仓库的仿真跑不起来，鸭子不走

**影响**：阻塞（阶段 0 / MDR-1）
**环境**：仿真，macOS arm64，无 GPU
**发现方式**：执行阶段 0，按教程跑 `make sim`

**现象**：`make sim` 启动即崩。换上上游的鸭子模型后能跑完 8 秒，但鸭子瘫在地上，位移仅 0.13 m。

**排查步骤**：

1. 直接跑，看完整 traceback。

   ```bash
   PYTHONPATH=src uv run --group sim src/sim/sim_main.py --hz 50
   ```

   结果：`ValueError: Actuator 'right_ankle' not found in MJCF model 'scene.xml'`。**不是** macOS viewer 的问题，崩在更早的模型加载阶段。

2. 比对模型里的 actuator 名与代码期望的名字。

   ```bash
   sed -n '/<actuator>/,/<\/actuator>/p' src/model/mjcf/robot.xml | grep -oE 'name="[^"]+"'
   ```

   结果：`shoulder_pitch`、`elbow`、`ankle_pitch`+`ankle_roll`，assets 里是 `humerus.stl`、`radius.stl`。**是人形机器人（microban），不是鸭子。**

3. 验证 policy 本身是不是鸭子的（ONNX 元数据是一手依据）。

   ```bash
   uv run python -c "import onnxruntime as ort; print(ort.InferenceSession('src/agents/walk.onnx').get_modelmeta().custom_metadata_map)"
   ```

   结果：14 个关节名与 `constants.py` 及上游 MJCF **三方逐项吻合**。策略是真的，只有模型是错的。

4. 换上游 `microduck_rl` 的鸭子模型重跑，逐个撞依赖问题：`vin_drop_gain` → 已改名 `vin_drop_resistance`；`max_current` 已移除；`bam.reset()` 不存在。PyPI 上 `better-actuator-models` 只有 1.0.0/1.0.1/1.0.2，**没有一个对得上**该代码。写适配层绕过。

5. 适配后能跑完，但鸭子倒地。做纯物理隔离测试 —— 关节锁死、零控制、只有重力。

   结果：`scene_walk.xml` 下鸭子沉到 z=−0.098（穿地）；`scene.xml` 停在 +0.046（正常）。**地面碰撞是场景文件的问题，与控制无关。**

6. 换 `scene.xml` 后不再穿地，但仍瘫倒。采样轨迹与 policy 实际收到的观测。

   结果：直立时 `projected_gravity = [0, 0, +1]`，而 `WalkMove.step()` 的跌倒保护是 `if body_projected_gravity[2] > -0.5: return`。**直立被判定为摔倒，policy 一次都没执行过。**

**根因**：两层。

表层是 AI-FanGe 仓库的 `microduck/src/model/` 装的是 microban 人形机器人的模型与 URDF，不是鸭子 —— 这是 fork 时留下的未维护残留。

深层是**方法错了**：把上游模型塞进 AI-FanGe 的控制栈，等于拼接两套独立演化的运行时，接缝有四处（机器人模型、执行器库版本、传感器坐标系、初始化顺序），每一处都不兼容。

**影响范围**：阶段 0 的既定做法作废，`docs/roadmap.md` 需改。**不影响路线选择本身** —— AI-FanGe 的硬件路线由实机视频和镜像下载量背书，仿真部分只是残留。顺带验证了 `.3mf` 打印文件确为鸭子（解包看切片预览图），阶段 2 的前提不受影响。

**修法**：整体改用官方运行时，只替换 policy 文件。

```bash
cd ~/Workspace/opensource/microduck_rl && uv run mjpython scripts/infer_policy.py \
    --walking <AI-FanGe仓库>/microduck/src/agents/walk.onnx
```

关键是**不加 `--new-cmd-obs`**：该参数切到 61 维新格式（13 维指令块），省略即 51 维旧格式，正是该策略的格式。macOS 上必须用 `mjpython`。
⚠️ 截至本条记录，此修法尚未实跑验证。

**预防**：

- 拼接两个项目的组件前，先数接缝。**接缝多于一处就该怀疑方法**，而不是逐个去补
- 判断仓库某部分是否可用，**先验文件本体**（解包、读元数据、比对零件名），别信目录名和 README
- 依赖未锁版本时，先核对已安装版本的 API 签名再调试行为

**死胡同**（已证伪，别重走）：

- **macOS viewer 需要 mjpython** —— 结论成立，但不是本次失败原因；程序在模型加载阶段就崩了，根本没走到开窗
- **电压压降参数映射错误** —— 把 `vin_drop_resistance` 置 None 后位移与高度**一字不差**，排除
- **IMU 安装角导致瘫倒** —— 置为单位四元数后数字完全相同。它确实让跌倒保护误判，但瘫倒发生在启动阶段，policy 还没接手

**可复用的验证手段**：

```bash
# 读 ONNX 真正要什么——关节名、默认姿态、输入输出维度
python -c "import onnxruntime as ort; s=ort.InferenceSession('P.onnx'); \
print(s.get_modelmeta().custom_metadata_map); print(s.get_inputs()[0].shape, s.get_outputs()[0].shape)"
```

```bash
# 比对 MJCF 的 actuator 名与代码期望
sed -n '/<actuator>/,/<\/actuator>/p' robot.xml | grep -oE 'name="[^"]+"'
```

```bash
# 纯物理隔离：关节锁死、零控制，只看会不会穿地。分离"控制问题"与"模型问题"
python -c "import mujoco; m=mujoco.MjModel.from_xml_path('scene.xml'); d=mujoco.MjData(m); \
d.qpos[2]=0.165; [mujoco.mj_step(m,d) for _ in range(600)]; print('final z =', d.qpos[2])"
```

```bash
# 验 .3mf 是不是名副其实——解包看切片预览图
python -c "import zipfile; zipfile.ZipFile('x.3mf').extract('Metadata/plate_1.png','/tmp')"
```
