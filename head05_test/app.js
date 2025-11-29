// 前端应用主逻辑 - 对角线区域，痕迹迅速消失
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
        const p = this.mapClientToDesign(e.clientX, e.clientY);
        const x = p.x;
        const y = p.y;
        
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

    mapClientToDesign(clientX, clientY) {
        const scale = window.__HK_SCALE || 1;
        const appEl = document.querySelector('.hk-app');
        if (appEl) {
            const rect = appEl.getBoundingClientRect();
            return { x: (clientX - rect.left) / scale, y: (clientY - rect.top) / scale };
        }
        const rect = this.canvas.getBoundingClientRect();
        return { x: clientX - rect.left, y: clientY - rect.top };
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
});