// head08_test starter JS — small harness to preview UI and wire controls
document.addEventListener('DOMContentLoaded', () => {
  console.log('head08 UI workbench ready');

  const playBtn = document.getElementById('playPauseBtn');
  const saveBtn = document.getElementById('saveBtn');

  playBtn.addEventListener('click', () => {
    if (playBtn.classList.contains('playing')){
      playBtn.classList.remove('playing');
      playBtn.textContent = '开始探索';
    } else {
      playBtn.classList.add('playing');
      playBtn.textContent = '停止探索';
      saveBtn.disabled = false;
    }
  });

  saveBtn.addEventListener('click', () => {
    alert('这里会触发保存逻辑（占位）');
  });

});

// ---------- 固定设计视口 (1440 x 720) 与 canvas 像素设置 ----------
const DESIGN_W = 1440;
const DESIGN_H = 720;

function setupFixedCanvas() {
  const canvas = document.getElementById('gridCanvas');
  const appEl = document.querySelector('.hk-app');
  if (!canvas || !appEl) return;

  // CSS 显示尺寸等于设计尺寸
  canvas.style.width = DESIGN_W + 'px';
  canvas.style.height = DESIGN_H + 'px';

  // 内部像素尺寸按 devicePixelRatio 放大以保证清晰度
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.round(DESIGN_W * dpr);
  canvas.height = Math.round(DESIGN_H * dpr);

  // 将绘图坐标系统缩放回 CSS 像素单位，便于绘图使用设计坐标
  const ctx = canvas.getContext('2d');
  if (ctx && ctx.setTransform) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
}

// 把客户端坐标 (clientX, clientY) 映射到设计坐标 (0..1440, 0..720)
function mapClientToDesign(clientX, clientY) {
  const appEl = document.querySelector('.hk-app');
  if (!appEl) return { x: clientX, y: clientY };
  const rect = appEl.getBoundingClientRect();
  const scale = window.__HK_SCALE || 1;
  // rect reflects the scaled size; divide by scale to map back to design coordinates
  const x = (clientX - rect.left) / scale;
  const y = (clientY - rect.top) / scale;
  return { x: x, y: y };
}

// 初始化并在窗口调整时更新
document.addEventListener('DOMContentLoaded', () => {
  // Apply scale first so CSS layout/rect are correct for canvas sizing
  applyScale();
  setupFixedCanvas();
  window.addEventListener('resize', () => {
    applyScale();
    setupFixedCanvas();
  });
});

// 计算并应用整体缩放，使设计视口在小屏时按比例缩放
function applyScale() {
  const appEl = document.querySelector('.hk-app');
  if (!appEl) return;

  const vw = window.innerWidth;
  const vh = window.innerHeight;
  // 计算缩放比例（不放大设计，避免模糊）
  const scale = Math.min(vw / DESIGN_W, vh / DESIGN_H, 1);

  appEl.style.transform = `scale(${scale})`;
  // 居中显示：设置 margin 使缩放后居中
  const mx = Math.max(0, (vw - DESIGN_W * scale) / 2);
  const my = Math.max(0, (vh - DESIGN_H * scale) / 2);
  appEl.style.marginLeft = mx + 'px';
  appEl.style.marginTop = my + 'px';

  window.__HK_SCALE = scale;
}