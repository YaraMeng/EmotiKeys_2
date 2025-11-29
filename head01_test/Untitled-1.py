#!/usr/bin/env python3
"""
前端文件生成器
用Python生成所有前端文件：HTML、CSS、JS
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
        <!-- 情绪标签 -->
        <div class="mood-label happy-label" data-mood="happy">😊 开心</div>
        <div class="mood-label calm-label" data-mood="calm">😌 平和</div>
        <div class="mood-label tense-label" data-mood="tense">😰 紧张</div>
        <div class="mood-label sad-label" data-mood="sad">😔 伤心</div>
        
        <!-- 中央头像 -->
        <div class="avatar-container">
            <img id="avatar" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiByeD0iNjAiIGZpbGw9IiM0RUE5RjEiLz4KPGNpcmNsZSBjeD0iNjAiIGN5PSI0MCIgcj0iMTUiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTQ1IDgwIEEyMCAyMCAwIDAgMCA3NSA4MCIgc3Ryb2tlPSIjRkZGIiBzdHJva2Utd2lkdGg9IjQiLz4KPC9zdmc+" 
                 alt="头像" class="avatar">
        </div>
        
        <!-- 网格画布 -->
        <div class="canvas-container">
            <canvas id="gridCanvas"></canvas>
        </div>
        
        <!-- 控件 -->
        <div class="controls">
            <button id="startBtn" class="control-btn">开始谱曲</button>
            <button id="clearBtn" class="control-btn">清空</button>
            <button id="exportBtn" class="control-btn" disabled>导出</button>
        </div>
        
        <!-- 状态显示 -->
        <div class="status">
            <span id="currentMood">当前情绪: 未选择</span>
            <span id="stepCounter">步数: 0</span>
        </div>
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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    min-height: 100vh;
    overflow-x: hidden;
}

.container {
    position: relative;
    width: 100vw;
    height: 100vh;
    padding: 20px;
}

/* 情绪标签 */
.mood-label {
    position: absolute;
    padding: 12px 20px;
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    z-index: 10;
}

.mood-label:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}

.happy-label { top: 10%; left: 50%; transform: translateX(-50%); }
.calm-label { top: 50%; right: 5%; transform: translateY(-50%); }
.tense-label { bottom: 10%; left: 50%; transform: translateX(-50%); }
.sad-label { top: 50%; left: 5%; transform: translateY(-50%); }

/* 头像容器 */
.avatar-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 5;
}

.avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid rgba(255, 255, 255, 0.8);
    cursor: grab;
    transition: all 0.3s ease;
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.3));
}

.avatar:active {
    cursor: grabbing;
}

.avatar.dragging {
    transform: scale(1.1);
    border-color: rgba(255, 255, 255, 1);
}

/* 情绪特定样式 */
.avatar.happy { filter: hue-rotate(0deg) contrast(1.2); }
.avatar.calm { filter: hue-rotate(180deg) brightness(1.1); }
.avatar.tense { 
    filter: hue-rotate(300deg) contrast(1.3); 
    animation: tenseShake 0.5s ease-in-out infinite alternate;
}
.avatar.sad { filter: hue-rotate(220deg) brightness(0.9); }

@keyframes tenseShake {
    0% { transform: translate(-50%, -50%) rotate(-1deg); }
    100% { transform: translate(-50%, -50%) rotate(1deg); }
}

/* 画布容器 */
.canvas-container {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    max-width: 1000px;
    aspect-ratio: 16 / 9;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.1);
}

#gridCanvas {
    width: 100%;
    height: 100%;
    display: block;
    cursor: crosshair;
}

/* 控件 */
.controls {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 15px;
    z-index: 10;
}

.control-btn {
    padding: 12px 24px;
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.control-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}

.control-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* 状态显示 */
.status {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 30px;
    background: rgba(0, 0, 0, 0.3);
    padding: 10px 20px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

/* 刷子效果 */
.cell-highlight {
    transition: all 0.2s ease;
}

.cell-highlight.happy {
    background: radial-gradient(circle, #FFD54F 0%, #FF8A65 100%);
}

.cell-highlight.calm {
    background: radial-gradient(circle, #4FC3F7 0%, #29B6F6 100%);
}

.cell-highlight.tense {
    background: radial-gradient(circle, #F44336 0%, #D32F2F 100%);
}

.cell-highlight.sad {
    background: radial-gradient(circle, #5C6BC0 0%, #3F51B5 100%);
}

/* 响应式设计 */
@media (max-width: 768px) {
    .mood-label {
        padding: 8px 16px;
        font-size: 14px;
    }
    
    .avatar {
        width: 80px;
        height: 80px;
    }
    
    .controls {
        bottom: 10px;
    }
    
    .control-btn {
        padding: 8px 16px;
        font-size: 14px;
    }
}'''
        
        with open(self.output_dir / "styles.css", "w", encoding="utf-8") as f:
            f.write(css_content)
        print("✅ 生成 styles.css 完成")
    
    def generate_js(self):
        """生成JavaScript文件"""
        js_content = '''// 前端应用主逻辑
class EmotionCanvasApp {
    constructor() {
        this.canvas = document.getElementById('gridCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.avatar = document.getElementById('avatar');
        this.currentMoodDisplay = document.getElementById('currentMood');
        this.stepCounterDisplay = document.getElementById('stepCounter');
        
        // 应用状态
        this.currentMood = null;
        this.isDrawing = false;
        this.stepCounter = 0;
        this.sessionId = null;
        this.moodConfig = {};
        this.scales = {};
        
        // 网格参数
        this.gridWidth = 20;
        this.gridHeight = 10;
        this.cellStates = this.createEmptyGrid();
        
        // 音频
        this.synth = new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: 'sine' },
            envelope: { attack: 0.02, decay: 0.1, sustain: 0.3, release: 1 }
        }).toDestination();
        
        this.reverb = new Tone.Reverb(2).toDestination();
        this.synth.connect(this.reverb);
        
        this.init();
    }
    
    async init() {
        await this.initBackend();
        this.setupEventListeners();
        this.resizeCanvas();
        this.drawGrid();
        
        // 启动音频
        await Tone.start();
        console.log('音频上下文已启动');
    }
    
    async initBackend() {
        try {
            // 1. 获取情绪配置
            const moodsResponse = await fetch('/moods');
            this.moodConfig = await moodsResponse.json();
            console.log('情绪配置:', this.moodConfig);
            
            // 2. 获取音阶
            for (const mood in this.moodConfig) {
                const scaleName = this.moodConfig[mood].scale;
                const scaleResponse = await fetch(`/scale?name=${scaleName}`);
                this.scales[mood] = await scaleResponse.json();
            }
            console.log('音阶配置:', this.scales);
            
            // 3. 创建会话
            const sessionResponse = await fetch('/sessions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    grid_width: this.gridWidth,
                    grid_height: this.gridHeight
                })
            });
            const sessionData = await sessionResponse.json();
            this.sessionId = sessionData.session_id;
            console.log('会话ID:', this.sessionId);
            
        } catch (error) {
            console.error('初始化后端失败:', error);
            // 使用默认配置降级处理
            this.useFallbackConfig();
        }
    }
    
    useFallbackConfig() {
        // 降级配置
        this.moodConfig = {
            happy: { bpm: 115, step: 4, scale: "C_ionian", vel: [80,100], legato: 0.9 },
            calm: { bpm: 78, step: 6, scale: "G_pentatonic", vel: [55,75], legato: 1.2 },
            tense: { bpm: 140, step: 1, scale: "E_phrygian", vel: [70,95], legato: 0.5 },
            sad: { bpm: 88, step: 3, scale: "A_aeolian", vel: [50,70], legato: 0.95 }
        };
        
        this.scales = {
            happy: { notes: [60,62,64,65,67,69,71,72] },
            calm: { notes: [67,69,72,74,76] },
            tense: { notes: [64,65,67,69,70,72,74,75] },
            sad: { notes: [69,71,72,74,76,77,79,81] }
        };
        
        this.sessionId = 'fallback-session-' + Date.now();
    }
    
    setupEventListeners() {
        // 情绪标签事件
        document.querySelectorAll('.mood-label').forEach(label => {
            label.addEventListener('mouseenter', (e) => {
                const mood = e.target.dataset.mood;
                this.setMood(mood);
            });
        });
        
        // 头像拖拽
        this.setupAvatarDrag();
        
        // 画布事件
        this.canvas.addEventListener('mousedown', (e) => this.startDrawing(e));
        this.canvas.addEventListener('mousemove', (e) => this.draw(e));
        this.canvas.addEventListener('mouseup', () => this.stopDrawing());
        this.canvas.addEventListener('mouseleave', () => this.stopDrawing());
        
        // 触摸事件
        this.canvas.addEventListener('touchstart', (e) => this.startDrawing(e));
        this.canvas.addEventListener('touchmove', (e) => this.draw(e));
        this.canvas.addEventListener('touchend', () => this.stopDrawing());
        
        // 控件事件
        document.getElementById('startBtn').addEventListener('click', () => this.startComposing());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearCanvas());
        
        // 窗口调整
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.drawGrid();
        });
    }
    
    setupAvatarDrag() {
        let isDragging = false;
        let startX, startY;
        let avatarX = 0, avatarY = 0;
        
        const onMouseMove = (e) => {
            if (!isDragging) return;
            
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            
            // 限制拖拽范围
            const maxOffset = 20;
            avatarX = Math.max(-maxOffset, Math.min(maxOffset, dx));
            avatarY = Math.max(-maxOffset, Math.min(maxOffset, dy));
            
            // 应用GSAP平滑动画
            gsap.to(this.avatar, {
                x: avatarX,
                y: avatarY,
                duration: 0.1,
                ease: "power2.out"
            });
            
            this.updateMoodFromPosition(avatarX, avatarY);
        };
        
        const onMouseUp = () => {
            isDragging = false;
            this.avatar.classList.remove('dragging');
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
            
            // 平滑回到中心
            gsap.to(this.avatar, {
                x: 0,
                y: 0,
                duration: 0.5,
                ease: "elastic.out(1, 0.5)"
            });
        };
        
        this.avatar.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            this.avatar.classList.add('dragging');
            
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        });
    }
    
    updateMoodFromPosition(x, y) {
        // 根据位置计算最近的情绪
        const distances = {
            happy: Math.sqrt(Math.pow(x - 0, 2) + Math.pow(y + 50, 2)),
            calm: Math.sqrt(Math.pow(x - 50, 2) + Math.pow(y - 0, 2)),
            tense: Math.sqrt(Math.pow(x - 0, 2) + Math.pow(y - 50, 2)),
            sad: Math.sqrt(Math.pow(x + 50, 2) + Math.pow(y - 0, 2))
        };
        
        const closestMood = Object.keys(distances).reduce((a, b) => 
            distances[a] < distances[b] ? a : b
        );
        
        if (closestMood !== this.currentMood) {
            this.setMood(closestMood);
        }
    }
    
    setMood(mood) {
        if (this.currentMood === mood) return;
        
        this.currentMood = mood;
        this.currentMoodDisplay.textContent = `当前情绪: ${this.getMoodText(mood)}`;
        
        // 更新头像样式
        this.avatar.className = 'avatar ' + mood;
        
        // 更新光标
        this.canvas.style.cursor = 'crosshair';
        
        console.log(`切换到情绪: ${mood}`);
    }
    
    getMoodText(mood) {
        const texts = { happy: '开心', calm: '平和', tense: '紧张', sad: '伤心' };
        return texts[mood] || mood;
    }
    
    startComposing() {
        Tone.Transport.start();
        this.isDrawing = true;
        document.getElementById('startBtn').textContent = '谱曲中...';
        document.getElementById('startBtn').disabled = true;
    }
    
    startDrawing(e) {
        if (!this.currentMood || !this.isDrawing) return;
        
        this.isDrawing = true;
        this.draw(e);
    }
    
    stopDrawing() {
        this.isDrawing = false;
    }
    
    draw(e) {
        if (!this.isDrawing || !this.currentMood) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const cellX = Math.floor(x / (this.canvas.width / this.gridWidth));
        const cellY = Math.floor(y / (this.canvas.height / this.gridHeight));
        
        if (cellX >= 0 && cellX < this.gridWidth && cellY >= 0 && cellY < this.gridHeight) {
            this.paintCell(cellX, cellY);
            this.triggerNote(cellX, cellY);
            this.sendCellToBackend(cellX, cellY);
        }
    }
    
    paintCell(x, y) {
        const cellWidth = this.canvas.width / this.gridWidth;
        const cellHeight = this.canvas.height / this.gridHeight;
        
        // 主格子颜色
        const colors = {
            happy: '#FFD54F',
            calm: '#4FC3F7', 
            tense: '#F44336',
            sad: '#5C6BC0'
        };
        
        this.ctx.fillStyle = colors[this.currentMood];
        this.ctx.fillRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
        
        // 刷子扩散效果
        this.createBrushEffect(x, y, cellWidth, cellHeight);
        
        // 保存状态
        this.cellStates[y][x] = {
            mood: this.currentMood,
            timestamp: new Date().toISOString(),
            intensity: 1.0
        };
    }
    
    createBrushEffect(x, y, cellWidth, cellHeight) {
        const centerX = (x + 0.5) * cellWidth;
        const centerY = (y + 0.5) * cellHeight;
        const radius = cellWidth * 2;
        
        const gradient = this.ctx.createRadialGradient(
            centerX, centerY, 0,
            centerX, centerY, radius
        );
        
        const colorStops = {
            happy: ['rgba(255, 213, 79, 0.8)', 'rgba(255, 138, 101, 0)'],
            calm: ['rgba(79, 195, 247, 0.8)', 'rgba(41, 182, 246, 0)'],
            tense: ['rgba(244, 67, 54, 0.8)', 'rgba(211, 47, 47, 0)'],
            sad: ['rgba(92, 107, 192, 0.8)', 'rgba(63, 81, 181, 0)']
        };
        
        gradient.addColorStop(0, colorStops[this.currentMood][0]);
        gradient.addColorStop(1, colorStops[this.currentMood][1]);
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(centerX - radius, centerY - radius, radius * 2, radius * 2);
    }
    
    async triggerNote(x, y) {
        if (!this.moodConfig[this.currentMood]) return;
        
        const cfg = this.moodConfig[this.currentMood];
        const scale = this.scales[this.currentMood];
        
        if (!scale || !scale.notes) return;
        
        // 步进计数
        this.stepCounter++;
        this.stepCounterDisplay.textContent = `步数: ${this.stepCounter}`;
        
        // 检查是否触发音符
        if (this.stepCounter % cfg.step === 0) {
            const pitch = this.mapCellToPitch(x, y, scale.notes);
            const velocity = this.mapIntensityToVelocity(1.0, cfg.vel);
            const duration = this.calculateNoteDuration(cfg.legato, cfg.bpm);
            
            // 播放音符
            this.synth.triggerAttackRelease(
                Tone.Frequency(pitch, "midi").toFrequency(),
                duration,
                Tone.now(),
                velocity / 127
            );
            
            console.log(`播放音符: pitch=${pitch}, vel=${velocity}, dur=${duration}`);
        }
    }
    
    mapCellToPitch(x, y, scale) {
        // X轴映射到音阶索引
        const scaleIndex = Math.floor((x / this.gridWidth) * scale.length);
        const basePitch = scale[scaleIndex % scale.length];
        
        // Y轴影响八度偏移
        const octaveOffset = Math.floor((1 - y / this.gridHeight) * 2) * 12;
        
        return basePitch + octaveOffset;
    }
    
    mapIntensityToVelocity(intensity, velRange) {
        const [min, max] = velRange;
        return Math.floor(min + intensity * (max - min));
    }
    
    calculateNoteDuration(legato, bpm) {
        const beatDuration = 60.0 / bpm; // 每拍秒数
        return beatDuration * legato;
    }
    
    async sendCellToBackend(x, y) {
        if (!this.sessionId) return;
        
        try {
            const cellData = {
                x: x,
                y: y,
                emotion: this.currentMood,
                intensity: 1.0,
                timestamp: new Date().toISOString()
            };
            
            const response = await fetch(`/sessions/${this.sessionId}/cells`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(cellData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            console.log('发送格子数据成功:', cellData);
            
        } catch (error) {
            console.error('发送格子数据失败:', error);
        }
    }
    
    async clearCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.cellStates = this.createEmptyGrid();
        this.stepCounter = 0;
        this.stepCounterDisplay.textContent = '步数: 0';
        
        this.drawGrid();
        
        // 发送清空请求到后端
        if (this.sessionId) {
            try {
                await fetch(`/sessions/${this.sessionId}/clear`, {
                    method: 'POST'
                });
                console.log('清空画布数据');
            } catch (error) {
                console.error('清空请求失败:', error);
            }
        }
    }
    
    createEmptyGrid() {
        return Array(this.gridHeight).fill().map(() => 
            Array(this.gridWidth).fill(null)
        );
    }
    
    resizeCanvas() {
        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;
    }
    
    drawGrid() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // 绘制网格线
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.lineWidth = 1;
        
        const cellWidth = this.canvas.width / this.gridWidth;
        const cellHeight = this.canvas.height / this.gridHeight;
        
        for (let x = 0; x <= this.gridWidth; x++) {
            this.ctx.beginPath();
            this.ctx.moveTo(x * cellWidth, 0);
            this.ctx.lineTo(x * cellWidth, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= this.gridHeight; y++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y * cellHeight);
            this.ctx.lineTo(this.canvas.width, y * cellHeight);
            this.ctx.stroke();
        }
        
        // 重绘已有格子
        this.redrawCells();
    }
    
    redrawCells() {
        const cellWidth = this.canvas.width / this.gridWidth;
        const cellHeight = this.canvas.height / this.gridHeight;
        const colors = {
            happy: '#FFD54F',
            calm: '#4FC3F7',
            tense: '#F44336', 
            sad: '#5C6BC0'
        };
        
        for (let y = 0; y < this.gridHeight; y++) {
            for (let x = 0; x < this.gridWidth; x++) {
                const cell = this.cellStates[y][x];
                if (cell) {
                    this.ctx.fillStyle = colors[cell.mood];
                    this.ctx.fillRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
                }
            }
        }
    }
}

// 启动应用
document.addEventListener('DOMContentLoaded', () => {
    window.app = new EmotionCanvasApp();
});'''
        
        with open(self.output_dir / "app.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print("✅ 生成 app.js 完成")
    
    def generate_requirements(self):
        """生成requirements.txt"""
        requirements = '''# 前端生成器依赖
# 注意：这些是生成前端文件所需的Python依赖
# 实际前端运行在浏览器中，不需要Python环境
        
# 生成脚本依赖
python>=3.8
        
# 如果你想要一个简单的HTTP服务器来测试
# pip install http-server-python
'''
        
        with open(self.output_dir / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements)
        print("✅ 生成 requirements.txt 完成")
    
    def generate_all(self):
        """生成所有文件"""
        print("🎨 开始生成前端文件...")
        self.generate_html()
        self.generate_css() 
        self.generate_js()
        self.generate_requirements()
        print("🎉 所有前端文件生成完成！")
        print("📁 文件保存在:", self.output_dir.absolute())
        print("\\n🚀 使用方法:")
        print("1. 确保后端服务运行在 http://localhost:8000")
        print("2. 用浏览器打开 index.html")
        print("3. 或者运行: python -m http.server 3000")
        print("4. 访问 http://localhost:3000")

def main():
    generator = FrontendGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main()