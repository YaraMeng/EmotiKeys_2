#!/usr/bin/env python3

"""

前端文件生成器 - 对角线四分区版

四个情绪区域呈对角线分布，固定尺寸1440*720px

"""

import os
from datetime import datetime
from pathlib import Path

class FrontendGenerator:
    def __init__(self, output_dir="."):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_html(self):
        """生成HTML文件"""
        html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>情绪音乐画布</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://unpkg.com/gsap@3.12.2/dist/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
</head>
<body>
    <div class="container">
        <!-- 情绪区域指示器 -->
        <div class="mood-region-indicator">
            <div class="region-label happy-region">😊 开心区域</div>
            <div class="region-label calm-region">😌 平和区域</div>
            <div class="region-label tense-region">😰 紧张区域</div>
            <div class="region-label sad-region">😔 伤心区域</div>
        </div>

        <!-- 中央头像 - 弹性拉动 -->
        <div class="avatar-container">
            <img id="avatar"
                 src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiByeD0iNjAiIGZpbGw9IiM0RUE5RjEiLz4KPGNpcmNsZSBjeD0iNjAiIGN5PSI0MCIgcj0iMTUiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTQ1IDgwIEEyMCAyMCA0IDAgMCA3NSA4MCIgc3Ryb2tlPSIjRkZGIiBzdHJva2Utd2lkdGg9IjQiLz4KPC9zdmc+"
                 alt="头像" class="avatar">
        </div>

        <!-- 网格画布 - 固定尺寸 -->
        <div class="canvas-container">
            <canvas id="gridCanvas" width="1440" height="720"></canvas>
        </div>

        <!-- 对角线边界（可视化） -->
        <div class="diagonal-boundaries">
            <div class="diagonal-boundary diagonal-1"></div>
            <div class="diagonal-boundary diagonal-2"></div>
        </div>

        <!-- 控件 -->
        <div class="controls">
            <button id="playPauseBtn" class="control-btn">开始探索</button>
            <button id="saveBtn" class="control-btn" disabled>保存音频</button>
        </div>

        <!-- 状态显示 -->
        <div class="status">
            <span id="currentMood">当前情绪: 等待探索</span>
            <span id="stepCounter">音符: 0</span>
            <span id="composingStatus">状态: 待开始</span>
            <span id="recordingStatus">录音: 未开始</span>
        </div>

        <!-- 隐藏的音频播放器 -->
        <audio id="audioPlayer" controls style="display: none;"></audio>
    </div>

    <script src="app.js"></script>
</body>
</html>'''
        
        with open(self.output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("✅ 生成 index.html 完成")

    def generate_css(self):
        """生成CSS文件"""
        css_content = '''/* 基础样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: auto;
}

.container {
    position: relative;
    width: 1440px;
    height: 720px;
    margin: 20px auto;
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* 情绪区域指示器 */
.mood-region-indicator {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 20px;
    z-index: 100;
    background: rgba(0, 0, 0, 0.4);
    padding: 10px 20px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.region-label {
    padding: 8px 16px;
    border-radius: 15px;
    font-size: 12px;
    font-weight: bold;
    opacity: 0.7;
    transition: all 0.3s ease;
}

.region-label.active {
    opacity: 1;
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.happy-region {
    background: linear-gradient(135deg, rgba(255,213,79,0.3), rgba(255,138,101,0.3));
    border: 1px solid #FFD54F;
}

.calm-region {
    background: linear-gradient(135deg, rgba(79,195,247,0.3), rgba(41,182,246,0.3));
    border: 1px solid #4FC3F7;
}

.tense-region {
    background: linear-gradient(135deg, rgba(244,67,54,0.3), rgba(211,47,47,0.3));
    border: 1px solid #F44336;
}

.sad-region {
    background: linear-gradient(135deg, rgba(92,107,192,0.3), rgba(63,81,181,0.3));
    border: 1px solid #5C6BC0;
}

/* 头像容器 - 弹性拉动 */
.avatar-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 90;
    cursor: grab;
    transition: transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    will-change: transform;
}

.avatar-container.dragging {
    cursor: grabbing;
    transition: none;
}

.avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 3px solid rgba(255, 255, 255, 0.8);
    transition: all 0.3s ease;
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    pointer-events: none;
}

.avatar-container.dragging .avatar {
    border-color: rgba(255, 255, 255, 1);
    filter: drop-shadow(0 12px 24px rgba(0,0,0,0.6));
    transform: scale(1.05);
}

/* 弹性拉动范围指示 */
.avatar-container::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200px;
    height: 200px;
    border: 2px dashed rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.avatar-container.dragging::before {
    opacity: 1;
}

/* 情绪特定样式 */
.avatar-container.happy .avatar {
    filter: hue-rotate(0deg) contrast(1.2) saturate(1.3) drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    border-color: #FFD54F;
}

.avatar-container.calm .avatar {
    filter: hue-rotate(180deg) brightness(1.1) saturate(1.1) drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    border-color: #4FC3F7;
}

.avatar-container.tense .avatar {
    filter: hue-rotate(300deg) contrast(1.3) saturate(1.4) drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    border-color: #F44336;
}

.avatar-container.sad .avatar {
    filter: hue-rotate(220deg) brightness(0.9) saturate(0.8) drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    border-color: #5C6BC0;
}

/* 紧张情绪的抖动动画 */
.avatar-container.tense .avatar {
    animation: tenseShake 0.5s ease-in-out infinite alternate;
}

@keyframes tenseShake {
    0% { transform: rotate(-1deg) scale(1.02); }
    100% { transform: rotate(1deg) scale(0.98); }
}

/* 画布容器 */
.canvas-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
}

/* 网格画布 - 固定尺寸 */
#gridCanvas {
    display: block;
    cursor: crosshair;
    background: rgba(0, 0, 0, 0.2);
}

/* 对角线边界 */
.diagonal-boundaries {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 50;
}

.diagonal-boundary {
    position: absolute;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    width: 2px;
    height: 150%;
}

.diagonal-1 {
    top: -25%;
    left: 50%;
    transform: translateX(-50%) rotate(45deg);
    transform-origin: center;
}

.diagonal-2 {
    top: -25%;
    left: 50%;
    transform: translateX(-50%) rotate(-45deg);
    transform-origin: center;
}

/* 网格高亮效果 */
.grid-highlight {
    position: absolute;
    pointer-events: none;
    z-index: 2;
    border-radius: 4px;
    transition: opacity 1.5s ease-out;
}

.grid-highlight.happy {
    background: radial-gradient(circle, rgba(255,213,79,0.8) 0%, rgba(255,213,79,0) 70%);
    box-shadow: 0 0 20px rgba(255,213,79,0.5);
}

.grid-highlight.calm {
    background: radial-gradient(circle, rgba(79,195,247,0.8) 0%, rgba(79,195,247,0) 70%);
    box-shadow: 0 0 20px rgba(79,195,247,0.5);
}

.grid-highlight.tense {
    background: radial-gradient(circle, rgba(244,67,54,0.8) 0%, rgba(244,67,54,0) 70%);
    box-shadow: 0 0 20px rgba(244,67,54,0.5);
}

.grid-highlight.sad {
    background: radial-gradient(circle, rgba(92,107,192,0.8) 0%, rgba(92,107,192,0) 70%);
    box-shadow: 0 0 20px rgba(92,107,192,0.5);
}

/* 控件 */
.controls {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 15px;
    z-index: 100;
}

.control-btn {
    padding: 12px 24px;
    background: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    font-weight: bold;
    min-width: 120px;
    font-size: 14px;
}

.control-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

.control-btn:active {
    transform: translateY(0);
}

.control-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.control-btn.playing {
    background: linear-gradient(135deg, #FF6B6B, #FF8E53);
    border-color: rgba(255, 255, 255, 0.6);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }
}

/* 状态显示 */
.status {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 30px;
    background: rgba(0, 0, 0, 0.4);
    padding: 12px 24px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 100;
}

.status span {
    font-size: 14px;
    font-weight: 500;
}

/* 保存动画 */
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}

.save-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #4CAF50, #45a049);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    z-index: 1000;
    font-size: 14px;
    font-weight: bold;
    backdrop-filter: blur(20px);
    animation: slideIn 0.3s ease;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.2);
}

/* 响应式设计 */
@media (max-width: 1480px) {
    body {
        padding: 10px;
    }
    
    .container {
        transform: scale(0.9);
        transform-origin: center;
    }
}

@media (max-width: 1320px) {
    .container {
        transform: scale(0.8);
    }
}

@media (max-width: 1160px) {
    .container {
        transform: scale(0.7);
    }
}

/* 加载动画 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.container {
    animation: fadeIn 0.8s ease;
}'''
        
        with open(self.output_dir / "styles.css", "w", encoding="utf-8") as f:
            f.write(css_content)
        print("✅ 生成 styles.css 完成")



    def generate_requirements(self):
        """生成requirements.txt"""
        requirements = '''# 前端生成器依赖
# 注意：这些是生成前端文件所需的Python依赖
# 实际前端运行在浏览器中，不需要Python环境

# 生成脚本依赖
python>=3.8
'''
        
        with open(self.output_dir / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements)
        print("✅ 生成 requirements.txt 完成")

    def generate_all(self):
        """生成所有文件"""
        # print("🎨 开始生成前端文件...")
        # self.generate_html()
        # self.generate_css()
        # self.generate_requirements()
        print("🎉 所有前端文件生成完成！")
        print("📁 文件保存在:", self.output_dir.absolute())
        print("\n🚀 使用方法:")
        print("1. 运行: python -m http.server 3000")
        print("2. 访问: http://192.168.124.17:8000/")
        print("3. 点击'开始探索'（会自动请求屏幕录制权限）")
        print("4. 弹性拖动中间的头像（有范围限制）")
        print("5. 在对角线四个区域移动鼠标体验不同情绪音乐:")
        print("   • 左上: 伤心区域 (蓝色) - A小调")
        print("   • 右上: 开心区域 (黄色) - C大调") 
        print("   • 左下: 紧张区域 (红色) - E小调")
        print("   • 右下: 平和区域 (青色) - G大调")
        print("6. 点击'停止探索'后点击'保存音频'下载WAV文件")

def main():
    generator = FrontendGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main()