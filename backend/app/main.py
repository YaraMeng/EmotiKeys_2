from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from .routes import moods, generate_notes, sessions

# 确定前端文件目录的路径
# 从 main.py -> app -> backend -> project_root -> head09_test
static_files_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "head09_test"))

app = FastAPI(title="EmotiKeys Backend (dev)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 路由
app.include_router(moods.router)
app.include_router(generate_notes.router)
app.include_router(sessions.router)

# 挂载静态文件目录
# 所有在 head09_test 目录下的文件都可以通过 / 路径访问
# 例如: /app.js, /styles.css, /assets/grid_happy.png
app.mount("/", StaticFiles(directory=static_files_dir, html=True), name="static")

# 这个根路由现在由 StaticFiles(html=True) 自动处理
# 当访问 "/" 时，它会自动寻找 index.html
# @app.get("/")
# async def root():
#     return FileResponse(os.path.join(static_files_dir, 'index.html'))
