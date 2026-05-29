# 谷歌方法论 MKS 样式规范

> 以「世界名校」为黄金模板，所有专题页必须对齐。
> 本规范作为 Claude Code 生成 + Hermes 验收的统一标准。

---

## 一、全局基础

### 1.1 CSS 变量（:root）
```css
--bg: #fdf6ec;           /* 页面背景 */
--card: #fffaf2;         /* 卡片背景 */
--accent: #c0392b;       /* 主色：标题、按钮、强调 */
--accent2: #d4a574;      /* 辅色：分割线、hover边框 */
--text: #3d2f2f;         /* 正文 */
--text2: #6b5555;        /* 次要文字 */
--border: #e8d5c0;       /* 边框 */
--gold: #b8860b;         /* MKS核心概念标记色 */
--shadow: 0 2px 12px rgba(60,30,20,.08);
--radius: 12px;
```

### 1.2 字体
```
font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
font-size: clamp(14px, 1.2vw, 17px);   /* 根字号 */
line-height: 1.7;
color: var(--text);
background: var(--bg);
```

### 1.3 容器
```css
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 clamp(12px, 3vw, 24px);
}
```

---

## 二、页头 Header

### 2.1 结构
```html
<header>
  <h1>吴军·谷歌方法论 — [专题名]</h1>
  <div class="sub">最小知识集 · [N]篇笔记提炼 | [一句话描述]</div>
  <a href="index.html" class="home-link">← 返回知识主板</a>
</header>
```

### 2.2 样式
| 元素 | 字号 | 颜色 | 其他 |
|---|---|---|---|
| h1 | clamp(1.5rem, 3.5vw, 2rem) | var(--accent) | margin-bottom: 8px |
| .sub | clamp(.85rem, 1.5vw, .95rem) | var(--text2) | |
| .home-link | .88rem | var(--accent) | border: 2px solid var(--accent); border-radius: 20px; padding: 6px 20px; |
| .home-link:hover | -- | #fff | background: var(--accent) |

### 2.3 强制检查
- [ ] href 必须是 `index.html`（不是 `#`）
- [ ] 不允许 `onclick` 拦截事件
- [ ] 文本统一为「← 返回知识主板」

---

## 三、标签导航 `.tab-bar`

### 3.1 9 个标签（固定）
```
知识集总览 | 知识卡片 | 题库系统 | 考试模式 | 复习模式 | 思维导图 | 深度追问 | 案例分析 | 实战决策
```

### 3.2 样式
```css
.tab-bar {
  position: sticky; top: 0; z-index: 100;
  display: flex; flex-wrap: wrap; gap: 4px;
  padding: 8px clamp(4px, 1vw, 12px);
  background: rgba(253,246,236,.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
  justify-content: center;
}
.tab-btn {
  padding: 7px 14px; border: none; border-radius: 18px;
  background: var(--card); color: var(--text2);
  font-size: .8rem; cursor: pointer;
  border: 1px solid transparent;
}
.tab-btn:hover { border-color: var(--accent2); color: var(--accent); }
.tab-btn.active { background: var(--accent); color: #fff; }
```

### 3.3 移动端
```css
@media(max-width: 640px) {
  .tab-bar { gap: 2px; padding: 6px 2px; }
  .tab-btn { padding: 5px 8px; font-size: .7rem; border-radius: 14px; }
}
```

---

## 四、知识集总览（Tab 0）

### 4.1 7 个子项（固定顺序）
1. 核心目标
2. 核心概念
3. 最小知识集
4. 概念关系图（Graphviz dot 生成，.svg-wrap 包裹）
5. 边界知识表（.boundary-table 或 .tbl）
6. 学习路径（.path-steps > .path-step）
7. 学习进度（.progress-wrap）

### 4.2 概念关系图
- 使用 Graphviz `dot` 布局引擎渲染 SVG
- 禁止手写 SVG 坐标
- 外层 `.svg-wrap { overflow-x: auto; }`，移动端可横向滚动
- SVG `min-width: 700px`，图表上方须有 `.legend` 图例

### 4.3 进度条
```css
.progress-wrap { margin: 16px 0; }
.progress-bar { height: 10px; border-radius: 5px; background: var(--border); overflow: hidden; }
.progress-fill { height: 100%; border-radius: 5px; background: linear-gradient(90deg, var(--accent2), var(--accent)); transition: width .5s; }
.progress-label { font-size: .78rem; color: var(--text2); margin-top: 4px; }
```

---

## 五、概念卡片 `.concept-card`

### 5.1 样式
```css
.concept-card {
  background: var(--card); border-radius: var(--radius);
  padding: 16px; box-shadow: var(--shadow);
  border-left: 4px solid var(--accent);
  transition: transform .2s;
}
.concept-card:hover { transform: translateY(-2px); }
.concept-card.mks { border-left-color: var(--gold); position: relative; }
.concept-card.mks::after {
  content: '★'; position: absolute; top: 8px; right: 12px;
  color: var(--gold); font-size: 1.2rem;
}
.concept-card h4 { font-size: .95rem; color: var(--accent); margin-bottom: 6px; }
.concept-card p { font-size: .82rem; color: var(--text2); line-height: 1.5; }
```

### 5.2 网格布局
```css
.grid2 { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
.grid3 { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
.grid4 { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
```
移动端全部降为 `grid-template-columns: 1fr`。

---

## 六、翻转卡片 `.flip-container`

### 6.1 标准结构
```html
<div class="flip-container">
  <div class="flip-inner" onclick="this.parentElement.classList.toggle('flipped')">
    <div class="flip-front">[概念名+设计]</div>
    <div class="flip-back">
      <div class="dim-label">定义</div><p>...</p>
      <div class="dim-label">类比</div><p>...</p>
      <div class="dim-label">示例</div><p>...</p>
      <div class="dim-label">反例</div><p>...</p>
    </div>
  </div>
</div>
<div class="flip-nav">
  <button onclick="prevCard()">◀</button>
  <button onclick="markLearned()">✓ 已掌握</button>
  <button onclick="nextCard()">▶</button>
</div>
```

### 6.2 关键 CSS
```css
.flip-container { perspective: 1000px; width: 100%; max-width: 500px; margin: 20px auto; }
.flip-inner { position: relative; width: 100%; height: 300px; transition: transform .6s; transform-style: preserve-3d; cursor: pointer; }
.flip-inner.flipped { transform: rotateY(180deg); }
.flip-front, .flip-back {
  position: absolute; width: 100%; height: 100%;
  backface-visibility: hidden; border-radius: var(--radius);
  display: flex; flex-direction: column; padding: 24px;
  box-shadow: var(--shadow);
}
.flip-front {
  background: linear-gradient(135deg, var(--accent), #a93226);
  color: #fff; font-size: 1.3rem; font-weight: 700;
  align-items: center; justify-content: center; text-align: center;
}
.flip-back {
  background: var(--card); color: var(--text);
  transform: rotateY(180deg);
  align-items: flex-start; text-align: left;
  overflow-y: auto; font-size: .85rem; line-height: 1.6;
}
.flip-back .dim-label { font-weight: 700; color: var(--accent); font-size: .8rem; }
.flip-nav { display: flex; justify-content: center; gap: 16px; margin-top: 12px; }
.flip-nav button {
  padding: 8px 20px; border-radius: 20px;
  border: 2px solid var(--accent); background: var(--card);
  color: var(--accent); cursor: pointer; font-size: .85rem;
}
.flip-nav button:hover { background: var(--accent); color: #fff; }
.flip-nav button.learned { background: #e8f5e9; border-color: #4caf50; color: #2e7d32; }
```

### 6.3 移动端
```css
@media(max-width: 640px) {
  .flip-inner { height: 320px; }
  .flip-front { font-size: 1.1rem; }
}
```

### 6.4 强制检查
- [ ] 翻转后背面 `overflow-y: auto`，内容多时可滚动
- [ ] `.flip-nav` 不在 `.flip-inner` 内部，不会被翻转
- [ ] 翻转后翻页按钮不被遮挡（`.flip-inner` 高度 ≥ 300px）
- [ ] 正面仅概念名+美观设计，反面四段式（定义/类比/示例/反例）

---

## 七、题库系统 `.quiz-card`

### 7.1 选择题
```html
<div class="quiz-card">
  <span class="q-tag q-mc">选择题</span>
  <div class="q-text">题目文字...</div>
  <div class="q-option" onclick="selectMC(this, 0)">A. 选项A</div>
  <div class="q-option" onclick="selectMC(this, 1)">B. 选项B</div>
  <div class="q-option" onclick="selectMC(this, 2)">C. 选项C</div>
  <div class="q-option" onclick="selectMC(this, 3)">D. 选项D</div>
  <div class="q-feedback right/wrong-msg">反馈文字</div>
</div>
```

### 7.2 选择题样式
```css
.quiz-card { background: var(--card); border-radius: var(--radius); padding: 20px; box-shadow: var(--shadow); margin-bottom: 14px; }
.q-tag { font-size: .75rem; padding: 3px 10px; border-radius: 8px; display: inline-block; margin-bottom: 8px; }
.q-mc { background: #fde8e8; color: var(--accent); }
.q-sa { background: #e8f0fe; color: #3a6ea5; }
.q-text { font-weight: 700; margin-bottom: 12px; }
.q-option { padding: 8px 14px; margin: 4px 0; border-radius: 8px; cursor: pointer; border: 1px solid var(--border); font-size: .85rem; transition: all .2s; }
.q-option:hover { border-color: var(--accent2); background: #fef9f4; }
.q-option.selected { border-color: var(--accent); background: #fde8e8; }
.q-option.correct { border-color: #4caf50; background: #e8f5e9; }    /* 选对或正解 */
.q-option.wrong { border-color: var(--accent); background: #ffebee; }   /* 选错 */
.q-feedback { margin-top: 8px; font-size: .82rem; padding: 8px; border-radius: 8px; display: none; }
.q-feedback.show { display: block; }
.q-feedback.right { background: #e8f5e9; color: #2e7d32; }
.q-feedback.wrong-msg { background: #ffebee; color: var(--accent); }
```

### 7.3 交互逻辑
- 点击选项 → 该选项变为 `.selected`，同时揭示正确答案（`.correct`）、标记错误选项（`.wrong`）
- 显示反馈 `.q-feedback.show`（正确用 `.right`，错误用 `.wrong-msg`）
- 点击后所有选项禁用
- MCQ 答案分布必须 `{0:5, 1:5, 2:5, 3:5}`（每页 20 题均匀分布）

### 7.4 简答题
```html
<textarea class="sa-input" placeholder="输入你的答案..."></textarea>
<button class="btn" onclick="checkSA(this)">对比参考答案</button>
<div class="sa-reveal">参考答案内容</div>
```

```css
.sa-input { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid var(--border); font-family: inherit; font-size: .85rem; resize: vertical; min-height: 80px; background: #fff; }
.sa-reveal { margin-top: 8px; padding: 10px; background: #fef9f4; border-radius: 8px; font-size: .82rem; display: none; }
.sa-reveal.show { display: block; }
```

---

## 八、考试模式

### 8.1 计时器
```css
.timer { font-size: 1.3rem; font-weight: 700; color: var(--accent); text-align: center; padding: 10px; }
.timer.warning { animation: pulse .5s infinite alternate; }
@keyframes pulse { from { opacity: 1; } to { opacity: .5; } }
```

### 8.2 统计面板
```css
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; }
.stat-card { text-align: center; padding: 16px; background: var(--card); border-radius: var(--radius); box-shadow: var(--shadow); }
.stat-card .num { font-size: 2rem; font-weight: 700; color: var(--accent); }
.stat-card .lbl { font-size: .78rem; color: var(--text2); margin-top: 4px; }
```

---

## 九、深度追问 `.socratic`

```css
.socratic-item { margin-bottom: 12px; }
.socratic-q { cursor: pointer; padding: 12px 16px; border-radius: var(--radius); background: var(--card); border: 1px solid var(--border); font-weight: 700; }
.socratic-q:hover { border-color: var(--accent2); }
.socratic-q::before { content: '❓ '; }
.socratic-a { display: none; padding: 12px 16px; background: #fef9f4; border-radius: 0 0 var(--radius) var(--radius); font-size: .85rem; color: var(--text2); }
```

---

## 十、实战决策 `.decision-round`

```css
.decision-round { background: var(--card); border-radius: var(--radius); padding: 20px; box-shadow: var(--shadow); margin-bottom: 16px; }
.decision-round .scenario { font-weight: 700; margin-bottom: 12px; color: var(--accent); }
.d-option { padding: 10px 14px; margin: 6px 0; border-radius: 8px; cursor: pointer; border: 1px solid var(--border); transition: all .2s; }
.d-option:hover { border-color: var(--accent2); background: #fef9f4; }
.d-option.chosen { border-color: var(--accent); background: #fde8e8; }
.d-result { display: none; margin-top: 12px; padding: 14px; border-radius: 8px; background: #fef9f4; font-size: .85rem; }
.d-result.show { display: block; }
```

---

## 十一、按钮系统

```css
.btn { padding: 10px 24px; border-radius: 20px; border: 2px solid var(--accent); background: var(--accent); color: #fff; cursor: pointer; font-size: .88rem; font-weight: 700; transition: all .2s; }
.btn:hover { background: #a93226; border-color: #a93226; }
.btn-outline { background: transparent; color: var(--accent); }
.btn-outline:hover { background: var(--accent); color: #fff; }
.btn-sm { padding: 6px 14px; font-size: .78rem; }
button:disabled { opacity: .5; cursor: not-allowed; }
```

---

## 十二、知识主板（index.html）

### 12.1 PCB 风格规格
- 深色背景: `#0a1a0a`，暗绿色调
- 组件 hover: `filter: brightness(1.25)` + glow 边框显形（`opacity: 0 → 1`）
- **禁止使用 `transform: scale()` 覆盖 SVG 的 `translate` 属性**
- 每个组件 `<g>` 必须有 `class="comp-body"` 在主矩形上
- 走线脉冲动画：`<animateMotion>` 在金色走线上来回

### 12.2 组件映射
| 组件 | 颜色 | 专题 | 链接 |
|---|---|---|---|
| CPU | #00e5ff | 计算机思维 | 7-计算机思维.html |
| RAM | #ffd700 | 硅谷与Google | 6-硅谷与Google.html |
| GPU | #ff00ff | 发明与创新 | 3-发明与创新.html |
| SSD | #00ff88 | 世界名校 | 1-世界名校.html |
| NIC | #ff8c00 | 投资与决策 | 4-投资与决策.html |
| +12V PSU | #ff4444 | 人生算法 | 2-人生算法.html |
| +5V PSU | #4488ff | 文明与全球化 | 5-文明与全球化.html |

### 12.3 强制检查
- [ ] 所有 7 个组件 `data-id` 正确
- [ ] `handleClick` 函数调用 `window.location.href = comp.link`
- [ ] 状态 LED 能持久化（localStorage）
- [ ] 移动端降级为卡片列表

---

## 十三、全局禁止项

1. **禁止** `href="#"` 或 `href="javascript:void(0)"` — 所有链接必须指向有效路径
2. **禁止** `onclick="alert(...)"` 或 `onclick="...return false"` 拦截导航
3. **禁止** 中文弯引号 `""` `''` — 必须使用 ASCII 直引号
4. **禁止** `transform: none !important` — 会破坏翻转卡片
5. **禁止** 手写 SVG 坐标做概念关系图 — 必须用 Graphviz dot
6. **禁止** `write_file` 工具读取部分文件后写回 — 会导致 JavaScript 截断
7. **禁止** 在翻转卡片的 `.flip-inner` 内部放置翻页按钮
8. **禁止** 固定像素宽度限制知识卡片（必须用 `max-width` + 百分比）

---

## 十四、验收检查清单

### 链接检查
- [ ] 7 个专题页 → 知识主板（href="index.html"）
- [ ] 知识主板 → 7 个专题页（点击跳转正常）
- [ ] 无 `#` 死链、无 `onclick` 拦截

### 翻转卡片
- [ ] 正面仅概念名，反面四段式
- [ ] 翻转后内容可滚动（overflow-y: auto）
- [ ] 翻页按钮在卡片下方不被遮挡
- [ ] 移动端高度 ≥ 320px

### 知识卡片
- [ ] 网格自适应（auto-fit, minmax）
- [ ] 移动端单列
- [ ] 内容不溢出、不截断

### 题库
- [ ] MCQ 正确标绿、错误标红
- [ ] 答题后禁用选项
- [ ] 简答题有输入框 + 参考答案对比

### 知识主板
- [ ] 7 个组件 hover 不抖动
- [ ] 点击跳转到正确专题
- [ ] 状态 LED 已访问持久化
- [ ] 移动端降级为卡片列表
