# Backend (复制自 `app/`)

该目录包含后端（FastAPI）代码的备份/组织版本，便于在多人协作时明确后端位置。

建议使用方式（本地开发）

1. 进入仓库根目录
```powershell
cd "D:\PolyU\semester_1\SD5913 programming\EmotiKeys_2_myy\EmotiKeys_2"
```

2. 激活虚拟环境并安装依赖
```powershell
# 如果已有 .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. 运行服务
```powershell
python -m uvicorn backend.app.main:app --port 8000
```

4. 在浏览器打开 Swagger UI
http://127.0.0.1:8000/docs

说明
- 目前 `backend/app/` 是 `app/` 内容的复制版本（仅保存到工作区，未提交）。
- 若团队决定使用 `backend/` 作为标准后端目录，可将 `app/` 删除或归档，并在 README 中记录变更。

已进行的变更（记录）
- 2025-11-13: 仓库中的旧 `app/` 源代码已被移除；其内容已复制到 `backend/app/` 并替换为归档占位符以避免误用。
- 2025-11-13: 之前用于备份的 `archived_app/` 目录已被删除（本次操作）。如需保留历史，请确保远端或其他分支有备份。

注意: 这些更改仅保存在当前工作区，尚未创建或推送包含这些删除的 commit。建议在本地创建分支（例如 `chore/remove-old-app`）并将变更提交，然后打开 PR 供团队审阅与 CI 验证。