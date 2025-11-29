#!/usr/bin/env python3
"""
前端文件生成器 - 对角线区域版
四种情绪对应对角线划分的四个区域，鼠标滑过痕迹迅速消失
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
        
        <!-- 中央头像 -->
        <div class="avatar-container">
            <img id="avatar" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiByeD0iNjAiIGZpbGw9IiM0RUE5RjEiLz4KPGNpcmNsZSBjeD0iNjAiIGN5PSI0MCIgcj0iMTUiIGZpbGw9IiNGRkYiLz4KPHBhdGggZD0iTTQ1IDgwIEEyMCAyMCA0IDAgMCA3NSA4MCIgc3Ryb2tlPSIjRkZGIiBzdHJva2Utd2lkdGg9IjQiLz4KPC9zdmc+" 
                 alt="头像" class="avatar">
        </div>
        
        <!-- 网格画布 - 全屏 -->
        <canvas id="gridCanvas"></canvas>
        
        <!-- 对角线边界（可视化） -->
        <div class="diagonal-boundaries">
            <div class="diagonal-boundary diagonal-1"></div>
            <div class="diagonal-boundary diagonal-2"></div>
        </div>
        
        <!-- 控件 -->
        <div class="controls">
            <button id="playPauseBtn" class="control-btn">开始探索</button>
            <button id="saveBtn" class="control-btn">保存作品</button>
        </div>
        
        <!-- 状态显示 -->
        <div class="status">
            <span id="currentMood">当前情绪: 等待探索</span>
            <span id="stepCounter">音符: 0</span>
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
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white;
    min-height: 100vh;
    overflow: hidden;
}

.container {
    position: relative;
    width: 100vw;
    height: 100vh;
}

/* 情绪区域指示器 */
.mood-region-indicator {
    position: fixed;
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

/* 头像容器 */
.avatar-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 90;
    pointer-events: none;
}

.avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 3px solid rgba(255, 255, 255, 0.8);
    transition: all 0.3s ease;
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    pointer-events: auto;
}

.avatar.dragging {
    transform: translate(-50%, -50%) scale(1.1);
    border-color: rgba(255, 255, 255, 1);
}

/* 情绪特定样式 */
.avatar.happy { 
    filter: hue-rotate(0deg) contrast(1.2) saturate(1.3) drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    border-color: #FFD54F;
}
.avatar.calm { 
    filter: hue-rotate(180deg) brightness(1.1) saturate(1.1) drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    border-color: #4FC3F7;
}
.avatar.tense { 
    filter: hue-rotate(300deg) contrast(1.3) saturate(1.4) drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    border-color: #F44336;
    animation: tenseShake 0.5s ease-in-out infinite alternate;
}
.avatar.sad { 
    filter: hue-rotate(220deg) brightness(0.9) saturate(0.8) drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    border-color: #5C6BC0;
}

@keyframes tenseShake {
    0% { transform: translate(-50%, -50%) rotate(-1deg) scale(1.02); }
    100% { transform: translate(-50%, -50%) rotate(1deg) scale(0.98); }
}

/* 网格画布 - 全屏无边框 */
#gridCanvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: block;
    cursor: crosshair;
    z-index: 1;
}

/* 对角线边界 */
.diagonal-boundaries {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 50;
}

.diagonal-boundary {
    position: absolute;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
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

/* 鼠标悬停效果 - 短暂显示 */
.cell-hover {
    transition: all 0.3s ease;
    animation: fadeOut 0.5s ease-in-out forwards;
}

@keyframes fadeOut {
    0% {
        opacity: 1;
        transform: scale(1);
    }
    70% {
        opacity: 0.7;
        transform: scale(1.05);
    }
    100% {
        opacity: 0;
        transform: scale(1);
    }
}

.cell-hover.happy {
    background: radial-gradient(circle, rgba(255,213,79,0.8) 0%, rgba(255,213,79,0) 70%) !important;
}

.cell-hover.calm {
    background: radial-gradient(circle, rgba(79,195,247,0.8) 0%, rgba(79,195,247,0) 70%) !important;
}

.cell-hover.tense {
    background: radial-gradient(circle, rgba(244,67,54,0.8) 0%, rgba(244,67,54,0) 70%) !important;
}

.cell-hover.sad {
    background: radial-gradient(circle, rgba(92,107,192,0.8) 0%, rgba(92,107,192,0) 70%) !important;
}

/* 控件 */
.controls {
    position: fixed;
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

.control-btn:hover {
    background: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

.control-btn:active {
    transform: translateY(0);
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
    position: fixed;
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
@media (max-width: 768px) {
    .mood-region-indicator {
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }
    
    .region-label {
        padding: 6px 12px;
        font-size: 10px;
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
        padding: 10px 20px;
        font-size: 12px;
        min-width: 100px;
    }
    
    .status {
        flex-direction: column;
        gap: 8px;
        padding: 10px 20px;
        bottom: 70px;
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
        """生成JavaScript文件 - 对角线区域，痕迹迅速消失"""
        js_content = '''// 前端应用主逻辑 - 对角线区域，痕迹迅速消失
class EmotionCanvasApp {
    constructor() {
        this.canvas = document.getElementById('gridCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.avatar = document.getElementById('avatar');
        this.currentMoodDisplay = document.getElementById('currentMood');
        this.stepCounterDisplay = document.getElementById('stepCounter');
        this.composingStatusDisplay = document.getElementById('composingStatus');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        
        // 应用状态
        this.currentMood = null;
        this.isComposing = false;
        this.stepCounter = 0;
        this.sessionId = null;
        this.moodConfig = {};
        this.scales = {};
        this.activeHoverEffects = new Map(); // 存储活跃的悬停效果
        
        // 网格参数
        this.gridWidth = 20;
        this.gridHeight = 10;
        
        // 情绪区域定义（对角线划分）
        this.regions = {
            happy: (x, y) => x + y < 1,    // 左上到右下的对角线下方：开心
            calm: (x, y) => x + y >= 1 && x >= y,   // 左上到右下的对角线上方且x>=y：平和
            tense: (x, y) => x + y >= 1 && x < y,   // 左上到右下的对角线上方且x<y：紧张
            sad: (x, y) => x + y < 1 && x < y       // 左上到右下的对角线下方且x<y：伤心
        };
        
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
                step: 1,
                scale: "C_ionian", 
                vel: [80, 100], 
                legato: 0.9,
                chord: [0, 2, 4]
            },
            calm: { 
                bpm: 78, 
                step: 1,
                scale: "G_pentatonic", 
                vel: [55, 75], 
                legato: 1.2,
                chord: [0, 2, 4]
            },
            tense: { 
                bpm: 140, 
                step: 1,
                scale: "E_phrygian", 
                vel: [70, 95], 
                legato: 0.7,
                chord: [0, 1, 4]
            },
            sad: { 
                bpm: 88, 
                step: 1,
                scale: "A_aeolian", 
                vel: [50, 70], 
                legato: 0.95,
                chord: [0, 2, 3]
            }
        };
        
        // 扩展音阶范围，让音乐更丰富
        this.scales = {
            happy: { notes: [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79] },
            calm: { notes: [55, 57, 60, 62, 64, 67, 69, 72, 74, 76] },
            tense: { notes: [52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 68, 71] },
            sad: { notes: [57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76] }
        };
        
        this.sessionId = 'fallback-session-' + Date.now();
        console.log('🎵 使用降级配置成功');
    }
    
    setupEventListeners() {
        // 画布事件 - 鼠标移动时检测区域并自动播放音乐
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseleave', () => this.handleMouseLeave());
        
        // 触摸事件
        this.canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            this.handleMouseMove(e.touches[0]);
        });
        this.canvas.addEventListener('touchend', () => this.handleMouseLeave());
        
        // 控件事件
        this.playPauseBtn.addEventListener('click', () => this.toggleComposing());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveToLocal());
        
        // 窗口调整
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.drawGrid();
        });

        console.log('🎮 事件监听器设置完成');
    }
    
    getCurrentRegion(x, y) {
        // 将坐标转换为相对位置 (0-1)
        const relX = x / this.canvas.width;
        const relY = y / this.canvas.height;
        
        // 检测鼠标在哪个情绪区域
        for (const [mood, condition] of Object.entries(this.regions)) {
            if (condition(relX, relY)) {
                return mood;
            }
        }
        
        return null;
    }
    
    updateRegionIndicator(mood) {
        // 更新区域指示器的高亮状态
        document.querySelectorAll('.region-label').forEach(label => {
            label.classList.remove('active');
        });
        
        if (mood) {
            const activeLabel = document.querySelector(`.${mood}-region`);
            if (activeLabel) {
                activeLabel.classList.add('active');
            }
        }
    }
    
    setMood(mood) {
        if (this.currentMood === mood) return;
        
        this.currentMood = mood;
        this.currentMoodDisplay.textContent = `当前情绪: ${this.getMoodText(mood)}`;
        
        // 更新头像样式
        this.avatar.className = 'avatar ' + mood;
        
        // 更新区域指示器
        this.updateRegionIndicator(mood);
        
        console.log(`🎵 进入情绪区域: ${mood}`);
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
    
    toggleComposing() {
        if (!this.isComposing) {
            this.startComposing();
        } else {
            this.stopComposing();
        }
    }
    
    startComposing() {
        this.isComposing = true;
        Tone.Transport.start();
        
        this.playPauseBtn.textContent = '暂停探索';
        this.playPauseBtn.classList.add('playing');
        this.composingStatusDisplay.textContent = '状态: 探索中';
        
        console.log('🎵 开始探索 - 鼠标在不同对角线区域移动体验不同情绪音乐');
    }
    
    stopComposing() {
        this.isComposing = false;
        Tone.Transport.stop();
        
        this.playPauseBtn.textContent = '开始探索';
        this.playPauseBtn.classList.remove('playing');
        this.composingStatusDisplay.textContent = '状态: 已暂停';
        
        // 清除区域指示器高亮
        this.updateRegionIndicator(null);
        this.currentMoodDisplay.textContent = '当前情绪: 等待探索';
        
        console.log('⏸️ 暂停探索');
    }
    
    handleMouseMove(e) {
        if (!this.isComposing) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // 检测当前区域
        const currentRegion = this.getCurrentRegion(x, y);
        
        if (currentRegion && currentRegion !== this.currentMood) {
            this.setMood(currentRegion);
        }
        
        const cellX = Math.floor(x / (this.canvas.width / this.gridWidth));
        const cellY = Math.floor(y / (this.canvas.height / this.gridHeight));
        
        if (cellX >= 0 && cellX < this.gridWidth && cellY >= 0 && cellY < this.gridHeight) {
            // 显示短暂的悬停效果
            this.showHoverEffect(cellX, cellY);
            
            // 自动播放音乐
            if (this.currentMood) {
                this.triggerNote(cellX, cellY);
                this.sendCellToBackend(cellX, cellY);
            }
        }
    }
    
    handleMouseLeave() {
        // 鼠标离开画布时清除所有效果
        this.clearAllHoverEffects();
        this.updateRegionIndicator(null);
        this.currentMoodDisplay.textContent = '当前情绪: 等待探索';
    }
    
    showHoverEffect(x, y) {
        const cellKey = `${x},${y}`;
        
        // 如果这个格子已经有活跃的效果，先清除它
        if (this.activeHoverEffects.has(cellKey)) {
            clearTimeout(this.activeHoverEffects.get(cellKey));
        }
        
        const cellWidth = this.canvas.width / this.gridWidth;
        const cellHeight = this.canvas.height / this.gridHeight;
        
        if (!this.currentMood) return;
        
        const colors = {
            happy: 'rgba(255, 213, 79, 0.8)',
            calm: 'rgba(79, 195, 247, 0.8)',
            tense: 'rgba(244, 67, 54, 0.8)',
            sad: 'rgba(92, 107, 192, 0.8)'
        };
        
        const centerX = (x + 0.5) * cellWidth;
        const centerY = (y + 0.5) * cellHeight;
        const radius = Math.min(cellWidth, cellHeight) * 0.8;
        
        // 创建径向渐变
        const gradient = this.ctx.createRadialGradient(
            centerX, centerY, 0,
            centerX, centerY, radius
        );
        
        gradient.addColorStop(0, colors[this.currentMood]);
        gradient.addColorStop(0.7, colors[this.currentMood].replace('0.8', '0.3'));
        gradient.addColorStop(1, 'transparent');
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(
            centerX - radius, 
            centerY - radius, 
            radius * 2, 
            radius * 2
        );
        
        // 设置0.5秒后自动清除这个效果
        const timeoutId = setTimeout(() => {
            this.clearHoverEffect(x, y);
            this.activeHoverEffects.delete(cellKey);
        }, 500);
        
        this.activeHoverEffects.set(cellKey, timeoutId);
    }
    
    clearHoverEffect(x, y) {
        const cellWidth = this.canvas.width / this.gridWidth;
        const cellHeight = this.canvas.height / this.gridHeight;
        
        this.ctx.clearRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
        // 重新绘制网格线
        this.drawGridLines();
    }
    
    clearAllHoverEffects() {
        // 清除所有活跃的悬停效果
        for (const timeoutId of this.activeHoverEffects.values()) {
            clearTimeout(timeoutId);
        }
        this.activeHoverEffects.clear();
        
        // 重绘画布
        this.drawGrid();
    }
    
    async triggerNote(x, y) {
        if (!this.moodConfig[this.currentMood] || !this.isComposing) return;
        
        const cfg = this.moodConfig[this.currentMood];
        const scale = this.scales[this.currentMood];
        
        if (!scale || !scale.notes) return;
        
        // 步进计数
        this.stepCounter++;
        this.stepCounterDisplay.textContent = `音符: ${this.stepCounter}`;
        
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
            
            console.log(`🎵 ${this.getMoodText(this.currentMood)}区域 - 播放音符: pitch=${mainPitch}, vel=${velocity}`);
        }
    }
    
    addMusicalEffects(rootPitch, scale, cfg, duration, velocity) {
        // 根据情绪类型添加不同的音乐效果
        switch(this.currentMood) {
            case 'happy':
                if (Math.random() < 0.3) {
                    this.playChord(rootPitch, [0, 4, 7], duration, velocity * 0.6);
                }
                break;
            case 'calm':
                if (Math.random() < 0.2) {
                    this.playChord(rootPitch, [0, 7], duration, velocity * 0.4);
                }
                break;
            case 'tense':
                if (Math.random() < 0.4) {
                    this.playChord(rootPitch, [0, 1, 6], duration, velocity * 0.7);
                }
                break;
            case 'sad':
                if (Math.random() < 0.25) {
                    this.playChord(rootPitch, [0, 3, 7], duration, velocity * 0.5);
                }
                break;
        }
    }
    
    playChord(rootPitch, intervals, duration, velocity) {
        intervals.forEach(interval => {
            const chordPitch = rootPitch + interval;
            if (chordPitch <= 84) {
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
        const smoothX = Math.floor((x / this.gridWidth) * scale.length);
        const scaleIndex = Math.min(smoothX, scale.length - 1);
        const basePitch = scale[scaleIndex];
        
        const octaveOffset = Math.floor((1 - y / this.gridHeight) * 2) * 12;
        const finalPitch = basePitch + octaveOffset;
        
        return Math.max(48, Math.min(84, finalPitch));
    }
    
    mapIntensityToVelocity(intensity, velRange) {
        const [min, max] = velRange;
        const randomVariation = (Math.random() - 0.5) * 15;
        return Math.floor(min + intensity * (max - min) + randomVariation);
    }
    
    calculateNoteDuration(legato, bpm) {
        const beatDuration = 60.0 / bpm;
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
            
        } catch (error) {
            console.error('发送格子数据失败:', error);
        }
    }
    
    async saveToLocal() {
        if (this.stepCounter === 0) {
            alert('请先探索一些区域创作音乐再保存！');
            return;
        }
        
        const composition = {
            metadata: {
                title: '情绪音乐作品',
                sessionId: this.sessionId,
                timestamp: new Date().toISOString(),
                totalNotes: this.stepCounter,
                mood: this.currentMood || 'mixed'
            },
            moodConfig: this.moodConfig,
            musicalData: {
                scales: this.scales,
                bpm: this.currentMood ? this.moodConfig[this.currentMood].bpm : 100
            }
        };
        
        try {
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
            
            console.log('💾 作品已保存到本地');
            this.showSaveNotification();
            
        } catch (error) {
            console.error('保存失败:', error);
            alert('保存失败，请重试');
        }
    }
    
    formatDate(date) {
        return date.toISOString()
            .replace(/[:.]/g, '-')
            .replace('T', '_')
            .slice(0, 19);
    }
    
    showSaveNotification() {
        const existingNotification = document.querySelector('.save-notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        const notification = document.createElement('div');
        notification.className = 'save-notification';
        notification.textContent = '🎵 作品已保存到本地！';
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    drawGrid() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.drawGridLines();
    }
    
    drawGridLines() {
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
        print("3. 点击'开始探索' → 在对角线划分的不同区域移动鼠标")
        print("4. 体验不同情绪的音乐，痕迹会自动消失")
        print("\n🆕 新特性:")
        print("• 对角线划分四个情绪区域:")
        print("  - 左上到右下对角线下方: 开心")
        print("  - 左上到右下对角线上方且x>=y: 平和")
        print("  - 左上到右下对角线上方且x<y: 紧张") 
        print("  - 左上到右下对角线下方且x<y: 伤心")
        print("• 鼠标滑过痕迹0.5秒后自动消失")
        print("• 径向渐变悬停效果")

def main():
    generator = FrontendGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main()