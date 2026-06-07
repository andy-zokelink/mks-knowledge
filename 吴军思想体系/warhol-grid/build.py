#!/usr/bin/env python3
"""Generate warhol-grid/index.html — 10,367 entity cards in Warhol soup-can style."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

with open(os.path.join(ROOT, 'data', 'entities.json')) as f:
    entities = json.load(f)
with open(os.path.join(ROOT, 'data', 'categories.json')) as f:
    categories = json.load(f)

# Sort entities by category order as specified
cat_order = {c['id']: i for i, c in enumerate(categories)}
entities.sort(key=lambda e: cat_order.get(e['category'], 99))

# Compact encoding: [name, catIdx]
cat_idx = {c['id']: i for i, c in enumerate(categories)}
compact = [[e['name'], cat_idx[e['category']]] for e in entities]

entities_json = json.dumps(compact, ensure_ascii=False)
categories_json = json.dumps(categories, ensure_ascii=False)

# Category counts for legend
cat_counts = {i: sum(1 for e in compact if e[1] == i) for i in range(len(categories))}

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>思想的罐头工厂 · Warhol Grid</title>
<style>
/* ===== Reset & Base ===== */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:100%;height:100%;overflow:hidden;font-family:"Helvetica Neue","PingFang SC","Microsoft YaHei",sans-serif;background:#1a1a2e}}

/* ===== Title Bar ===== */
.title-bar{{
  position:sticky;top:0;z-index:10000;
  display:flex;align-items:center;justify-content:space-between;
  height:50px;padding:0 20px;
  background:#0f0f1a;color:#fff;
  border-bottom:1px solid #333;
}}
.title-bar h1{{
  font-size:17px;font-weight:900;letter-spacing:2px;
  background:linear-gradient(90deg,#a855f7,#10b981,#3b82f6,#f97316,#06b6d4,#f59e0b,#ef4444);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}}
.title-bar .count{{font-size:11px;color:#666;letter-spacing:1px}}

/* ===== Legend (fixed top-right) ===== */
.legend{{
  position:fixed;top:56px;right:10px;z-index:10001;
  display:flex;flex-direction:column;gap:2px;
  background:rgba(15,15,26,0.94);backdrop-filter:blur(10px);
  padding:8px 12px;border-radius:8px;border:1px solid #333;
  pointer-events:none;
}}
.legend-item{{display:flex;align-items:center;gap:7px;font-size:10px;color:#bbb;white-space:nowrap}}
.legend-swatch{{width:12px;height:12px;border-radius:2px;flex-shrink:0}}
.legend-count{{color:#555;font-size:9px;margin-left:1px}}

/* ===== Grid Container ===== */
.grid-container{{
  width:100%;height:calc(100vh - 50px);
  overflow-y:auto;overflow-x:hidden;
  padding:3px;
  scroll-behavior:smooth;
}}
.grid{{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(62px,1fr));
  gap:3px;
}}

/* ===== Card ===== */
.card{{
  position:relative;
  aspect-ratio:1;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;
  transition:transform .22s cubic-bezier(.34,1.56,.64,1),
             box-shadow .22s ease,
             border-radius .22s ease;
  will-change:transform;
  overflow:hidden;
  border-radius:3px;
  contain:layout style paint;
  content-visibility:auto;
  contain-intrinsic-size:62px;
}}
/* Halftone dot overlay — Warhol screen-print texture */
.card::after{{
  content:"";
  position:absolute;inset:0;
  background-image:radial-gradient(circle,rgba(0,0,0,.08) 1px,transparent 1px);
  background-size:6px 6px;
  pointer-events:none;z-index:0;
}}
/* Glossy highlight stripe */
.card::before{{
  content:"";
  position:absolute;top:0;left:0;right:0;height:35%;
  background:linear-gradient(180deg,rgba(255,255,255,.28) 0%,transparent 100%);
  pointer-events:none;z-index:0;
  border-radius:3px 3px 0 0;
}}
.card .card-text{{
  font-size:7.5px;font-weight:800;color:#fff;
  text-align:center;line-height:1.15;
  text-shadow:0 1px 3px rgba(0,0,0,.7);
  padding:2px;position:relative;z-index:1;
  overflow:hidden;text-overflow:ellipsis;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;
  pointer-events:none;letter-spacing:.5px;
  word-break:keep-all;
}}

/* ===== Card Hover — "pick up a can from the shelf" ===== */
.card:hover{{
  transform:scale(3);
  z-index:9999!important;
  box-shadow:0 12px 48px rgba(0,0,0,.65),0 0 0 4px #fff;
  border-radius:5px;
  overflow:visible!important;
  contain:none!important;
  content-visibility:visible!important;
  transition:transform .18s cubic-bezier(.34,1.56,.64,1),
             box-shadow .18s ease,
             border-radius .18s ease;
}}
.card:hover::after,
.card:hover::before{{border-radius:5px}}
.card:hover .card-text{{
  font-size:8.5px;-webkit-line-clamp:unset;
  display:flex;align-items:center;justify-content:center;
  word-break:break-all;
}}
/* Category label revealed on hover */
.card:hover .card-cat{{
  opacity:1;
}}

.card-cat{{
  position:absolute;bottom:3px;left:0;right:0;
  font-size:5.5px;color:rgba(255,255,255,.82);text-align:center;
  z-index:2;pointer-events:none;letter-spacing:1px;
  text-shadow:0 1px 2px rgba(0,0,0,.5);
  opacity:0;transition:opacity .15s ease;
}}

/* ===== Category Dividers ===== */
.cat-divider{{
  grid-column:1/-1;
  height:26px;display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:900;letter-spacing:3px;color:#fff;
  margin:4px 0;position:relative;
  contain:layout style paint;
}}
.cat-divider::before,.cat-divider::after{{
  content:"";flex:1;height:1.5px;margin:0 10px;opacity:.45;
}}
.cat-divider::before{{background:linear-gradient(90deg,transparent,currentColor)}}
.cat-divider::after{{background:linear-gradient(90deg,currentColor,transparent)}}

/* ===== Responsive ===== */
@media(max-width:1024px){{
  .grid{{grid-template-columns:repeat(auto-fill,minmax(50px,1fr));gap:2px}}
  .card .card-text{{font-size:6.5px}}
  .card{{contain-intrinsic-size:50px}}
  .card:hover{{transform:scale(3.2)}}
  .card:hover .card-text{{font-size:7.5px}}
}}
@media(max-width:768px){{
  .grid{{grid-template-columns:repeat(auto-fill,minmax(42px,1fr));gap:2px}}
  .card .card-text{{font-size:5.5px}}
  .card{{contain-intrinsic-size:42px}}
  .card:hover{{transform:scale(3.5)}}
  .card:hover .card-text{{font-size:6.5px}}
  .title-bar h1{{font-size:14px;letter-spacing:1px}}
  .title-bar{{height:42px;padding:0 12px}}
  .grid-container{{height:calc(100vh - 42px)}}
  .legend{{top:48px;right:6px;padding:6px 10px}}
  .legend-item{{font-size:9px;gap:5px}}
  .legend-swatch{{width:10px;height:10px}}
  .cat-divider{{font-size:9px;height:22px;letter-spacing:1px}}
  .card-cat{{font-size:5px}}
}}
@media(max-width:480px){{
  .grid{{grid-template-columns:repeat(auto-fill,minmax(34px,1fr));gap:1.5px}}
  .card .card-text{{font-size:4.5px;-webkit-line-clamp:2}}
  .card{{contain-intrinsic-size:34px;border-radius:2px}}
  .card:hover{{transform:scale(4)}}
  .card:hover .card-text{{font-size:5.5px}}
  .title-bar h1{{font-size:12px;letter-spacing:.5px}}
  .title-bar{{height:38px;padding:0 10px}}
  .grid-container{{height:calc(100vh - 38px);padding:2px}}
  .legend{{top:42px;right:3px;padding:4px 8px;gap:1px}}
  .legend-item{{font-size:8px;gap:3px}}
  .legend-swatch{{width:8px;height:8px}}
  .cat-divider{{font-size:8px;height:18px;letter-spacing:.5px;margin:2px 0}}
  .card-cat{{font-size:4px;bottom:1px}}
}}

/* ===== Scrollbar ===== */
.grid-container::-webkit-scrollbar{{width:5px}}
.grid-container::-webkit-scrollbar-track{{background:#0f0f1a}}
.grid-container::-webkit-scrollbar-thumb{{background:#333;border-radius:3px}}
.grid-container::-webkit-scrollbar-thumb:hover{{background:#555}}

/* Keyhole — subtle vignette overlay for depth */
.grid-container::after{{
  content:"";position:fixed;inset:0;top:50px;
  box-shadow:inset 0 0 120px 30px rgba(0,0,0,.35);
  pointer-events:none;z-index:500;
}}
</style>
</head>
<body>

<div class="title-bar">
  <h1>思想的罐头工厂 · Warhol Grid</h1>
  <span class="count">10,367 cans</span>
</div>

<div class="legend">
''' + ''.join(f'''  <div class="legend-item"><span class="legend-swatch" style="background:{c['color']}"></span>{c['label']}<span class="legend-count">{cat_counts[i]}</span></div>
''' for i, c in enumerate(categories)) + '''</div>

<div class="grid-container">
<div class="grid" id="grid"></div>
</div>

<script>
var CATEGORIES=''' + categories_json + ''';
var ENTITIES=''' + entities_json + ''';

!function(){{
  var grid=document.getElementById('grid');
  var catNames=CATEGORIES.map(function(c){{return c.id}});
  var catColors=CATEGORIES.map(function(c){{return c.color}});
  var catLabels=CATEGORIES.map(function(c){{return c.label}});
  var fragment=document.createDocumentFragment();
  var prevCat=-1,total=ENTITIES.length;

  for(var i=0;i<total;i++){{
    var e=ENTITIES[i],name=e[0],catIdx=e[1];
    if(catIdx!==prevCat){{
      var d=document.createElement('div');
      d.className='cat-divider';
      d.style.color=catColors[catIdx];
      d.textContent=catLabels[catIdx]+' · '+catNames[catIdx];
      fragment.appendChild(d);
      prevCat=catIdx;
    }}
    var card=document.createElement('div');
    card.className='card';
    card.style.backgroundColor=catColors[catIdx];
    var t=document.createElement('span');
    t.className='card-text';t.textContent=name;card.appendChild(t);
    var cl=document.createElement('span');
    cl.className='card-cat';cl.textContent=catLabels[catIdx];card.appendChild(cl);
    fragment.appendChild(card);
  }}
  grid.appendChild(fragment);
  console.log('%cWarhol Grid%c '+total+' cards · 7 categories · ready',
    'font-weight:900;color:#fff;background:#a855f7;padding:2px 6px;border-radius:3px','');
}}();
</script>
</body>
</html>
'''

out_path = os.path.join(BASE, 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(out_path) / 1024
print(f"Written {out_path} ({size_kb:.0f} KB)")
