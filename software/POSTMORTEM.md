# software — Post-Mortems

软件线的排查记录。**仅追加**，新条目加在最上面，绝不修改已有条目。

排查流程见 `troubleshoot` skill。动手前先扫一遍本文件，确认不是已知问题。

## 事故

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
