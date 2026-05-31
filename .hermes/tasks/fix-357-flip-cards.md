# MKS 翻修需求：投资与财富 / 艺术审美与品味 / 职场与人生智慧

## 问题诊断

三个文件（3、5、7）是用旧版/无模板生成的，**完全没有翻转卡片功能**：
- 无 `.flip-card`/`.flip-inner` CSS 3D 翻转样式
- 无 `setCard()` / `markLearned()` / `prevCard()` / `nextCard()` JS 函数
- 无翻转卡片对应的 HTML 结构（flip-inner/flip-front/flip-back + 翻页按钮）
- 导航标签可能也是旧格式（概念卡片/关系图/Socratic问答 等）

对比：`1-科技与商业逻辑.html` 和 `4-历史与文明对话.html` 是正常工作的标准模板。

## 待修文件（按金标准模板）

| 文件 | 路径 | 概念数 | 已知特殊问题 |
|------|------|--------|------------|
| 3-投资与财富.html | `/home/admin/mks-knowledge/硅谷来信1_v2/3-投资与财富.html` | 10个 | 卡片正反面空白 |
| 5-艺术审美与品味.html | `/home/admin/mks-knowledge/硅谷来信1_v2/5-艺术审美与品味.html` | 10个 | 不能点击/样式不对 |
| 7-职场与人生智慧.html | `/home/admin/mks-knowledge/硅谷来信1_v2/7-职场与人生智慧.html` | 10个 | 不能点击/样式不对 |

## 修改目标（三个文件统一对齐的标准）

### 必须以 `4-历史与文明对话.html` 为翻转卡片金标准

文件 4 的翻转卡片是唯一正确的参考——CSS/HTML/JS 三层全部对齐。文件 1 虽然能用但机制不同（无 3D 翻转）。

### 必须遵守的规范

全部从 `.claude/skills/mks-builder.md` 读取，关键点：

1. **翻转卡片 CSS（强制）**：
```css
.flip-card{perspective:1000px;height:clamp(220px,40vw,280px);margin-bottom:14px}
.flip-inner{position:relative;width:100%;height:100%;transition:transform .6s;transform-style:preserve-3d;cursor:pointer}
.flip-inner.flipped{transform:rotateY(180deg)}
.flip-front,.flip-back{position:absolute;width:100%;height:100%;backface-visibility:hidden;...}
.flip-back{...;transform:rotateY(180deg);overflow-y:auto;align-items:flex-start;text-align:left}
```

2. **翻转卡片 HTML（强制结构）**：
```html
<div class="flip-card"><div class="flip-inner" id="flipInner">
  <div class="flip-front" id="flipFront"></div>
  <div class="flip-back" id="flipBack"></div>
</div></div>
<div class="flip-nav">
  <button onclick="prevCard()">← 上一张</button>
  <span id="cardIndex">1 / N</span>
  <button onclick="nextCard()">下一张 →</button>
</div>
<button onclick="markLearned()" id="markLearnedBtn">✓ 标记已学习</button>
<div class="progress-bar"><div class="progress-fill" id="cardProgress"></div></div>
<p>已学习 <span id="cardLearned">0</span> / N 个概念</p>
```

3. **翻转卡片 JS（强制函数名和 ID）**：
- 函数名：`setCard()`（不是 renderCard/renderFlipCard）
- ID：`flipInner`、`flipFront`、`flipBack`、`cardIndex`、`markLearnedBtn`、`cardProgress`、`cardLearned`
- 翻转仅通过 `flipInner.addEventListener('click')`，**禁止** inline `onclick`
- 概念数组 `concepts`，每个条目有 `id:'cN'`、`name`、`def`、`analogy`、`example`、`counter`

4. **导航标签（9个，固定顺序）**：
知识集总览 → 知识卡片 → 题库系统 → 考试模式 → 复习模式 → 思维导图 → 深度追问 → 案例分析 → 实战决策

5. **知识集总览（7子项）**：
核心目标、核心概念、最小知识集、概念关系图、边界知识表、学习路径、学习进度

6. **暖色系**：--bg:#fdf6ec --card:#fffaf2 --accent:#c0392b

7. **JS 禁止项**：
- 中文弯引号 → ASCII 直引号
- `transform: none !important`
- `position: relative` 在 flip 元素上
- `min-height` 在 flip 元素上
- 旧 ID 残留（flipper/cardIdx/learnedBtn/flipCounter）

8. **MCQ**：20题，答案 {0:5,1:5,2:5,3:5} 严格均匀

## 工作方式

1. 先读 `4-历史与文明对话.html` 作为金标准模板
2. 读目标文件（3/5/7），提取所有独特内容（概念数据、MCQ、简答、案例、SVG数据等）
3. 用金标准模板结构 + 目标文件独特内容，生成新的 HTML
4. 覆盖写入原路径（`硅谷来信1_v2/` 目录）
5. 每个文件完成后跑 validator：`node ~/.hermes/skills/note-taking/mks-builder/scripts/validate_mks_html.js <file>`
6. 三个文件全部验证通过后通知

## 验收条件

- validator 全部通过
- 翻转卡片可点击翻转（正面→背面）
- 翻页按钮正常工作
- 9个标签页全部可切换且无空白
- 知识集总览 7子项齐全
- 暖色系
- JS 无语法错误、无弯引号
- 概念关系图用 Graphviz dot，禁止手写 SVG 坐标
