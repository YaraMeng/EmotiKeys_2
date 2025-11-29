// 前端应用主逻辑

// API 基础地址（将其替换为运行后端的机器地址）
const API_BASE = 'http://192.168.124.7:8000';

function apiFetch(path, options = {}) {
    return fetch(`${API_BASE}${path}`, options);
}
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
            const moodsResponse = await apiFetch('/moods');
            this.moodConfig = await moodsResponse.json();
            console.log('情绪配置:', this.moodConfig);
            
            // 2. 获取音阶
            for (const mood in this.moodConfig) {
                const scaleName = this.moodConfig[mood].scale;
                const scaleResponse = await apiFetch(`/scale?name=${scaleName}`);
                this.scales[mood] = await scaleResponse.json();
            }
            console.log('音阶配置:', this.scales);
            
            // 3. 创建会话
            const sessionResponse = await apiFetch('/sessions', {
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
            
            const response = await apiFetch(`/sessions/${this.sessionId}/cells`, {
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
                await apiFetch(`/sessions/${this.sessionId}/clear`, {
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
});