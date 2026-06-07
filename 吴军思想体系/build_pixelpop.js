/**
 * build_pixelpop.js
 * Generates pixelpop.html — Canvas 2D pop-art pixel mosaic
 * of 10,367 thought entities. Sorted by category → color-block zoning.
 * Three LOD levels: dots → abbreviations → full names.
 */
const fs = require('fs');

const entities = JSON.parse(fs.readFileSync('data/entities_compact.json', 'utf8'));
const categories = JSON.parse(fs.readFileSync('data/categories.json', 'utf8'));

const GRID_COLS = 102;
const GRID_ROWS = 102;
const TOTAL = entities.length;

const grid = new Array(GRID_COLS * GRID_ROWS).fill(null);
for (let i = 0; i < entities.length; i++) {
  grid[i] = entities[i];
}

const catsJS = JSON.stringify(categories);
const gridJS = JSON.stringify(grid);

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>像素波普拼贴 · Pixel Pop Collage — 吴军思想体系</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;overflow:hidden;background:#060609;font-family:'PingFang SC','Noto Sans SC','Microsoft YaHei',sans-serif}

canvas{display:block;position:fixed;top:0;left:0;width:100%;height:100%}
body.grabbing canvas{cursor:grabbing}
body.grab canvas{cursor:grab}
body.pointing canvas{cursor:pointer}

#topbar{position:fixed;top:0;left:0;right:0;z-index:20;display:flex;align-items:center;justify-content:space-between;padding:14px 24px;background:linear-gradient(180deg,rgba(6,6,9,0.96) 40%,rgba(6,6,9,0) 100%);pointer-events:none}
#topbar>*{pointer-events:auto}
#title{font-size:17px;font-weight:300;letter-spacing:0.25em;color:rgba(255,255,255,0.75);white-space:nowrap}

#zoom-group{display:flex;align-items:center;gap:10px}
#zoom-label{font-size:11px;color:rgba(255,255,255,0.45);min-width:38px;text-align:center;font-variant-numeric:tabular-nums;font-family:'SF Mono',Consolas,monospace}
#zoom-slider{-webkit-appearance:none;width:120px;height:4px;background:rgba(255,255,255,0.15);border-radius:2px;outline:none;cursor:pointer}
#zoom-slider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#fff;border:2px solid rgba(255,255,255,0.3);box-shadow:0 0 10px rgba(255,255,255,0.3);cursor:pointer}
#zoom-slider::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:#fff;border:2px solid rgba(255,255,255,0.3);box-shadow:0 0 10px rgba(255,255,255,0.3);cursor:pointer}

#filters{position:fixed;top:90px;left:50%;transform:translateX(-50%);z-index:20;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;background:rgba(10,10,18,0.78);backdrop-filter:blur(20px) saturate(1.4);-webkit-backdrop-filter:blur(20px) saturate(1.4);border:1px solid rgba(255,255,255,0.08);border-radius:24px;padding:8px 16px;box-shadow:0 8px 32px rgba(0,0,0,0.5)}
.filter-pill{display:flex;align-items:center;gap:6px;padding:5px 12px;border-radius:20px;border:1px solid;cursor:pointer;user-select:none;font-size:12px;transition:all 0.2s;white-space:nowrap;opacity:0.85}
.filter-pill:hover{opacity:1;transform:translateY(-1px)}
.filter-pill.on{opacity:1;color:#fff}
.filter-pill.off{opacity:0.3;filter:grayscale(0.7)}
.filter-pill .dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
.filter-pill .count{font-size:10px;opacity:0.55;margin-left:2px}

#tooltip{position:fixed;z-index:30;pointer-events:none;background:rgba(16,16,30,0.94);backdrop-filter:blur(24px) saturate(1.6);-webkit-backdrop-filter:blur(24px) saturate(1.6);border:1px solid rgba(255,255,255,0.12);border-radius:16px;padding:16px 22px;box-shadow:0 16px 48px rgba(0,0,0,0.6);opacity:0;transform:translateY(6px);transition:opacity 0.18s,transform 0.22s cubic-bezier(0.34,1.56,0.64,1);max-width:320px}
#tooltip.show{opacity:1;transform:translateY(0)}
#tooltip .t-name{font-size:18px;font-weight:600;color:#fff;margin-bottom:4px}
#tooltip .t-cat{font-size:12px;opacity:0.6}
#tooltip .t-color{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:middle}

#hint{position:fixed;bottom:28px;left:50%;transform:translateX(-50%);z-index:10;font-size:12px;color:rgba(255,255,255,0.3);letter-spacing:0.1em;pointer-events:none;transition:opacity 0.6s;user-select:none}

#legend{position:fixed;bottom:28px;right:24px;z-index:10;display:flex;flex-direction:column;gap:4px;font-size:11px;color:rgba(255,255,255,0.5)}
.legend-row{display:flex;align-items:center;gap:6px}
.legend-swatch{width:10px;height:10px;border-radius:2px;flex-shrink:0}
</style>
</head>
<body class="grab">

<canvas id="c"></canvas>

<div id="topbar">
  <div id="title">像素波普拼贴&nbsp;·&nbsp;Pixel Pop Collage</div>
  <div id="zoom-group">
    <span id="zoom-label">1.0×</span>
    <input type="range" id="zoom-slider" min="0" max="1000" value="500">
  </div>
</div>

<div id="filters"></div>

<div id="tooltip">
  <div class="t-name"></div>
  <div class="t-cat"></div>
</div>

<div id="legend"></div>
<div id="hint">滚轮缩放 &nbsp;|&nbsp; 拖拽平移 &nbsp;|&nbsp; 点击放大</div>

<script>
// ============================================================
// DATA
// ============================================================
var CATEGORIES = ${catsJS};
var GRID_DATA = ${gridJS};
var GRID_COLS = ${GRID_COLS};
var GRID_ROWS = ${GRID_ROWS};
var TOTAL_ENTITIES = ${TOTAL};

var CAT_STATS = [];
var _cc = new Array(CATEGORIES.length).fill(0);
for (var i = 0; i < GRID_DATA.length; i++) {
  var cell = GRID_DATA[i];
  if (cell) _cc[cell[1]]++;
}
for (var i = 0; i < CATEGORIES.length; i++) {
  CAT_STATS.push({ id: CATEGORIES[i].id, color: CATEGORIES[i].color, label: CATEGORIES[i].label, count: _cc[i] });
}

// ============================================================
// CONSTANTS
// ============================================================
var BASE_CELL = 10;
var GAP = 1;
var CELL_STRIDE = BASE_CELL + GAP;

var LOD1_S = 13;  // rendered cell px < 13  → LOD1 dots only
var LOD2_S = 42;  // rendered cell px >= 42 → LOD3 full name

var ZOOM_MIN = 0.2;
var ZOOM_MAX = 10;

// Pre-computed per-category RGB for fast access
var CAT_RGB = CATEGORIES.map(function(c) {
  var h = c.color.replace('#','');
  return {
    r: parseInt(h.substring(0,2),16),
    g: parseInt(h.substring(2,4),16),
    b: parseInt(h.substring(4,6),16),
    hex: c.color
  };
});

// ============================================================
// STATE
// ============================================================
var S = {
  ox: 0, oy: 0,       // offset
  s: 1,                // scale
  tox: 0, toy: 0,      // target offset
  ts: 1,               // target scale

  dragging: false,
  dsx: 0, dsy: 0,      // drag start
  dbx: 0, dby: 0,      // drag base offset
  pinchDist: 0,

  mx: 0, my: 0,
  hover: null,          // {col, row, data}

  filters: new Array(CATEGORIES.length).fill(true),

  dpr: 1,
  animId: 0,
  dirty: true,
};

// ============================================================
// DOM
// ============================================================
var canvas = document.getElementById('c');
var ctx = canvas.getContext('2d');
var tooltip = document.getElementById('tooltip');
var zoomSlider = document.getElementById('zoom-slider');
var zoomLabel = document.getElementById('zoom-label');
var filtersEl = document.getElementById('filters');
var legendEl = document.getElementById('legend');
var hintEl = document.getElementById('hint');
var body = document.body;

// ============================================================
// RESIZE
// ============================================================
function resize() {
  S.dpr = Math.min(window.devicePixelRatio || 1, 2);
  var W = window.innerWidth;
  var H = window.innerHeight;
  canvas.width = W * S.dpr;
  canvas.height = H * S.dpr;
  canvas.style.width = W + 'px';
  canvas.style.height = H + 'px';
  ctx.setTransform(1,0,0,1,0,0);
  ctx.scale(S.dpr, S.dpr);
  fitGrid();
}

function fitGrid() {
  var W = window.innerWidth;
  var H = window.innerHeight;
  var gw = GRID_COLS * CELL_STRIDE;
  var gh = GRID_ROWS * CELL_STRIDE;
  var ns = Math.min(W / gw, (H - 80) / gh) * 0.88;
  S.s = S.ts = ns;
  S.ox = S.tox = (W - gw * ns) / 2;
  S.oy = S.toy = (H - 80 - gh * ns) / 2 + 60;
  updateSlider();
  S.dirty = true;
}

// ============================================================
// ZOOM SLIDER
// ============================================================
function updateSlider() {
  var t = (Math.log(S.ts) - Math.log(ZOOM_MIN)) / (Math.log(ZOOM_MAX) - Math.log(ZOOM_MIN));
  zoomSlider.value = Math.round(Math.max(0, Math.min(1, t)) * 1000);
  zoomLabel.textContent = S.ts.toFixed(1) + '×';
}

zoomSlider.addEventListener('input', function() {
  var t = parseInt(zoomSlider.value) / 1000;
  S.ts = ZOOM_MIN * Math.exp(t * (Math.log(ZOOM_MAX) - Math.log(ZOOM_MIN)));
  S.ts = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, S.ts));

  var cx = window.innerWidth / 2;
  var cy = window.innerHeight / 2;
  var ratio = S.ts / S.s;
  S.tox = cx - (cx - S.ox) * ratio;
  S.toy = cy - (cy - S.oy) * ratio;
  S.dirty = true;
});

// ============================================================
// MOUSE / TOUCH
// ============================================================
canvas.addEventListener('mousedown', function(e) {
  if (e.button !== 0) return;
  S.dragging = true;
  S.dsx = e.clientX; S.dsy = e.clientY;
  S.dbx = S.ox; S.dby = S.oy;
  S.tox = S.ox; S.toy = S.oy;
  body.classList.remove('grab'); body.classList.add('grabbing');
});

window.addEventListener('mouseup', function() {
  if (!S.dragging) return;
  S.dragging = false;
  body.classList.remove('grabbing'); body.classList.add('grab');
  updateCursor();
});

window.addEventListener('mousemove', function(e) {
  S.mx = e.clientX; S.my = e.clientY;
  if (S.dragging) {
    S.ox = S.tox = S.dbx + (e.clientX - S.dsx);
    S.oy = S.toy = S.dby + (e.clientY - S.dsy);
    S.dirty = true;
    tooltip.classList.remove('show');
  } else {
    updateHover();
  }
});

canvas.addEventListener('wheel', function(e) {
  e.preventDefault();
  var factor = Math.exp(-e.deltaY * 0.0008);
  var ns = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, S.ts * factor));
  var ratio = ns / S.ts;
  S.ts = S.s = ns;
  S.tox = S.ox = e.clientX - (e.clientX - S.ox) * ratio;
  S.toy = S.oy = e.clientY - (e.clientY - S.oy) * ratio;
  updateSlider();
  S.dirty = true;
  updateHover();
}, {passive:false});

// Touch
canvas.addEventListener('touchstart', function(e) {
  e.preventDefault();
  if (e.touches.length === 1) {
    S.dragging = true;
    S.dsx = e.touches[0].clientX; S.dsy = e.touches[0].clientY;
    S.dbx = S.ox; S.dby = S.oy;
    S.tox = S.ox; S.toy = S.oy;
    body.classList.remove('grab'); body.classList.add('grabbing');
  } else if (e.touches.length === 2) {
    S.dragging = false;
    S.pinchDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
  }
}, {passive:false});

canvas.addEventListener('touchmove', function(e) {
  e.preventDefault();
  if (e.touches.length === 1 && S.dragging) {
    S.ox = S.tox = S.dbx + (e.touches[0].clientX - S.dsx);
    S.oy = S.toy = S.dby + (e.touches[0].clientY - S.dsy);
    S.dirty = true;
    tooltip.classList.remove('show');
  } else if (e.touches.length === 2 && S.pinchDist > 0) {
    var d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
    var factor = d / S.pinchDist;
    var cx = (e.touches[0].clientX + e.touches[1].clientX) / 2;
    var cy = (e.touches[0].clientY + e.touches[1].clientY) / 2;
    var ns = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, S.ts * factor));
    var ratio = ns / S.ts;
    S.ts = S.s = ns;
    S.tox = S.ox = cx - (cx - S.ox) * ratio;
    S.toy = S.oy = cy - (cy - S.oy) * ratio;
    updateSlider();
    S.dirty = true;
    S.pinchDist = d;
  }
}, {passive:false});

canvas.addEventListener('touchend', function() {
  S.dragging = false;
  S.pinchDist = 0;
  body.classList.remove('grabbing'); body.classList.add('grab');
});

// ============================================================
// HOVER
// ============================================================
function s2g(sx, sy) {
  return {
    col: Math.floor((sx - S.ox) / (CELL_STRIDE * S.s)),
    row: Math.floor((sy - S.oy) / (CELL_STRIDE * S.s))
  };
}

function cellRect(col, row) {
  return {
    x: col * CELL_STRIDE * S.s + S.ox,
    y: row * CELL_STRIDE * S.s + S.oy,
    w: BASE_CELL * S.s,
    h: BASE_CELL * S.s
  };
}

function updateHover() {
  var gc = s2g(S.mx, S.my);
  if (gc.col < 0 || gc.col >= GRID_COLS || gc.row < 0 || gc.row >= GRID_ROWS) {
    clearHover(); return;
  }
  var idx = gc.row * GRID_COLS + gc.col;
  var data = GRID_DATA[idx];
  if (!data) { clearHover(); return; }
  if (!S.filters[data[1]]) { clearHover(); return; }

  // Only show cursor change + tooltip when cell big enough (LOD2+)
  var cellPx = BASE_CELL * S.s;
  var prevKey = S.hover ? S.hover.col + ',' + S.hover.row : '';
  var newKey = gc.col + ',' + gc.row;

  if (prevKey === newKey && S.hover) {
    if (cellPx >= LOD1_S) positionTooltip(cellRect(gc.col, gc.row));
    return;
  }

  S.hover = { col: gc.col, row: gc.row, data: data };
  S.dirty = true;

  if (cellPx >= LOD1_S) {
    showTooltip(data, cellRect(gc.col, gc.row));
  } else {
    tooltip.classList.remove('show');
  }
  updateCursor();
}

function clearHover() {
  if (S.hover) { S.hover = null; S.dirty = true; tooltip.classList.remove('show'); updateCursor(); }
}

function showTooltip(data, rect) {
  var cat = CATEGORIES[data[1]];
  tooltip.querySelector('.t-name').textContent = data[0];
  tooltip.querySelector('.t-cat').innerHTML = '<span class="t-color" style="background:' + cat.color + '"></span>' + cat.label;
  tooltip.classList.add('show');
  positionTooltip(rect);
}

function positionTooltip(rect) {
  var tx = rect.x + rect.w + 16;
  var ty = rect.y + rect.h / 2 - 30;
  var tw = tooltip.offsetWidth || 200;
  var th = tooltip.offsetHeight || 60;
  if (tx + tw > window.innerWidth - 16) tx = rect.x - tw - 16;
  if (tx < 16) tx = 16;
  if (ty + th > window.innerHeight - 16) ty = window.innerHeight - th - 16;
  if (ty < 16) ty = 16;
  tooltip.style.left = tx + 'px';
  tooltip.style.top = ty + 'px';
}

function updateCursor() {
  if (S.dragging) return;
  if (S.hover && BASE_CELL * S.s >= LOD1_S) {
    body.classList.add('pointing'); body.classList.remove('grab');
  } else {
    body.classList.remove('pointing'); body.classList.add('grab');
  }
}

// ============================================================
// RENDERING
// ============================================================
function cellSize() { return BASE_CELL * S.s; }
function lod() {
  var cs = cellSize();
  if (cs < LOD1_S) return 1;
  if (cs < LOD2_S) return 2;
  return 3;
}

function visRange() {
  var stride = CELL_STRIDE * S.s;
  var W = window.innerWidth;
  var H = window.innerHeight;
  return {
    c0: Math.max(0, Math.floor(-S.ox / stride)),
    c1: Math.min(GRID_COLS - 1, Math.ceil((W - S.ox) / stride)),
    r0: Math.max(0, Math.floor(-S.oy / stride)),
    r1: Math.min(GRID_ROWS - 1, Math.ceil((H - S.oy) / stride))
  };
}

// Precompute a lookup of varied colors for silk-screen effect
// Keyed by category + a pseudorandom seed
var colorCache = {};
function getCellColor(catIdx, idx) {
  var key = catIdx;
  if (!colorCache[key]) {
    var c = CAT_RGB[catIdx];
    // Precompute 256 variations per category
    var arr = new Array(256);
    for (var i = 0; i < 256; i++) {
      var v = ((i - 128) * 0.1) | 0;
      arr[i] = 'rgb(' +
        Math.min(255, Math.max(0, c.r + v)) + ',' +
        Math.min(255, Math.max(0, c.g + v)) + ',' +
        Math.min(255, Math.max(0, c.b + v)) + ')';
    }
    colorCache[key] = arr;
  }
  var seed = ((idx * 2654435761) >>> 0) & 0xFF;
  return colorCache[key][seed];
}

// Brightness for text contrast
var catDark = CAT_RGB.map(function(c) {
  return (0.299 * c.r + 0.587 * c.g + 0.114 * c.b) < 140;
});

function render() {
  var W = window.innerWidth;
  var H = window.innerHeight;
  var L = lod();
  var V = visRange();
  var cp = BASE_CELL * S.s;       // cell pixel size
  var gp = GAP * S.s;              // gap pixel size
  var sp = CELL_STRIDE * S.s;     // stride pixel size

  var hc = S.hover ? S.hover.col : -1;
  var hr = S.hover ? S.hover.row : -1;

  // ---- Black background for the entire grid area (mortar) ----
  ctx.fillStyle = '#050508';
  ctx.fillRect(0, 0, W, H);

  // ---- Grid black backdrop ----
  var gx0 = V.c0 * sp + S.ox;
  var gy0 = V.r0 * sp + S.oy;
  var gx1 = (V.c1 + 1) * sp + S.ox;
  var gy1 = (V.r1 + 1) * sp + S.oy;
  // The background is already black, no need for extra rect

  // ---- Draw cells ----
  for (var row = V.r0; row <= V.r1; row++) {
    for (var col = V.c0; col <= V.c1; col++) {
      var idx = row * GRID_COLS + col;
      var data = GRID_DATA[idx];
      if (!data) continue;
      if (!S.filters[data[1]]) continue;

      var sx = col * sp + S.ox;
      var sy = row * sp + S.oy;
      if (cp < 0.5) continue;

      var catIdx = data[1];
      var isHov = (col === hc && row === hr);

      // Cell body fill
      if (L === 1) {
        ctx.fillStyle = CAT_RGB[catIdx].hex;
      } else {
        ctx.fillStyle = getCellColor(catIdx, idx);
      }
      ctx.fillRect(sx, sy, cp, cp);

      // ---- Text (LOD 2/3) ----
      if (L >= 2) {
        var name = data[0];
        var text, fontSize;

        if (L === 2) {
          // Abbreviation
          if (name.length <= 2) text = name;
          else if (cp > 25 && name.length >= 3) text = name.substring(0, 3);
          else text = name.substring(0, 2);
          fontSize = Math.max(7, Math.min(cp * 0.52, 14));
        } else {
          text = name;
          fontSize = Math.max(10, Math.min(cp * 0.32, 20));
        }

        ctx.fillStyle = catDark[catIdx] ? '#ffffff' : '#111111';
        ctx.font = fontSize + 'px "PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        // Scale down text if too wide
        var tw = ctx.measureText(text).width;
        if (tw > cp - 3) {
          var sf = (cp - 3) / tw;
          var fs2 = Math.max(5, fontSize * sf);
          ctx.font = fs2 + 'px "PingFang SC","Noto Sans SC","Microsoft YaHei",sans-serif';
        }
        ctx.fillText(text, sx + cp / 2, sy + cp / 2);

        // Category dot at corner (LOD 3)
        if (L === 3 && cp > 35) {
          ctx.fillStyle = CAT_RGB[catIdx].hex;
          ctx.beginPath();
          ctx.arc(sx + cp - 4, sy + 4, Math.max(2.5, cp * 0.065), 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // ---- Hover highlight ----
      if (isHov && L >= 2) {
        ctx.save();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = Math.max(1.5, cp * 0.06);
        ctx.shadowColor = CAT_RGB[catIdx].hex;
        ctx.shadowBlur = cp * 0.25;
        ctx.strokeRect(sx + 0.5, sy + 0.5, cp - 1, cp - 1);
        ctx.restore();
      }
    }
  }

  // ---- Pop-art vignette ----
  if (L <= 2) {
    var grad = ctx.createRadialGradient(W/2, H/2, W * 0.35, W/2, H/2, W * 0.72);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(1, 'rgba(0,0,0,0.4)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);
  }

  // ---- Tooltip refresh ----
  if (S.hover && L >= 2) {
    showTooltip(S.hover.data, cellRect(S.hover.col, S.hover.row));
  } else if (S.hover && L < 2) {
    tooltip.classList.remove('show');
  }
}

// ============================================================
// ANIMATION LOOP
// ============================================================
function loop() {
  // Smooth lerp toward target
  if (!S.dragging) {
    var lerp = 0.32;
    var dx = S.tox - S.ox, dy = S.toy - S.oy, ds = S.ts - S.s;
    if (Math.abs(dx) > 0.3 || Math.abs(dy) > 0.3 || Math.abs(ds) > 0.0005) {
      S.ox += dx * lerp;
      S.oy += dy * lerp;
      S.s += ds * lerp;
      S.dirty = true;
    }
  }

  if (S.dirty) {
    render();
    S.dirty = false;
    updateHint();
  }

  S.animId = requestAnimationFrame(loop);
}

function updateHint() {
  var L = lod();
  if (L === 1) {
    hintEl.textContent = '滚轮放大查看细节  |  拖拽平移';
    hintEl.style.opacity = '0.5';
  } else if (L === 2) {
    hintEl.textContent = '继续放大查看完整名称  |  拖拽平移';
    hintEl.style.opacity = '0.4';
  } else {
    hintEl.textContent = '悬停查看详情  |  滚轮缩小看全景';
    hintEl.style.opacity = '0.3';
  }
}

// ============================================================
// FILTER UI
// ============================================================
function buildFilterUI() {
  var html = '';
  CAT_STATS.forEach(function(cat, i) {
    html += '<div class="filter-pill on" style="border-color:' + cat.color + '" data-idx="' + i + '">' +
      '<span class="dot" style="background:' + cat.color + '"></span>' +
      '<span>' + cat.label + '</span>' +
      '<span class="count">' + cat.count + '</span></div>';
  });
  filtersEl.innerHTML = html;
  // Delegate click
  filtersEl.addEventListener('click', function(e) {
    var pill = e.target.closest('.filter-pill');
    if (!pill) return;
    var idx = parseInt(pill.getAttribute('data-idx'));
    S.filters[idx] = !S.filters[idx];
    if (S.filters[idx]) { pill.classList.add('on'); pill.classList.remove('off'); }
    else { pill.classList.remove('on'); pill.classList.add('off'); }
    S.dirty = true;
  });
}

function buildLegend() {
  legendEl.innerHTML = CAT_STATS.map(function(c) {
    return '<div class="legend-row"><span class="legend-swatch" style="background:' + c.color + '"></span>' + c.label + '</div>';
  }).join('');
}

// ============================================================
// KEYBOARD
// ============================================================
window.addEventListener('keydown', function(e) {
  if (e.key === 'f' || e.key === '0') {
    fitGrid();
    S.ox = S.tox; S.oy = S.toy; S.s = S.ts;
    S.dirty = true;
  }
  if (e.key === 'Escape') {
    S.filters = new Array(CATEGORIES.length).fill(true);
    var pills = document.querySelectorAll('.filter-pill');
    for (var i = 0; i < pills.length; i++) { pills[i].classList.add('on'); pills[i].classList.remove('off'); }
    S.dirty = true;
  }
});

// ============================================================
// CLICK TO ZOOM
// ============================================================
canvas.addEventListener('click', function(e) {
  if (S.dragging) return;
  if (!S.hover || lod() < 2) return;
  var rect = cellRect(S.hover.col, S.hover.row);
  var cx = window.innerWidth / 2;
  var cy = window.innerHeight / 2;
  var ns = Math.min(ZOOM_MAX, S.s * 2.8);
  var ratio = ns / S.s;
  S.ts = ns;
  S.tox = cx - (rect.x + rect.w / 2) * ratio;
  S.toy = cy - (rect.y + rect.h / 2) * ratio;
  updateSlider();
  S.dirty = true;
});

// ============================================================
// INIT
// ============================================================
function init() {
  buildFilterUI();
  buildLegend();
  resize();
  S.ox = S.tox; S.oy = S.toy; S.s = S.ts;
  updateSlider();
  S.animId = requestAnimationFrame(loop);
}

window.addEventListener('resize', function() {
  resize();
  S.ox = S.tox; S.oy = S.toy; S.s = S.ts;
  S.dirty = true;
});

init();
</script>

</body>
</html>`;

fs.writeFileSync('pixelpop.html', html);
console.log('Written pixelpop.html (' + (html.length / 1024).toFixed(1) + ' KB)');
console.log('Grid: ' + GRID_COLS + '×' + GRID_ROWS + ', entities: ' + TOTAL);
var dist = {}; grid.forEach(function(e) { if (e) { var l = categories[e[1]].label; dist[l] = (dist[l]||0)+1; }});
console.log('Category distribution:', dist);
