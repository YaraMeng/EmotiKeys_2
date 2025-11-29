// 前端应用主逻辑 - 修复四个区域划分
class EmotionCanvasApp {
    constructor() {
        this.canvas = document.getElementById('gridCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.avatarContainer = document.querySelector('.avatar-container');
        this.avatar = document.getElementById('avatar');
        this.currentMoodDisplay = document.getElementById('currentMood');
        this.stepCounterDisplay = document.getElementById('stepCounter');
        this.composingStatusDisplay = document.getElementById('composingStatus');
        this.recordingStatusDisplay = document.getElementById('recordingStatus');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.saveBtn = document.getElementById('saveBtn');
        this.audioPlayer = document.getElementById('audioPlayer');
        
        // 应用状态
        this.currentMood = null;
        this.isComposing = false;
        this.isRecording = false;
        this.stepCounter = 0;
        this.sessionId = null;
        this.moodConfig = {};
        this.scales = {};
        this.activeHighlights = new Map();
        this.recorder = null;
        this.audioChunks = [];
        this.recordedAudio = null;
        
        // 头像弹性拉动状态
        this.isDragging = false;
        this.dragStartX = 0;
        this.dragStartY = 0;
        this.avatarOffsetX = 0;
        this.avatarOffsetY = 0;
        this.maxPullDistance = 100; // 最大拉动距离
        
        // 网格参数
        this.gridWidth = 20;
        this.gridHeight = 10;
        
        // 修复的情绪区域定义 - 正确划分四个区域
        this.regions = {
            // 右上区域：开心
            happy: (x, y) => x > 0.5 && y < 0.5,
            // 右下区域：平和
            calm: (x, y) => x > 0.5 && y > 0.5,
            // 左下区域：紧张
            tense: (x, y) => x < 0.5 && y > 0.5,
            // 左上区域：伤心
            sad: (x, y) => x < 0.5 && y < 0.5
        };
        
        // 初始化音频
        this.initAudio();
        
        this.init();
    }
    
    initAudio() {
        // 使用更真实的钢琴音色
        this.synth = new Tone.PolySynth({
            maxPolyphony: 32,
            voice: Tone.Synth,
            options: {
                oscillator: {
                    type: "triangle8"
                },
                envelope: {
                    attack: 0.005,
                    decay: 0.1,
                    sustain: 0.3,
                    release: 1.2
                },
                filter: {
                    Q: 8,
                    frequency: 1200,
                    type: "lowpass"
                }
            }
        });
        
        // 创建效果链
        this.reverb = new Tone.Reverb({
            decay: 2.8,
            wet: 0.25
        });
        
        this.delay = new Tone.FeedbackDelay({
            delayTime: 0.15,
            feedback: 0.4,
            wet: 0.1
        });
        
        this.compressor = new Tone.Compressor({
            threshold: -24,
            ratio: 4,
            attack: 0.003,
            release: 0.25
        });
        
        this.eq = new Tone.EQ3({
            low: -2,
            mid: 0,
            high: 2
        });
        
        // 连接效果链
        this.synth.chain(
            this.compressor,
            this.eq,
            this.delay,
            this.reverb,
            Tone.Destination
        );
        
        console.log('🎹 高级钢琴音色初始化完成');
    }
    
    async initRecorder() {
        try {
            // 尝试获取屏幕音频流（需要浏览器支持）
            if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
                throw new Error('浏览器不支持屏幕录制');
            }
            
            // 获取屏幕共享流（包含音频）
            const stream = await navigator.mediaDevices.getDisplayMedia({
                video: true,
                audio: {
                    echoCancellation: false,
                    noiseSuppression: false,
                    autoGainControl: false,
                    sampleRate: 44100,
                    channelCount: 2
                }
            });
            
            // 创建音频上下文来处理音频
            const audioContext = new AudioContext();
            const source = audioContext.createMediaStreamSource(stream);
            const destination = audioContext.createMediaStreamDestination();
            
            // 连接音频节点
            source.connect(destination);
            
            // 创建录音器
            this.recorder = new MediaRecorder(destination.stream);
            this.recorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            this.recorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                this.recordedAudio = audioBlob;
                this.audioPlayer.src = URL.createObjectURL(audioBlob);
                this.saveBtn.disabled = false;
                
                // 停止所有音轨
                stream.getTracks().forEach(track => track.stop());
                console.log('🎙️ 屏幕录音完成');
            };
            
            return true;
            
        } catch (error) {
            console.error('无法访问屏幕音频:', error);
            
            // 降级方案：使用系统音频（需要用户授权）
            try {
                const fallbackStream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        echoCancellation: false,
                        noiseSuppression: false,
                        autoGainControl: false,
                        sampleRate: 44100,
                        channelCount: 2
                    } 
                });
                
                this.recorder = new MediaRecorder(fallbackStream);
                this.recorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        this.audioChunks.push(event.data);
                    }
                };
                
                this.recorder.onstop = () => {
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                    this.recordedAudio = audioBlob;
                    this.audioPlayer.src = URL.createObjectURL(audioBlob);
                    this.saveBtn.disabled = false;
                    console.log('🎙️ 系统音频录音完成');
                };
                
                return true;
                
            } catch (fallbackError) {
                console.error('也无法访问系统音频:', fallbackError);
                alert('无法访问音频输入设备，录音功能不可用');
                return false;
            }
        }
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
            const moodsResponse = await apiFetch('/moods');
            this.moodConfig = await moodsResponse.json();
            console.log('情绪配置:', this.moodConfig);
            
            for (const mood in this.moodConfig) {
                const scaleName = this.moodConfig[mood].scale;
                const scaleResponse = await apiFetch(`/scale?name=${scaleName}`);
                this.scales[mood] = await scaleResponse.json();
            }
            
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
            
        } catch (error) {
            console.error('初始化后端失败，使用降级配置:', error);
            this.useFallbackConfig();
        }
    }
    
    useFallbackConfig() {
        // 优化的音乐配置
        this.moodConfig = {
            happy: { 
                bpm: 120, 
                step: 1,
                scale: "C_major", 
                vel: [70, 85], 
                legato: 0.7
            },
            calm: { 
                bpm: 80, 
                step: 2,
                scale: "G_major", 
                vel: [50, 65], 
                legato: 1.2
            },
            tense: { 
                bpm: 100, 
                step: 1,
                scale: "E_minor", 
                vel: [60, 75], 
                legato: 0.5
            },
            sad: { 
                bpm: 70, 
                step: 2,
                scale: "A_minor", 
                vel: [45, 60], 
                legato: 1.0
            }
        };
        
        // 和谐的音阶定义
        this.scales = {
            happy: { 
                notes: [60, 62, 64, 65, 67, 69, 71, 72], // C大调
                type: "major"
            },
            calm: { 
                notes: [55, 57, 59, 60, 62, 64, 66, 67], // G大调
                type: "major"
            },
            tense: { 
                notes: [52, 54, 55, 57, 59, 60, 62, 64], // E小调
                type: "minor"
            },
            sad: { 
                notes: [57, 59, 60, 62, 64, 65, 67, 69], // A小调
                type: "minor"
            }
        };
        
        this.sessionId = 'fallback-session-' + Date.now();
        console.log('🎵 使用优化降级配置成功');
    }
    
    setupEventListeners() {
        // 画布事件
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseleave', () => this.handleMouseLeave());
        
        this.canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            this.handleMouseMove(e.touches[0]);
        });
        this.canvas.addEventListener('touchend', () => this.handleMouseLeave());
        
        // 头像弹性拖拽事件
        this.setupAvatarDrag();
        
        // 控件事件
        this.playPauseBtn.addEventListener('click', () => this.toggleComposing());
        this.saveBtn.addEventListener('click', () => this.saveAudio());
        
        // 窗口调整
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.drawGrid();
        });

        console.log('🎮 事件监听器设置完成');
    }
    
    setupAvatarDrag() {
        // 鼠标事件
        this.avatarContainer.addEventListener('mousedown', (e) => this.startDrag(e));
        document.addEventListener('mousemove', (e) => this.drag(e));
        document.addEventListener('mouseup', () => this.stopDrag());
        
        // 触摸事件
        this.avatarContainer.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startDrag(e.touches[0]);
        });
        document.addEventListener('touchmove', (e) => {
            e.preventDefault();
            this.drag(e.touches[0]);
        });
        document.addEventListener('touchend', () => this.stopDrag());
    }
    
    startDrag(e) {
        this.isDragging = true;
        this.dragStartX = e.clientX;
        this.dragStartY = e.clientY;
        this.avatarOffsetX = 0;
        this.avatarOffsetY = 0;
        this.avatarContainer.classList.add('dragging');
        
        // 更新光标样式
        document.body.style.cursor = 'grabbing';
    }
    
    drag(e) {
        if (!this.isDragging) return;
        
        const deltaX = e.clientX - this.dragStartX;
        const deltaY = e.clientY - this.dragStartY;
        
        // 计算距离中心的距离
        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        
        // 弹性效果：距离越远，阻力越大
        if (distance > this.maxPullDistance) {
            const angle = Math.atan2(deltaY, deltaX);
            this.avatarOffsetX = Math.cos(angle) * this.maxPullDistance;
            this.avatarOffsetY = Math.sin(angle) * this.maxPullDistance;
        } else {
            this.avatarOffsetX = deltaX;
            this.avatarOffsetY = deltaY;
        }
        
        // 应用弹性位置
        this.avatarContainer.style.transform = `translate(calc(-50% + ${this.avatarOffsetX}px), calc(-50% + ${this.avatarOffsetY}px))`;
    }
    
    stopDrag() {
        if (!this.isDragging) return;
        
        this.isDragging = false;
        this.avatarContainer.classList.remove('dragging');
        document.body.style.cursor = '';
        
        // 弹性回弹动画
        gsap.to(this.avatarContainer, {
            x: 0,
            y: 0,
            duration: 0.6,
            ease: "elastic.out(1, 0.5)",
            onUpdate: () => {
                this.avatarContainer.style.transform = `translate(calc(-50% + ${this.avatarContainer._gsap.x}px), calc(-50% + ${this.avatarContainer._gsap.y}px))`;
            }
        });
        
        console.log('👤 头像弹性回弹');
    }
    
    getCurrentRegion(x, y) {
        // 将坐标转换为相对位置 (0-1)
        const relX = x / this.canvas.width;
        const relY = y / this.canvas.height;
        
        console.log(`坐标: (${relX.toFixed(2)}, ${relY.toFixed(2)})`);
        
        // 检测鼠标在哪个情绪区域
        for (const [mood, condition] of Object.entries(this.regions)) {
            if (condition(relX, relY)) {
                console.log(`检测到情绪区域: ${mood}`);
                return mood;
            }
        }
        
        console.log('未检测到情绪区域');
        return null;
    }
    
    updateRegionIndicator(mood) {
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
        
        // 更新头像容器样式
        this.avatarContainer.className = 'avatar-container ' + mood;
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
    
    async toggleComposing() {
        if (!this.isComposing) {
            await this.startComposing();
        } else {
            this.stopComposing();
        }
    }
    
    async startComposing() {
        // 初始化录音器
        const recorderReady = await this.initRecorder();
        if (!recorderReady) {
            alert('录音功能初始化失败，无法开始探索');
            return;
        }
        
        this.isComposing = true;
        Tone.Transport.start();
        
        // 自动开始录音
        this.startRecording();
        
        this.playPauseBtn.textContent = '停止探索';
        this.playPauseBtn.classList.add('playing');
        this.composingStatusDisplay.textContent = '状态: 探索中';
        
        console.log('🎵 开始探索 + 自动录音');
    }
    
    stopComposing() {
        this.isComposing = false;
        Tone.Transport.stop();
        
        // 自动停止录音
        this.stopRecording();
        
        this.playPauseBtn.textContent = '开始探索';
        this.playPauseBtn.classList.remove('playing');
        this.composingStatusDisplay.textContent = '状态: 已停止';
        this.updateRegionIndicator(null);
        this.currentMoodDisplay.textContent = '当前情绪: 等待探索';
        
        console.log('⏹️ 停止探索 + 录音');
    }
    
    startRecording() {
        if (!this.recorder) {
            console.warn('录音功能不可用');
            return;
        }
        
        this.audioChunks = [];
        this.recorder.start();
        this.isRecording = true;
        
        this.recordingStatusDisplay.textContent = '录音: 进行中';
        this.saveBtn.disabled = true;
        
        console.log('🎙️ 自动开始录音');
    }
    
    stopRecording() {
        if (this.recorder && this.isRecording) {
            this.recorder.stop();
            this.isRecording = false;
            
            this.recordingStatusDisplay.textContent = '录音: 已完成';
            
            console.log('⏹️ 自动停止录音');
        }
    }
    
    handleMouseMove(e) {
        if (!this.isComposing) return;
        
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const currentRegion = this.getCurrentRegion(x, y);
        if (currentRegion && currentRegion !== this.currentMood) {
            this.setMood(currentRegion);
        }
        
        const cellX = Math.floor(x / (this.canvas.width / this.gridWidth));
        const cellY = Math.floor(y / (this.canvas.height / this.gridHeight));
        
        if (cellX >= 0 && cellX < this.gridWidth && cellY >= 0 && cellY < this.gridHeight && this.currentMood) {
            this.createHighlight(cellX, cellY);
            this.triggerNote(cellX, cellY);
            this.sendCellToBackend(cellX, cellY);
        }
    }
    
    handleMouseLeave() {
        this.updateRegionIndicator(null);
        this.currentMoodDisplay.textContent = '当前情绪: 等待探索';
    }
    
    createHighlight(x, y) {
        const cellKey = `${x},${y}`;
        
        if (this.activeHighlights.has(cellKey)) {
            const existingHighlight = this.activeHighlights.get(cellKey);
            existingHighlight.remove();
            this.activeHighlights.delete(cellKey);
        }
        
        const cellWidth = this.canvas.width / this.gridWidth;
        const cellHeight = this.canvas.height / this.gridHeight;
        
        const highlight = document.createElement('div');
        highlight.className = `grid-highlight ${this.currentMood}`;
        highlight.style.width = `${cellWidth}px`;
        highlight.style.height = `${cellHeight}px`;
        highlight.style.left = `${x * cellWidth}px`;
        highlight.style.top = `${y * cellHeight}px`;
        highlight.style.opacity = '1';
        
        document.body.appendChild(highlight);
        
        setTimeout(() => {
            highlight.style.opacity = '0';
            setTimeout(() => {
                if (highlight.parentNode) {
                    highlight.parentNode.removeChild(highlight);
                }
                this.activeHighlights.delete(cellKey);
            }, 1500);
        }, 100);
        
        this.activeHighlights.set(cellKey, highlight);
    }
    
    async triggerNote(x, y) {
        if (!this.moodConfig[this.currentMood] || !this.isComposing) return;
        
        const cfg = this.moodConfig[this.currentMood];
        const scale = this.scales[this.currentMood];
        
        if (!scale || !scale.notes) return;
        
        this.stepCounter++;
        this.stepCounterDisplay.textContent = `音符: ${this.stepCounter}`;
        
        if (this.stepCounter % cfg.step === 0) {
            const mainPitch = this.getHarmonicPitch(x, y, scale);
            const velocity = this.mapIntensityToVelocity(1.0, cfg.vel);
            const duration = this.calculateNoteDuration(cfg.legato, cfg.bpm);
            
            this.synth.triggerAttackRelease(
                Tone.Frequency(mainPitch, "midi").toFrequency(),
                duration,
                Tone.now(),
                velocity / 127
            );
            
            this.playHarmonicChord(mainPitch, scale, cfg, duration, velocity);
        }
    }
    
    getHarmonicPitch(x, y, scale) {
        const rowNote = Math.floor((y / this.gridHeight) * 3);
        const colNote = Math.floor((x / this.gridWidth) * scale.notes.length);
        
        const baseOctave = Math.floor(rowNote);
        const noteIndex = colNote % scale.notes.length;
        
        let basePitch = scale.notes[noteIndex];
        basePitch += baseOctave * 12;
        
        return Math.max(48, Math.min(76, basePitch));
    }
    
    playHarmonicChord(rootPitch, scale, cfg, duration, velocity) {
        let chordIntervals;
        
        if (scale.type === "major") {
            chordIntervals = [0, 4, 7]; // 大三和弦
        } else {
            chordIntervals = [0, 3, 7]; // 小三和弦
        }
        
        if (Math.random() < 0.3) {
            chordIntervals.forEach((interval, index) => {
                const chordPitch = rootPitch + interval;
                if (chordPitch <= 76) {
                    const chordTime = Tone.now() + 0.05 + (index * 0.02);
                    const chordVelocity = velocity * (0.3 + (index * 0.15));
                    
                    this.synth.triggerAttackRelease(
                        Tone.Frequency(chordPitch, "midi").toFrequency(),
                        duration * 0.6,
                        chordTime,
                        chordVelocity / 127
                    );
                }
            });
        }
    }
    
    mapIntensityToVelocity(intensity, velRange) {
        const [min, max] = velRange;
        const randomVariation = (Math.random() - 0.5) * 8;
        return Math.floor(min + intensity * (max - min) + randomVariation);
    }
    
    calculateNoteDuration(legato, bpm) {
        const beatDuration = 60.0 / bpm;
        const randomVariation = 1 + (Math.random() - 0.5) * 0.03;
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
            
            await apiFetch(`/sessions/${this.sessionId}/cells`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(cellData)
            });
            
        } catch (error) {
            console.error('发送格子数据失败:', error);
        }
    }
    
    saveAudio() {
        if (!this.recordedAudio) {
            alert('没有可保存的录音');
            return;
        }
        
        const url = URL.createObjectURL(this.recordedAudio);
        const a = document.createElement('a');
        a.href = url;
        a.download = `情绪音乐_${this.formatDate(new Date())}.wav`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log('💾 音频已保存');
        this.showSaveNotification();
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
        notification.textContent = '🎵 音频已保存到本地！';
        
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
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
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