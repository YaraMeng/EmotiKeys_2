#!/usr/bin/env python3
"""
前端文件生成器 - 修改版
优化音乐效果，添加保存功能
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
            <button id="exportBtn" class="control-btn">保存作品</button>
        </div>
        
        <!-- 状态显示 -->
        <div class="status">
            <span id="currentMood">当前情绪: 未选择</span>
            <span id="stepCounter">步数: 0</span>
            <span id="composingStatus">状态: 待开始</span>
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
    font-weight: bold;
}

.mood-label:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.happy-label { 
    top: 10%; 
    left: 50%; 
    transform: translateX(-50%);
    background: linear-gradient(135deg, rgba(255,213,79,0.3), rgba(255,138,101,0.3));
}
.calm-label { 
    top: 50%; 
    right: 5%; 
    transform: translateY(-50%);
    background: linear-gradient(135deg, rgba(79,195,247,0.3), rgba(41,182,246,0.3));
}
.tense-label { 
    bottom: 10%; 
    left: 50%; 
    transform: translateX(-50%);
    background: linear-gradient(135deg, rgba(244,67,54,0.3), rgba(211,47,47,0.3));
}
.sad-label { 
    top: 50%; 
    left: 5%; 
    transform: translateY(-50%);
    background: linear-gradient(135deg, rgba(92,107,192,0.3), rgba(63,81,181,0.3));
}

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
.avatar.happy { 
    filter: hue-rotate(0deg) contrast(1.2) saturate(1.3);
    border-color: #FFD54F;
}
.avatar.calm { 
    filter: hue-rotate(180deg) brightness(1.1) saturate(1.1);
    border-color: #4FC3F7;
}
.avatar.tense { 
    filter: hue-rotate(300deg) contrast(1.3) saturate(1.4);
    border-color: #F44336;
    animation: tenseShake 0.5s ease-in-out infinite alternate;
}
.avatar.sad { 
    filter: hue-rotate(220deg) brightness(0.9) saturate(0.8);
    border-color: #5C6BC0;
}

@keyframes tenseShake {
    0% { transform: translate(-50%, -50%) rotate(-1deg) scale(1.02); }
    100% { transform: translate(-50%, -50%) rotate(1deg) scale(0.98); }
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
    backdrop-filter: blur(5px);
}

#gridCanvas {
    width: 100%;
    height: 100%;
    display: block;
    cursor: crosshair;
    transition: cursor 0.3s ease;
}

#gridCanvas.composing {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="%23FFD54F" stroke="%23FFFFFF" stroke-width="2"/></svg>') 12 12, crosshair;
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
    font-weight: bold;
    min-width: 120px;
}

.control-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.control-btn:active {
    transform: translateY(0);
}

.control-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.control-btn.composing {
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
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 30px;
    background: rgba(0, 0, 0, 0.3);
    padding: 12px 24px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.status span {
    font-size: 14px;
    font-weight: 500;
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
@media (max-width: 768px) {
    .mood-label {
        padding: 8px 16px;
        font-size: 12px;
    }
    
    .avatar {
        width: 80px;
        height: 80px;
    }
    
    .controls {
        bottom: 10px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .control-btn {
        padding: 8px 16px;
        font-size: 12px;
        min-width: 100px;
    }
    
    .status {
        flex-direction: column;
        gap: 8px;
        padding: 8px 16px;
    }
    
    .status span {
        font-size: 12px;
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
    
    def generate_js(self):
        """生成JavaScript文件 - 优化音乐和保存功能"""
        js_content = '''// 前端应用主逻辑 - 优化版
class EmotionCanvasApp {
    constructor() {
        this.canvas = document.getElementById('gridCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.avatar = document.getElementById('avatar');
        this.currentMoodDisplay = document.getElementById('currentMood');
        this.stepCounterDisplay = document.getElementById('stepCounter');
        this.composingStatusDisplay = document.getElementById('composingStatus');
        
        // 应用状态
        this.currentMood = null;
        this.isDrawing = false;
        this.stepCounter = 0;
        this.sessionId = null;
        this.moodConfig = {};
        this.scales = {};
        this.isComposing = false;
        
        // 网格参数
        this.gridWidth = 20;
        this.gridHeight = 10;
        this.cellStates = this.createEmptyGrid();
        
        // 初始化音频
        this.initAudio();
        
        this.init();
    }
    
    initAudio() {
        // 使用更真实的钢琴音色
        this.synth = new Tone.PolySynth(Tone.Synth, {
            oscillator: {
                type: "triangle"
            },
            envelope: {
                attack: 0.005,
                decay: 0.1,
                sustain: 0.3,
                release: 1.2
            }
        }).toDestination();

        // 添加效果
        this.reverb = new Tone.Reverb({
            decay: 2.5,
            wet: 0.2
        }).toDestination();
        
        this.synth.connect(this.reverb);

        console.log('🎹 音频系统初始化完成');
    }
    
    async init() {
        await this.initBackend();
        this.setupEventListeners();
        this.resizeCanvas();
        this.drawGrid();
        
        // 启动音频
        await Tone.start();
        console.log('🎵 音频上下文已启动');
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
            console.error('初始化后端失败，使用降级配置:', error);
            // 使用默认配置降级处理
            this.useFallbackConfig();
        }
    }
    
    useFallbackConfig() {
        // 更音乐化的降级配置
        this.moodConfig = {
            happy: { 
                bpm: 115, 
                step: 4, 
                scale: "C_ionian", 
                vel: [80, 100], 
                legato: 0.9,
                chord: [0, 2, 4] // 大三和弦
            },
            calm: { 
                bpm: 78, 
                step: 6, 
                scale: "G_pentatonic", 
                vel: [55, 75], 
                legato: 1.2,
                chord: [0, 2, 4] // 大三和弦
            },
            tense: { 
                bpm: 140, 
                step: 2,  // 改为2步一音，避免太密集
                scale: "E_phrygian", 
                vel: [70, 95], 
                legato: 0.7,
                chord: [0, 1, 4] // 小调和弦
            },
            sad: { 
                bpm: 88, 
                step: 3, 
                scale: "A_aeolian", 
                vel: [50, 70], 
                legato: 0.95,
                chord: [0, 2, 3] // 小三和弦
            }
        };
        
        // 扩展音阶范围，让音乐更丰富
        this.scales = {
            happy: { notes: [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79] }, // 2个八度C大调
            calm: { notes: [55, 57, 60, 62, 64, 67, 69, 72, 74, 76] }, // G大调五声
            tense: { notes: [52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 68, 71] }, // E弗里吉亚
            sad: { notes: [57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76] } // A小调
        };
        
        this.sessionId = 'fallback-session-' + Date.now();
        console.log('🎵 使用降级配置成功');
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
        this.canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startDrawing(e.touches[0]);
        });
        this.canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            this.draw(e.touches[0]);
        });
        this.canvas.addEventListener('touchend', () => this.stopDrawing());
        
        // 控件事件
        document.getElementById('startBtn').addEventListener('click', () => this.startComposing());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearCanvas());
        document.getElementById('exportBtn').addEventListener('click', () => this.saveToLocal());
        
        // 窗口调整
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.drawGrid();
        });

        console.log('🎮 事件监听器设置完成');
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
        
        console.log(`🎵 切换到情绪: ${mood}`);
    }
    
    getMoodText(mood) {
        const texts = { 
            happy: '开心', 
            calm: '平和', 
            tense: '紧张', 
            sad: '伤心' 
        };
        return texts[mood] || mood;
    }
    
    startComposing() {
        if (!this.currentMood) {
            alert('请先选择一种情绪！');
            return;
        }

        if (!this.isComposing) {
            this.isComposing = true;
            Tone.Transport.start();
            
            const startBtn = document.getElementById('startBtn');
            startBtn.textContent = '停止谱曲';
            startBtn.classList.add('composing');
            
            this.canvas.classList.add('composing');
            this.composingStatusDisplay.textContent = '状态: 谱曲中';
            
            console.log('🎵 开始谱曲');
        } else {
            this.stopComposing();
        }
    }
    
    stopComposing() {
        this.isComposing = false;
        Tone.Transport.stop();
        
        const startBtn = document.getElementById('startBtn');
        startBtn.textContent = '开始谱曲';
        startBtn.classList.remove('composing');
        
        this.canvas.classList.remove('composing');
        this.composingStatusDisplay.textContent = '状态: 已停止';
        
        console.log('🛑 停止谱曲');
    }
    
    startDrawing(e) {
        if (!this.currentMood || !this.isComposing) {
            if (!this.isComposing) {
                alert('请先点击"开始谱曲"！');
            }
            return;
        }
        
        this.isDrawing = true;
        this.draw(e);
    }
    
    stopDrawing() {
        this.isDrawing = false;
    }
    
    draw(e) {
        if (!this.isDrawing || !this.currentMood || !this.isComposing) return;
        
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
        if (!this.moodConfig[this.currentMood] || !this.isComposing) return;
        
        const cfg = this.moodConfig[this.currentMood];
        const scale = this.scales[this.currentMood];
        
        if (!scale || !scale.notes) return;
        
        // 步进计数
        this.stepCounter++;
        this.stepCounterDisplay.textContent = `步数: ${this.stepCounter}`;
        
        // 检查是否触发音符
        if (this.stepCounter % cfg.step === 0) {
            // 主旋律音符
            const mainPitch = this.mapCellToPitch(x, y, scale.notes);
            const velocity = this.mapIntensityToVelocity(1.0, cfg.vel);
            const duration = this.calculateNoteDuration(cfg.legato, cfg.bpm);
            
            // 播放主音符
            this.synth.triggerAttackRelease(
                Tone.Frequency(mainPitch, "midi").toFrequency(),
                duration,
                Tone.now(),
                velocity / 127
            );
            
            // 根据情绪添加不同的音乐效果
            this.addMusicalEffects(mainPitch, scale.notes, cfg, duration, velocity);
            
            console.log(`🎵 播放音符: pitch=${mainPitch}, vel=${velocity}, dur=${duration.toFixed(3)}s`);
        }
    }
    
    addMusicalEffects(rootPitch, scale, cfg, duration, velocity) {
        // 根据情绪类型添加不同的音乐效果
        switch(this.currentMood) {
            case 'happy':
                // 快乐情绪：添加大三和弦
                if (Math.random() < 0.4) {
                    this.playChord(rootPitch, [0, 4, 7], duration, velocity * 0.6);
                }
                break;
                
            case 'calm':
                // 平静情绪：添加五度和弦
                if (Math.random() < 0.3) {
                    this.playChord(rootPitch, [0, 7], duration, velocity * 0.4);
                }
                break;
                
            case 'tense':
                // 紧张情绪：添加不和谐音
                if (Math.random() < 0.5) {
                    this.playChord(rootPitch, [0, 1, 6], duration, velocity * 0.7);
                }
                break;
                
            case 'sad':
                // 悲伤情绪：添加小三和弦
                if (Math.random() < 0.35) {
                    this.playChord(rootPitch, [0, 3, 7], duration, velocity * 0.5);
                }
                break;
        }
    }
    
    playChord(rootPitch, intervals, duration, velocity) {
        intervals.forEach(interval => {
            const chordPitch = rootPitch + interval;
            if (chordPitch <= 84) { // 限制最高音
                // 和弦音符稍微延迟一点，产生更丰富的效果
                const chordTime = Tone.now() + 0.02;
                this.synth.triggerAttackRelease(
                    Tone.Frequency(chordPitch, "midi").toFrequency(),
                    duration * 0.6,
                    chordTime,
                    velocity / 127
                );
            }
        });
    }
    
    mapCellToPitch(x, y, scale) {
        // X轴映射到音阶索引，使用平滑映射
        const smoothX = Math.floor((x / this.gridWidth) * scale.length);
        const scaleIndex = Math.min(smoothX, scale.length - 1);
        const basePitch = scale[scaleIndex];
        
        // Y轴影响八度偏移，但限制在合理范围内
        const octaveOffset = Math.floor((1 - y / this.gridHeight) * 2) * 12;
        const finalPitch = basePitch + octaveOffset;
        
        // 限制音高在合理的钢琴范围内 (48-84)
        return Math.max(48, Math.min(84, finalPitch));
    }
    
    mapIntensityToVelocity(intensity, velRange) {
        const [min, max] = velRange;
        // 添加随机变化，让力度更自然
        const randomVariation = (Math.random() - 0.5) * 15;
        return Math.floor(min + intensity * (max - min) + randomVariation);
    }
    
    calculateNoteDuration(legato, bpm) {
        const beatDuration = 60.0 / bpm;
        // 添加微小随机变化，让节奏更自然
        const randomVariation = 1 + (Math.random() - 0.5) * 0.1;
        return beatDuration * legato * randomVariation;
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
            
            console.log('📡 发送格子数据成功:', cellData);
            
        } catch (error) {
            console.error('发送格子数据失败:', error);
        }
    }
    
    async saveToLocal() {
        if (!this.isComposing && this.stepCounter === 0) {
            alert('请先创作一些音乐再保存！');
            return;
        }
        
        if (this.isComposing) {
            this.stopComposing();
        }
        
        const composition = {
            metadata: {
                title: '情绪音乐作品',
                sessionId: this.sessionId,
                timestamp: new Date().toISOString(),
                duration: Math.floor(this.stepCounter * 0.3), // 估算时长（秒）
                totalSteps: this.stepCounter,
                mood: this.currentMood || 'mixed'
            },
            moodConfig: this.moodConfig,
            grid: {
                width: this.gridWidth,
                height: this.gridHeight,
                cells: this.getActiveCells()
            },
            musicalData: {
                scales: this.scales,
                bpm: this.currentMood ? this.moodConfig[this.currentMood].bpm : 100
            }
        };
        
        try {
            // 创建Blob并下载
            const blob = new Blob([JSON.stringify(composition, null, 2)], {
                type: 'application/json'
            });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `情绪音乐作品_${this.formatDate(new Date())}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            console.log('💾 作品已保存到本地', composition);
            this.showSaveNotification();
            
        } catch (error) {
            console.error('保存失败:', error);
            alert('保存失败，请重试');
        }
    }
    
    getActiveCells() {
        const activeCells = [];
        for (let y = 0; y < this.gridHeight; y++) {
            for (let x = 0; x < this.gridWidth; x++) {
                if (this.cellStates[y][x]) {
                    activeCells.push({
                        x: x,
                        y: y,
                        ...this.cellStates[y][x]
                    });
                }
            }
        }
        return activeCells;
    }
    
    formatDate(date) {
        return date.toISOString()
            .replace(/[:.]/g, '-')
            .replace('T', '_')
            .slice(0, 19);
    }
    
    showSaveNotification() {
        // 移除现有的通知
        const existingNotification = document.querySelector('.save-notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        const notification = document.createElement('div');
        notification.className = 'save-notification';
        notification.textContent = '🎵 作品已保存到本地！';
        
        document.body.appendChild(notification);
        
        // 3秒后自动移除
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    async clearCanvas() {
        if (this.isComposing) {
            this.stopComposing();
        }
        
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.cellStates = this.createEmptyGrid();
        this.stepCounter = 0;
        this.stepCounterDisplay.textContent = '步数: 0';
        this.composingStatusDisplay.textContent = '状态: 已清空';
        
        this.drawGrid();
        
        console.log('🗑️ 画布已清空');
        
        // 发送清空请求到后端（如果连接）
        if (this.sessionId) {
            try {
                await fetch(`/sessions/${this.sessionId}/clear`, {
                    method: 'POST'
                });
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
    try {
        window.app = new EmotionCanvasApp();
        console.log('🎉 情绪音乐画布应用启动成功！');
    } catch (error) {
        console.error('应用启动失败:', error);
        alert('应用启动失败，请刷新页面重试');
    }
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
        print("\n🚀 使用方法:")
        print("1. 运行: python -m http.server 3000")
        print("2. 访问: http://localhost:3000")
        print("3. 选择情绪 → 点击'开始谱曲' → 在网格上拖动创作音乐")
        print("4. 点击'保存作品'将创作保存为JSON文件")
        print("\n🎵 新功能:")
        print("• 更好听的钢琴音色和和弦效果")
        print("• 开始/停止谱曲控制")
        print("• 本地保存作品功能")
        print("• 更美观的界面和动画")

def main():
    generator = FrontendGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main()