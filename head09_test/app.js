// 前端应用主逻辑 - 修复四个区域划分
class EmotionCanvasApp {
    constructor() {
        this.canvas = document.getElementById('gridCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvasContainer = document.querySelector('.canvas-container');
        this.avatarContainer = document.querySelector('.avatar-container');
        this.avatar = document.getElementById('avatar');
        this.currentMoodDisplay = document.getElementById('currentMood');
        this.stepCounterDisplay = document.getElementById('stepCounter');
        this.composingStatusDisplay = document.getElementById('composingStatus');
        this.recordingStatusDisplay = document.getElementById('recordingStatus');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.saveBtn = document.getElementById('saveBtn');
        this.audioPlayer = document.getElementById('audioPlayer');
        this.infoDrawer = document.querySelector('.info-drawer');
        this.infoPull = document.querySelector('.info-pull');
        this.infoHand = document.querySelector('.info-hand');
        this.container = document.querySelector('.container');
        
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
        this.drawerTimer = null;
        this.drawerIsOpen = false;
        this.avatarIdleTimer = null;
        this.isAvatarHover = false;
        
        // avatar assets
        this.avatarFaces = {
            base: './assets/face.png',
            baseAlt: './assets/face_2.png',
            happy: './assets/happy_face.png',
            calm: './assets/clam_face.png',
            tense: './assets/tense_face.png',
            sad: './assets/sad_face.png'
        };
        this.avatar.src = this.avatarFaces.base;
        this.highlightImages = {
            happy: { base: './assets/grid_happy.png', overlay: './assets/grid_happy_ex.png' },
            calm: { base: './assets/grid_clam.png', overlay: './assets/grid_clam_ex.png' },
            tense: { base: './assets/grid_tense.png', overlay: './assets/grid_tense_ex.png' },
            sad: { base: './assets/grid_sad.png', overlay: './assets/grid_sad_ex.png' }
        };

        // grid config (1584/72=22, 864/72=12)
        this.gridWidth = 22;
        this.gridHeight = 12;
        
        // 修复的情绪区域定义 - 正确划分四个区域
                // 情绪区域：以上/下/左/右为主轴划分（距中心偏移更大的方向）
        this.regions = null;
        
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
        this.setupDrawerInteraction();
        this.setupAvatarHover();
        this.resizeCanvas();
        this.drawGrid();
        
        // 启动音频
        await Tone.start();
        console.log('🎵 音频上下文已启动');
    }
    
    async initBackend() {
        try {
            const moodsResponse = await fetch('/moods');
            this.moodConfig = await moodsResponse.json();
            console.log('情绪配置:', this.moodConfig);
            
            for (const mood in this.moodConfig) {
                const scaleName = this.moodConfig[mood].scale;
                const scaleResponse = await fetch(`/scale?name=${scaleName}`);
                this.scales[mood] = await scaleResponse.json();
            }
            
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
        const p = this.mapClientToDesign(e.clientX, e.clientY);
        this.dragStartX = p.x;
        this.dragStartY = p.y;
        this.avatarOffsetX = 0;
        this.avatarOffsetY = 0;
        this.avatarContainer.classList.add('dragging');
        
        // 更新光标样式
        document.body.style.cursor = 'grabbing';
    }
    
    drag(e) {
        if (!this.isDragging) return;
        const p = this.mapClientToDesign(e.clientX, e.clientY);
        const deltaX = p.x - this.dragStartX;
        const deltaY = p.y - this.dragStartY;
        
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
        const relX = x / this.canvas.width;
        const relY = y / this.canvas.height;
        const dx = relX - 0.5;
        const dy = relY - 0.5;

        // 取偏移更大的轴决定情绪：上 happy，下 sad，左 calm，右 tense
        let mood;
        if (Math.abs(dy) >= Math.abs(dx)) {
            mood = dy < 0 ? 'happy' : 'sad';
        } else {
            mood = dx > 0 ? 'tense' : 'calm';
        }
        return mood;
    }
    
    updateRegionIndicator(mood) {
        document.querySelectorAll('.region-label').forEach(label => {
            const isActive = mood && label.classList.contains(`${mood}-region`);
            const defaultSrc = label.dataset.srcDefault;
            const activeSrc = label.dataset.srcActive;

            label.classList.toggle('active', Boolean(isActive));
            if (isActive && activeSrc) {
                label.src = activeSrc;
            } else if (defaultSrc) {
                label.src = defaultSrc;
            }
        });
    }
    
    setMood(mood) {
        if (this.currentMood === mood) return;

        this.currentMood = mood;
        this.currentMoodDisplay.textContent = `Current mood: ${this.getMoodText(mood)}`;
        this.setAvatarFace(mood);

        // 更新头像容器样式
        this.avatarContainer.className = 'avatar-container ' + mood;
        this.updateRegionIndicator(mood);

        if (mood === null) {
            this.startAvatarIdle();
        } else {
            this.stopAvatarIdle();
        }

        console.log(`🎵 Entered mood region: ${mood}`);
    }

    getMoodText(mood) {
        const texts = {
            happy: 'Happy',
            calm: 'Calm',
            tense: 'Tense',
            sad: 'Sad'
        };
        if (!mood) return 'Awaiting exploration';
        return texts[mood] || mood;
    }

    setAvatarFace(mood) {
        const faceSrc = this.avatarFaces[mood] || this.avatarFaces.base;
        this.avatar.src = faceSrc;
        if (!mood) {
            this.startAvatarIdle();
        } else {
            this.stopAvatarIdle();
        }
    }

    async toggleComposing() {
        if (!this.isComposing) {
            if (this.drawerIsOpen && typeof this.closeDrawer === 'function') {
                this.closeDrawer();
            }
            await this.startComposing();
        } else {
            this.stopComposing();
        }
    }
    
    async startComposing() {
        const recorderReady = await this.initRecorder();
        if (!recorderReady) {
            alert('Recording unavailable, cannot start exploring.');
            return;
        }

        this.isComposing = true;
        Tone.Transport.start();

        this.startRecording();

        this.playPauseBtn.textContent = "Stop Exploring";
        this.playPauseBtn.classList.add('playing');
        this.composingStatusDisplay.textContent = "Status: Exploring";

        console.log('🎵 Start exploring + auto recording');
    }

    stopComposing() {
        this.isComposing = false;
        Tone.Transport.stop();

        this.stopRecording();

        this.playPauseBtn.textContent = "Start Exploring";
        this.playPauseBtn.classList.remove('playing');
        this.composingStatusDisplay.textContent = "Status: Stopped";
        this.updateRegionIndicator(null);
        this.currentMood = null;
        this.setAvatarFace(null);
        this.currentMoodDisplay.textContent = "Current mood: Awaiting exploration";

        console.log('⏹️ Stop exploring + recording');
    }

    startRecording() {
        if (!this.recorder) {
            console.warn('Recorder unavailable');
            return;
        }

        this.audioChunks = [];
        this.recorder.start();
        this.isRecording = true;

        this.recordingStatusDisplay.textContent = 'Recording: In progress';
        this.saveBtn.disabled = true;

        console.log('🎙️ Auto recording started');
    }

    stopRecording() {
        if (this.recorder && this.isRecording) {
            this.recorder.stop();
            this.isRecording = false;
            
            this.recordingStatusDisplay.textContent = 'Recording: Completed';
            
            console.log('⏹️ Auto recording stopped');
        }
    }

    handleMouseMove(e) {
        if (!this.isComposing) return;
        const p = this.mapClientToDesign(e.clientX, e.clientY);
        const x = p.x;
        const y = p.y;
        
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
        this.currentMood = null;
        this.setAvatarFace(null);
        this.currentMoodDisplay.textContent = "Current mood: Awaiting exploration";
        this.startAvatarIdle();
    }

    createHighlight(x, y) {
        const mood = this.currentMood;
        const images = this.highlightImages[mood];
        if (!images) return;

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

        const baseImg = document.createElement('img');
        baseImg.className = 'base-layer';
        baseImg.src = images.base;

        const overlayImg = document.createElement('img');
        overlayImg.className = 'overlay-layer';
        overlayImg.src = images.overlay;

        highlight.appendChild(baseImg);
        highlight.appendChild(overlayImg);

        const container = this.canvasContainer || document.body;
        container.appendChild(highlight);

        setTimeout(() => {
            baseImg.classList.add('fade');
        }, 100);

        setTimeout(() => {
            overlayImg.classList.add('dissolve');
        }, 700);

        setTimeout(() => {
            if (highlight.parentNode) {
                highlight.parentNode.removeChild(highlight);
            }
            this.activeHighlights.delete(cellKey);
        }, 1500);
        
        this.activeHighlights.set(cellKey, highlight);
    }
    
    async triggerNote(x, y) {
        if (!this.moodConfig[this.currentMood] || !this.isComposing) return;
        
        const cfg = this.moodConfig[this.currentMood];
        const scale = this.scales[this.currentMood];
        
        if (!scale || !scale.notes) return;
        
        this.stepCounter++;
        this.stepCounterDisplay.textContent = `Notes: ${this.stepCounter}`;
        
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
            
            await fetch(`/sessions/${this.sessionId}/cells`, {
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
            alert('No recording to save');
            return;
        }
        
        const url = URL.createObjectURL(this.recordedAudio);
        const a = document.createElement('a');
        a.href = url;
        a.download = `emoti_record_${this.formatDate(new Date())}.wav`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        console.log('💾 Audio saved');
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
        // 固定画布尺寸为容器尺寸，保持与背景网格对齐
        const rect = this.canvasContainer?.getBoundingClientRect();
        if (rect) {
            this.canvas.width = rect.width;
            this.canvas.height = rect.height;
        } else {
            // fallback 固定为设计稿尺寸
            this.canvas.width = 1584;
            this.canvas.height = 864;
        }
    }

    // 把客户端坐标映射到设计/画布坐标，兼容 head08 缩放 (window.__HK_SCALE)
    mapClientToDesign(clientX, clientY) {
        const scale = window.__HK_SCALE || 1;
        const appEl = document.querySelector('.hk-app');
        if (appEl) {
            const rect = appEl.getBoundingClientRect();
            return { x: (clientX - rect.left) / scale, y: (clientY - rect.top) / scale };
        }
        // fallback to canvas rect
        const rect = this.canvas.getBoundingClientRect();
        return { x: clientX - rect.left, y: clientY - rect.top };
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

    setupAvatarHover() {
        if (!this.avatarContainer) return;
        this.avatarContainer.addEventListener('mouseenter', () => {
            this.isAvatarHover = true;
            this.stopAvatarIdle();
            if (!this.currentMood) {
                this.avatar.src = this.avatarFaces.base;
            }
        });
        this.avatarContainer.addEventListener('mouseleave', () => {
            this.isAvatarHover = false;
            if (!this.currentMood) {
                this.startAvatarIdle();
            }
        });
        this.startAvatarIdle(500);
    }

    startAvatarIdle(interval = 500) {
        if (this.currentMood || this.isAvatarHover) return;
        if (this.avatarIdleTimer) return;
        let toggle = false;
        this.avatarIdleTimer = setInterval(() => {
            if (this.currentMood || this.isAvatarHover) {
                this.stopAvatarIdle();
                return;
            }
            toggle = !toggle;
            this.avatar.src = toggle ? this.avatarFaces.base : this.avatarFaces.baseAlt;
        }, interval);
    }

    stopAvatarIdle() {
        if (this.avatarIdleTimer) {
            clearInterval(this.avatarIdleTimer);
            this.avatarIdleTimer = null;
        }
        if (this.avatarFaces && this.avatar) {
            this.avatar.src = this.avatarFaces[this.currentMood] || this.avatarFaces.base;
        }
    }

    setupDrawerInteraction() {
        const dragTargets = [this.infoHand].filter(Boolean);
        if (!this.infoDrawer || dragTargets.length === 0) return;

        const handImg = this.infoHand;
        const originalHandSrc = handImg ? handImg.src : null;
        const openedHandSrc = './assets/hand02.png';
        const originalPullSrc = this.infoPull ? this.infoPull.src : null;
        const openedPullSrc = './assets/close.png';
        const closeDrawer = () => {
            if (!this.drawerIsOpen) return;
            this.drawerIsOpen = false;
            this.infoDrawer.classList.remove('open');
            if (handImg) {
                handImg.src = originalHandSrc || handImg.src;
                handImg.style.left = '1512px';
                handImg.style.top = '403px';
                handImg.style.transform = '';
            }
            if (this.infoPull) this.infoPull.src = originalPullSrc || this.infoPull.src;
        };
        this.closeDrawer = closeDrawer;

        dragTargets.forEach(el => {
            let isDown = false;
            let startX = 0;
            let startY = 0;
            let offsetX = 0;
            let offsetY = 0;
            let startTime = 0;

            const onMove = (e) => {
                if (!isDown || this.drawerIsOpen) return;
                const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                const clientY = e.touches ? e.touches[0].clientY : e.clientY;
                let dx = clientX - startX;
                let dy = clientY - startY;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist > 85) {
                    const scale = 85 / dist;
                    dx *= scale;
                    dy *= scale;
                }
                offsetX = dx;
                offsetY = dy;
                // 应用偏移到手
                if (handImg) handImg.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
                const elapsed = Date.now() - startTime;
                if (elapsed >= 1000) {
                    openDrawer();
                    endDrag();
                }
            };

            const endDrag = () => {
                isDown = false;
                window.removeEventListener('mousemove', onMove);
                window.removeEventListener('touchmove', onMove);
                window.removeEventListener('mouseup', endDrag);
                window.removeEventListener('touchend', endDrag);
                if (!this.drawerIsOpen) {
                    if (handImg) handImg.style.transform = '';
                }
            };

            const openDrawer = () => {
                this.drawerIsOpen = true;
                this.infoDrawer.classList.add('open');
                if (handImg) {
                    handImg.src = openedHandSrc;
                    handImg.style.transform = '';
                }
                if (this.infoPull) this.infoPull.src = openedPullSrc;
            };

            el.addEventListener('mousedown', (e) => {
                if (this.drawerIsOpen) return;
                isDown = true;
                startX = e.clientX;
                startY = e.clientY;
                startTime = Date.now();
                window.addEventListener('mousemove', onMove);
                window.addEventListener('mouseup', endDrag);
            });

            el.addEventListener('touchstart', (e) => {
                if (this.drawerIsOpen) return;
                isDown = true;
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
                startTime = Date.now();
                window.addEventListener('touchmove', onMove, { passive: false });
                window.addEventListener('touchend', endDrag);
            });
        });

        // 点击 close 收起
        if (this.infoPull) {
            this.infoPull.addEventListener('click', () => {
                closeDrawer();
            });
        }
    }
}

// 启动应用
document.addEventListener('DOMContentLoaded', () => {
    try {
        window.app = new EmotionCanvasApp();
        console.log('App initialized');
    } catch (error) {
        console.error('App init failed:', error);
        alert('App failed to start, please refresh and try again.');
    }
});

