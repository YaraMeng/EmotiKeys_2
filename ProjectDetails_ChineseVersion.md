# Project details

## 项目名与一句话

在 20×10 的像素网格里，用鼠标“描摹”你的心情；颜色在流动，钢琴在回应，头像在倾听。

## 2)技术架构（Python 主导 + 低延迟声画）

前端：HTML/CSS + Canvas（p5.js）+ Tone.js（浏览器端合成/播放，低延迟）+ GSAP（丝滑视觉过渡）

后端（Python）：FastAPI + WebSocket

提供情绪/乐理参数映射（scale、BPM、音长表、力度范围、音阶重心等）

可选：将用户“走位”的网格数据回传，做统计/回放/作品导出

数据：SQLite 或 JSON（保存用户一次会话的网格涂抹序列、情绪选择、截图）

说明：实时声音合成最好放在浏览器（Tone.js）以保证手感；Python 管理“情绪→乐理参数”的规则与状态，也满足课程“主要用 Python”的要求（API、状态机、记录、导出）。

## 3)交互与页面结构（UI）

### 布局

中央：插画头像（可拖拽轻微偏移，随情绪换表情）

围绕头像放置 4 个情绪标签（开心、平和、紧张、伤心）

下方：20×10 网格画布（100% 宽度保留 16:9，高度自适应）

右下：播放/暂停、清空、导出（PNG 截图 & JSON 轨迹）按钮

### 进入流程

鼠标点击头像 → “开始谱曲”（Tone.Transport.start；光标变成画笔）

鼠标移到某个情绪标签或其影响区域 → 当前情绪 mood = X（头像产生微偏移+表情变化）

在网格上移动/按下 → 每步落点触发颜色+音符；松开停止触发，但可继续移动着色（只视觉）

### 头像“拖拽/吸附”

根据鼠标与情绪标签中心的距离，对头像应用 8–12px 的平滑偏移（GSAP x/y，缓动 power2.out）

表情集（4张 PNG/SVG 或 Lottie）：开心大笑、平和微笑、紧张皱眉、伤心下垂

# 4)网格与颜色规则

网格：20×10；格子尺寸随窗口等比缩放；每格存状态 {mood, time, pitch, velocity, dur}

颜色映射（统一 HSL，带渐变）

开心 (Happy)：H≈45–55（金黄），S 高，L 中高；涂抹出现暖色条纹

平和 (Calm)：H≈180–200（青蓝），S 中，L 中；柔和渐变（网格边缘加淡淡圆角阴影）

紧张 (Tense)：H≈350–5（红），S 高，L 中低；随机颗粒/抖动纹理

伤心 (Sad)：H≈220–240（靛蓝），S 中低，L 低；纵向流动（细微噪声）



在鼠标移动时，对落点格子和邻域 1-ring 做 径向渐变，让“刷子”更有手感。

# 5)关键：情绪 → 钢琴乐理映射（音高/时值/力度/律动）

我们用四类音阶/和声 + 节奏/音长/力度/奏法，并结合你设定的“每几格出一个调”的节拍抽样规则。

## 5.1 音阶与和声（每个情绪一套预设）


| **情绪**   | **调式/音阶**          | **重心（起始音）** | **和声/色彩**              |
| ------------ | ------------------------ | -------------------- | ---------------------------- |
| 开心 Happy | **大调（Ionian）**     | C4 或 D4           | 明亮，三和弦多用，偶尔加 6 |
| 平和 Calm  | **五声音阶（大五声）** | G3/C4              | 稳定无半音冲突，适合延音   |
|            |                        |                    |                            |
|            |                        |                    |                            |


| 紧张 Tense | **弗里吉亚 Phrygian 或和声小调片段** | E4 | 半音邻近与下二度制造张力 |
| ------------ | -------------------------------------- | ---- | -------------------------- |


| 伤心 Sad     | **自然小调（Aeolian）**        | A3 | 下行动机、二度/六度，柔和   |
| -------------- | -------------------------------- | ---- | ----------------------------- |
 

Python 后端返回该情绪的音阶集合（例如 Happy = [C4, D4, E4, G4, A4…]）。

## **5.2 你的“每几格一个调”的节拍抽样**

* Happy：4 格一音——中速（BPM 110–120），八分音符为主，音高偏高（C5 及以上可偶尔触发），力度(velocity) 80–100。奏法：tenuto（音长 = 节拍 90%）。
* Calm：6 格一音——偏慢（BPM 70–85），二分/四分交替，音延长（legato，音长 = 110–140% 同步做交叠），力度 55–75，加混响。
* Tense：1 格一音——快（BPM 130–150），多为十六分音/装饰音，音高集中在中高区（E4–B5），力度 70–95，奏法 staccatissimo（音长 40–55%），可加入不规则休止（1/8 概率）。
* Sad：3 格一音——中慢（BPM 80–95），附点八分/四分，力度 50–70，下行音型概率更高；偶发波音（上/下邻音）。
 

实现：前端维护 gridStepCounter。当 counter % step[mood] == 0 就触发一次 playNote()。

## **5.3 位置→音高映射（让画面走位“可听见”）**

横轴 X：从左到右映射到音阶索引（或半音），例如 20 列对应音域宽度 2–2.5 个八度；

纵轴 Y：控制音区/强弱/滤波：越上方音高更高、力度略强，越下方更低更弱；

每种情绪可带音阶偏置（比如 Tense 上移半音的概率 15%）。

// 例：将坐标映射为音阶索引
const scale = currentScale; // 从后端拿到，如 [60,62,64,67,69...]
const ix = Math.floor(map(x, 0, cols-1, 0, scale.length-1));
const pitch = scale[ix] + octaveOffset(y); // octaveOffset: 基于 Y 加减 12


# **6. 动效与细节（“丝滑”的来源）**

* 头像拖拽：与情绪标签中心计算距离 → 归一化到 0–1 → gsap.to(head, {x:dx*12, y:dy*12, duration:0.25, ease:"power2.out"})
* 表情切换：crossfade 150ms；紧张时在眉/眼部叠加轻微抖动（CSS filter: contrast + subtle rotation）

* 网格刷子：落点格子即时上色，同时对周围一圈做 6–8 帧的扩散过渡（Canvas radialGradient + alpha 衰减）
* 音乐与画面同步：用 Tone.Transport 的 tick，对颜色衰减与节拍做轻绑定（比如每小节切一次辅助背景纹理）


# **7. 后端（Python）API 设计（FastAPI）**

```python
# GET /moods -> 基础配置
{
  "happy":   {"bpm":115, "step":4, "scale":"C_ionian",  "vel":[80,100], "legato":0.9},
  "calm":    {"bpm":78,  "step":6, "scale":"G_pentatonic","vel":[55,75], "legato":1.2},
  "tense":   {"bpm":140, "step":1, "scale":"E_phrygian","vel":[70,95], "legato":0.5},
  "sad":     {"bpm":88,  "step":3, "scale":"A_aeolian", "vel":[50,70], "legato":0.95}
}

# GET /scale?name=C_ionian -> 返回 MIDI 音级数组（含推荐音域）
{ "notes": [60,62,64,65,67,69,71], "octaves":[3,4,5] }

# WS /session -> 记录用户事件（进入情绪区域、网格落点、生成的音符），用于回放/导出
```

Python 侧同时提供 export：把一次会话的网格涂抹与音符序列导出 JSON；前端可用此 JSON 回放并生成截图/GIF。

# **8. 关键数据结构（前端**

```python
type MoodName = "happy"|"calm"|"tense"|"sad";

interface Cell {
  mood: MoodName | null;
  t: number;            // 时间戳
  pitch?: number;       // 触发时的MIDI
  vel?: number;         // 力度
  dur?: number;         // 秒
  color?: string;
}

const grid: Cell[][] = makeGrid(20, 10);

// 当前情绪影响区（圆形/多边形）
const moodZones = { happy: {cx, cy, r}, ... };
```


# **9. 三人协作分工（刚好对标评分“执行”）**



| **角色代号**                                                          | **成员职责定位**                   | **主责范围（Primary）**                                                                                                                                                                                     | **次责支持（Secondary）**           |
| ----------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| ****Developer A（Tech Lead & Backend Owner）****                      | 技术方向、系统架构、后端开发负责人 | ��****Back-end / Python Owner**** ：• FastAPI 服务搭建• 情绪 → 乐理参数映射规则（核心业务逻辑）• API / WebSocket 设计与实现• 数据存储、导出、版本管理�� 技术质量负责人（代码规范、测试、CI）       | ✨ 支持前端联调、交互逻辑校验       |
| ****Developer B（Creative Interaction & Visual Experience Owner）**** | 用户体验、视觉交互、动画体验负责人 | ��****Interaction & Visual Layer Owner**** ：• 网格画布（Canvas）绘制与涂抹视觉效果• 表情头像、拖拽动效、情绪 UI 动态响应• 色彩系统、粒子、渐变、微动效、动效统一规范• GSAP / CSS 动效 & 可访问性体验 | �� 协助前端音效控制 UI 元素与控件 |
| ****Developer C（Audio Interaction & Frontend Integration Owner）**** | 声音、音乐逻辑、前端系统整合负责人 | ��****Audio & Frontend Integration Owner**** ：• Tone.js 声音引擎集成、音阶/节拍控制• 位置→音高逻辑实现、触发机制• 前后端联调（调用 Python API）• UI 控件（开始、清空、导出）功能逻辑                | �� 协助视觉演示与用户测试迭代     |


进度文档输出



| **成员**    | **可展示产出（老师能直接看到的）**                              |
| ------------- | ----------------------------------------------------------------- |
| Developer A | 后端 API 文档、数据结构、规则映射逻辑、测试报告、Increment Demo |
| Developer B | UI 组件、动效视频 Demo、画布交互 GIF、视觉规范文档              |
| Developer C | 视频 Demo（声音与网格互动）、前端代码、联调展示、音效参数面板   |


评分


| **Rubric 项目**  | **三人分工如何满足**                                            |
| ------------------ | ----------------------------------------------------------------- |
| **创意** 25%**** | B&C负责体验创新，A确保可实现性                                  |
| **代码** 50%**** | A主业务代码 + C主前端逻辑 + B主交互动画代码，每人均有可评分代码 |
| **执行** 25%**** | 责任明确，可分 Sprint 并逐步交付 Increment                      |



# 10 **最小可行版本**


头像+4 情绪 UI（表情图可先用占位）；

20×10 网格着色（仅 Happy 一套规则）

Tone.js 单声部钢琴 + “每 4 格一音”触发

Python /moods 和 /scale 返回配置（前端调用成功）

README + 一段 10 秒屏录 GIF

# **11. 可选加分**


多声部：主旋律 + 和弦铺底（Calm/Sad 适合）

回放：从 JSON 复现你的“情绪轨迹”

导出：把音符序列转成 MIDI 文件（Python mido 生成）

触觉：移动端轻震（Vibration API）


# **12. 小片段（前端触发伪代码** **）**

```python
// 假设 currentMood 已由鼠标靠近的情绪标签决定
const cfg = moodConfig[currentMood];   // 来自 /moods
const scale = await fetchScale(cfg.scale);

let stepCounter = 0;
function onCellEnter(x, y) {
  paintCell(x,y,currentMood);
  if (stepCounter % cfg.step === 0) {
    const pitch = xyToPitch(x,y,scale);  // X决定级数，Y决定八度
    const vel   = rand(cfg.vel[0], cfg.vel[1]) / 127;
    const dur   = gridDurFromLegato(cfg.legato, bpmToSec(cfg.bpm));
    piano.triggerAttackRelease(midiToFreq(pitch), dur, Tone.now(), vel);
  }
  stepCounter++;
}
```
