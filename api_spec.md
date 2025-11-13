# API 规范（api_spec.md）

此文档定义后端对前端的 REST 与 WebSocket 合约（Sprint1 优先实现 /moods、/scale、session 与 notes 生成接口）。时间格式使用 ISO 8601 (UTC)。session_id 使用 UUID v4。

## 全局约定

- 时间：ISO 8601 UTC，例如 "2025-11-13T12:00:00.000Z"
- 坐标：x ∈ [0, grid_width-1], y ∈ [0, grid_height-1]
- intensity ∈ [0.0, 1.0]（超出裁剪）
- emotion 枚举：["happy","calm","tense","sad","excited"]（可扩展）
- 返回 JSON Content-Type: application/json

---

## 数据模型（简洁）

```json
Session
{
"session_id": "string (uuid)",
"created_at": "string (date-time)",
"grid_width": int,
"grid_height": int,
"meta": object
}

Cell
{
"x": int,
"y": int,
"emotion": string | null,
"intensity": number (0..1),
"timestamp": "string (date-time)"
}

SparseGridResponse
{
"session_id": string,
"grid_width": int,
"grid_height": int,
"cells": [ Cell, ... ],
"meta": object
}

NoteEvent
{
"at_time": "string (date-time)",
"pitch": int,        // MIDI pitch
"velocity": int,     // 0-127
"duration": number,  // seconds
"source_cell": Cell
}

EmotionStyle
{
"emotion": "happy|calm|tense|sad|excited",
"bpm": int,
"step": int,
"scale": "string",
"vel": [min,max],
"legato": number,
"palette": [ "#hex", ... ]
}

ErrorResponse
{
"error": "string",
"code": int,
"details": object|null
}
```


---

## 主要 REST 路由

1) GET /moods

- 描述：返回所有情绪的配置（EmotionStyle）。

```json
Response 200
{
"happy": { "bpm":115,"step":4,"scale":"C_ionian","vel":[80,100],"legato":0.9,"palette":["#FFD54F","#FF8A65"] },
"calm": { ... },
...
}
```

2) GET /scale?name={scale_name}

- 描述：返回 scale 对应的 MIDI 音级数组和建议八度范围。
- Query：name (required) 例如 "C_ionian"

  ```json
  Response 200
  {
  "name":"C_ionian",
  "notes":[60,62,64,65,67,69,71],
  "suggested_octaves":[3,4,5]
  }
  ```

3) POST /sessions

- 描述：创建 session。

  ```json
  - Request
    {
    "grid_width": 20,
    "grid_height": 10,
    "meta": { "user": "alice" } // 可选
    }
  - Response 201
    {
    "session_id":"d9f1b8c1-...",
    "created_at":"2025-11-13T12:00:00.000Z",
    "grid_width":20,
    "grid_height":10,
    "meta": {"user":"alice"}
    }
  ```

4) GET /sessions/{session_id}

- 描述：获取 session 当前状态（稀疏 cells 列表）。

  ```json
  Response 200 (SparseGridResponse)
  {
  "session_id":"...",
  "grid_width":20,
  "grid_height":10,
  "cells":[ {"x":1,"y":0,"emotion":"happy","intensity":0.8,"timestamp":"..."} ],
  "meta": {}
  }
  ```

5) POST /sessions/{session_id}/cells

- 描述：单点更新一个 cell（或回填最新状态）。

  ```json
  - Request
    {
    "x":3, "y":7, "emotion":"calm", "intensity":0.6, "timestamp":"2025-11-13T12:02:01.234Z"
    }
  - Response 200
    { "x":3,"y":7,"emotion":"calm","intensity":0.6,"timestamp":"..." }
  ```

6) POST /sessions/{session_id}/cells/batch

- 描述：批量写入，提高效率。

  ```json
  - Request
    { "events": [ Cell, Cell, ... ] }
  - Response 200
    { "updated": 3 }
  ```

7) POST /sessions/{session_id}/clear

- 描述：清空 session 的 grid。

  ```json
  Response 200
  { "cleared": true }
  ```

8) POST /generate-notes

- 描述：把 events（cell updates）映射成 note events（供前端播放或导出）。

  ```json
  - Request
    {
    "session_id":"...",
    "events":[ {"x":3,"y":7,"emotion":"calm","intensity":0.6,"timestamp":"..."}, ... ]
    }
  - Response 200
    {
    "notes":[ { "at_time":"...","pitch":60,"velocity":64,"duration":0.5,"source_cell":{...} }, ... ],
    "tempo": 90,
    "scale":"C-major"
    }
  ```

9) GET /sessions/{session_id}/export

- 描述：导出 session 为 JSON（包含 cells、events、emotion_styles snapshot）。

  ```json
  Response 200 (application/json attachment)
  { "session_id":"...","cells":[...],"events":[...],"emotion_styles":{...} }
  ```

---

## WebSocket（实时）— 可选骨架

- Endpoint: /ws/sessions/{session_id}
- 连接后 JSON 消息格式：

Client -> Server

- cell_update
  { "type":"cell_update", "payload": { Cell } }
- cells_batch
  { "type":"cells_batch", "payload": [ Cell, ... ] }
- ping
  { "type":"ping", "payload": { "ts":"..." } }

Server -> Client

- ack
  { "type":"ack", "payload": { "req_id":"...", "status":"ok" } }
- broadcast cell update
  { "type":"cell_update_broadcast", "payload": { Cell, "sender":"user-id" } }
- note events
  { "type":"note_events", "payload": { "notes":[ NoteEvent, ... ], "tempo":90, "scale":"C_ionian" } }

实现建议：

- 每条消息带 seq（sequence）和可选 req_id 用于 ack/重传。
- 初版仅实现回显/ack 与 note_events 生成功能；完整多实例 pub/sub 可在 Sprint2 使用 Redis。

---

## 校验与错误码

- 400 Bad Request：参数类型错误或坐标越界；示例：{ "error":"Bad Request","code":400,"details":{"x":"out of range 0..19"} }
- 404 Not Found：session 未找到
- 429 Too Many Requests：速率限制
- 500 Internal Server Error：服务器内部错误

坐标校验：

- 0 <= x < grid_width
- 0 <= y < grid_height
- intensity 自动裁剪到 [0.0,1.0] 或返回 400（根据团队偏好）

批量接口限制：

- 单次最大事件数建议 500（可配置）

并发冲突策略（简要）

- 默认：last-writer-wins（按服务器接收时间或 timestamp 排序）
- 若需要更复杂合并，需在合约中明确（如 intensity 累加等）

---

## 示例（PowerShell curl / Invoke-WebRequest）

获取 /moods：

```powershell
curl -Method Get -Uri http://127.0.0.1:8000/moods
```

创建 session：

```powershell
curl -Method Post -Uri http://127.0.0.1:8000/sessions -ContentType "application/json" -Body '{"grid_width":20,"grid_height":10}'
```

写入单点 cell（PowerShell）：

```powershell
curl -Method Post -Uri "http://127.0.0.1:8000/sessions/{session_id}/cells" -ContentType "application/json" -Body '{"x":3,"y":7,"emotion":"calm","intensity":0.6,"timestamp":"2025-11-13T12:02:01Z"}'
```

生成 notes：

```powershell
curl -Method Post -Uri http://127.0.0.1:8000/generate-notes -ContentType "application/json" -Body '{"session_id":"...","events":[{"x":3,"y":7,"emotion":"calm","intensity":0.6,"timestamp":"..."}]}'
```

---

## 交付与验收（Sprint1）

- 必交：`api_spec.md`（本文件），并在 FastAPI `/docs`（自动生成）中能看到相应模型（pydantic）。
- 必交：实现 /moods 与 /scale（只读 endpoint），并能返回文档中定义的示例数据。
- 优先交付：实现 POST /sessions、GET /sessions/{id} 与 POST /sessions/{id}/cells（最小内存实现可接受）。
- 验收标准：前端开发者能基于 /moods 和 /scale 开始实现 UI 与 Tone.js 的参数获取。

---

## 备注与扩展建议

- 推荐在 FastAPI 中使用 pydantic 模型逐条实现，上述 schema 可直接转成 pydantic class 并自动呈现在 /docs。
- WebSocket 初版仅做连接、ack 与 note_events 推送，避免 Sprint1 过多实时复杂度。
- 若要将此文件导出为 OpenAPI YAML，请告知，我可以把 paths/schemas 自动生成为 OpenAPI 草稿。

---

结束：上面就是 `api_spec.md` 的完整草案（已保存为文件）。
