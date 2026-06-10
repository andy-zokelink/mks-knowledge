#!/usr/bin/env python3
"""Generate all HTML files for 科技参考3 MKS"""

import json, os, re, textwrap

OUT_DIR = '/home/admin/mks-knowledge/科技参考3'

with open(os.path.join(OUT_DIR, 'articles_categorized.json'), 'r') as f:
    articles = json.load(f)

# ============================================================
# TOPIC DEFINITIONS (final)
# ============================================================
TOPICS = {
    "1-AI与芯片革命": {
        "title": "AI与芯片革命",
        "subtitle": "大模型、半导体与智能时代的底层博弈",
        "icon": "🤖",
        "slug": "1-AI与芯片革命",
        "filename": "1-AI与芯片革命.html",
        "desc": "从GPT到Sora，从英伟达到EUV光刻机，人工智能与芯片技术正在重塑人类文明的底层逻辑。75篇文章覆盖AI大模型原理、芯片制造博弈、智能驾驶演进与AI安全等核心议题。",
        "color": "#F59E0B",
        "bg_card": "#FFFDF7",
    },
    "2-航天与太空探索": {
        "title": "航天与太空探索",
        "subtitle": "从星舰到月球基地，人类走出地球的征途",
        "icon": "🚀",
        "slug": "2-航天与太空探索",
        "filename": "2-航天与太空探索.html",
        "desc": "SpaceX星舰的每一次发射、月球基地的务实规划、旅行者号的星际远航——航天科技正以前所未有的速度推进。20篇文章覆盖火箭技术、太空旅行与宇宙科学。",
        "color": "#F59E0B",
        "bg_card": "#FFFDF7",
    },
    "3-医学与健康前沿": {
        "title": "医学与健康前沿",
        "subtitle": "疾病机制、衰老研究与医疗突破",
        "icon": "🔬",
        "slug": "3-医学与健康前沿",
        "filename": "3-医学与健康前沿.html",
        "desc": "从癌症治疗到抗衰老研究，从朊病毒到超级细菌，现代医学正在分子层面重新理解生命。59篇文章深入探讨疾病的生物学机制、前沿疗法与健康科学的最新发现。",
        "color": "#F59E0B",
        "bg_card": "#FFFDF7",
    },
    "4-食品营养与安全": {
        "title": "食品营养与安全",
        "subtitle": "从餐桌到实验室，吃背后的科学真相",
        "icon": "🍽️",
        "slug": "4-食品营养与安全",
        "filename": "4-食品营养与安全.html",
        "desc": "代糖真的致癌吗？化工罐车装食用油有多严重？水果为什么越来越甜？44篇文章用科学方法审视食品安全、营养学争议与日常饮食决策，揭开「吃」这件事背后的科学逻辑。",
        "color": "#F59E0B",
        "bg_card": "#FFFDF7",
    },
    "5-消费品评测与避坑": {
        "title": "消费品评测与避坑",
        "subtitle": "科技消费品的理性选购指南",
        "icon": "🛒",
        "slug": "5-消费品评测与避坑",
        "filename": "5-消费品评测与避坑.html",
        "desc": "电动车、手机、家电、眼镜、降噪耳机……科技消费品琳琅满目，智商税无处不在。47篇文章提供基于科学原理与工程逻辑的选购方法论，帮你避开消费陷阱。",
        "color": "#F59E0B",
        "bg_card": "#FFFDF7",
    },
    "6-人类演化与文明进程": {
        "title": "人类演化与文明进程",
        "subtitle": "从尼安德特人到AI，人类如何走到今天",
        "icon": "🧬",
        "slug": "6-人类演化与文明进程",
        "filename": "6-人类演化与文明进程.html",
        "desc": "智人为什么战胜了尼安德特人？暴力如何在人类社会中消退？语言与文字如何涌现？32篇文章从演化生物学、人类学与历史维度审视人类文明的底层动力。",
        "color": "#F59E0B",
        "bg_card": "#FFFDF7",
    },
    "7-科学方法与认知论": {
        "title": "科学方法与认知论",
        "subtitle": "批判性思维、统计素养与知识生产机制",
        "icon": "📐",
        "slug": "7-科学方法与认知论",
        "filename": "7-科学方法与认知论.html",
        "desc": "统计学如何识破假唱？同行评议为何失效？什么才是可靠的知识？34篇文章聚焦科学方法论本身——我们如何知道我们知道的东西？知识与认知的边界在哪里？",
        "color": "#F59E0B",
        "bg_card": "#FFFDF7",
    },
}

# Group articles by topic
topic_articles = {t: [] for t in TOPICS}
for a in articles:
    t = a['topic']
    if t in topic_articles:
        topic_articles[t].append(a)

# Sort by sort_order within each topic
for t in topic_articles:
    topic_articles[t].sort(key=lambda a: a['sort_order'])

# ============================================================
# CONTENT CLEANING
# ============================================================
def clean_content(raw):
    """Clean and extract summary from article content"""
    if not raw:
        return ""
    # Remove greeting pattern
    text = re.sub(r'\$_IGET_USER_NAME_\$，你好。?\s*欢迎回到《科技参考》[第]?[一二三]?季?，我是卓克。?\s*', '', raw)
    text = re.sub(r'\$_IGET_USER_NAME_\$', '', text)
    text = re.sub(r'你好，我是卓克[，。]?', '', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    # Extract first meaningful paragraph (first 200 chars of cleaned content)
    # Split by newlines and take first non-empty paragraph
    paras = [p.strip() for p in text.split('\n') if p.strip() and len(p.strip()) > 20]

    summary = ''
    for p in paras[:3]:
        clean_p = re.sub(r'^\d+[\.\、\s]+', '', p)  # Remove leading numbers
        if len(clean_p) > 15:
            summary = clean_p[:280]
            if len(clean_p) > 280:
                summary += '...'
            break

    if not summary:
        summary = text[:200]

    # Extract key concepts (sentences with key indicators)
    key_sentences = []
    sentences = re.split(r'[。；]', text)
    for s in sentences:
        s = s.strip()
        if not s or len(s) < 20:
            continue
        # Look for sentences with key indicators
        if any(kw in s for kw in ['关键', '核心', '本质', '简单说', '结论', '重要',
                                     '实际上', '其实', '真正的', '最', '值得',
                                     '因为', '所以', '原因', '原理', '机制']):
            clean_s = s[:200]
            if len(clean_s) > 30 and clean_s not in key_sentences:
                key_sentences.append(clean_s)
        if len(key_sentences) >= 2:
            break

    return summary, key_sentences

# Process all articles
for a in articles:
    summary, key_sentences = clean_content(a.get('content', ''))
    a['summary'] = summary
    a['insights'] = key_sentences

# ============================================================
# COMMON CSS
# ============================================================
COMMON_CSS = '''/* ============================================================
   科技参考3 · MKS 知识主板
   设计：白底 + 琥珀色(#F59E0B)强调 + 卡片式布局
   纯 HTML/CSS，移动端响应式
   ============================================================ */

:root {
  --bg: #fafbfc;
  --card-bg: #ffffff;
  --accent: #F59E0B;
  --accent-dark: #D97706;
  --accent-light: #FEF3C7;
  --text: #1f2937;
  --text-light: #6b7280;
  --text-lighter: #9ca3af;
  --border: #e5e7eb;
  --border-light: #f3f4f6;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
  --shadow: 0 2px 12px rgba(0,0,0,0.07);
  --shadow-lg: 0 8px 30px rgba(0,0,0,0.10);
  --radius: 12px;
  --radius-sm: 8px;
  --transition: 0.2s ease;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: "Noto Serif SC", "Source Han Serif SC", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.75;
  min-height: 100vh;
}

a { color: var(--accent-dark); text-decoration: none; transition: color var(--transition); }
a:hover { color: var(--accent); }

/* ============================================================
   TOP NAV BAR
   ============================================================ */
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 10px 20px;
  display: flex; align-items: center; gap: 16px;
  flex-wrap: wrap;
}
.top-nav .home-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 16px;
  background: var(--accent);
  color: #fff;
  border-radius: 20px;
  font-size: 13px; font-weight: 600;
  border: none; cursor: pointer;
  text-decoration: none;
  transition: all var(--transition);
}
.top-nav .home-btn:hover {
  background: var(--accent-dark);
  color: #fff;
}
.top-nav .breadcrumb {
  font-size: 13px; color: var(--text-light);
}

/* ============================================================
   MAIN CONTAINER
   ============================================================ */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 20px 60px;
}

/* ============================================================
   INDEX PAGE — HERO
   ============================================================ */
.hero {
  text-align: center;
  padding: 40px 16px 32px;
}
.hero .icon-row {
  font-size: 48px;
  margin-bottom: 12px;
}
.hero h1 {
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  font-weight: 900;
  color: var(--text);
  letter-spacing: 0.04em;
  margin-bottom: 8px;
}
.hero h1 .accent {
  color: var(--accent-dark);
}
.hero .subtitle {
  font-size: clamp(0.85rem, 1.5vw, 1rem);
  color: var(--text-light);
  margin-bottom: 4px;
}
.hero .meta {
  font-size: 0.8rem;
  color: var(--text-lighter);
}

/* Divider */
.divider {
  display: flex; align-items: center; gap: 16px;
  margin: 0 auto 40px;
  max-width: 600px;
}
.divider::before, .divider::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
}
.divider .dot {
  width: 8px; height: 8px;
  background: var(--accent);
  border-radius: 50%;
}

/* ============================================================
   INDEX — TOPIC CARDS GRID
   ============================================================ */
.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.topic-card {
  display: flex; flex-direction: column;
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  padding: 28px 24px 24px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.topic-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent), var(--accent-dark));
  border-radius: 0 0 2px 2px;
}
.topic-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent);
}
.topic-card .card-icon {
  font-size: 36px;
  margin-bottom: 12px;
}
.topic-card h3 {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}
.topic-card .card-subtitle {
  font-size: 0.82rem;
  color: var(--accent-dark);
  margin-bottom: 10px;
  font-weight: 500;
}
.topic-card .card-desc {
  font-size: 0.88rem;
  color: var(--text-light);
  line-height: 1.65;
  flex: 1;
}
.topic-card .card-count {
  margin-top: 14px;
  font-size: 0.78rem;
  color: var(--text-lighter);
  display: flex; align-items: center; gap: 6px;
}
.topic-card .card-count .badge {
  display: inline-block;
  background: var(--accent-light);
  color: var(--accent-dark);
  padding: 2px 10px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.75rem;
}

/* ============================================================
   TOPIC PAGE — HEADER
   ============================================================ */
.topic-header {
  text-align: center;
  padding: 30px 16px 24px;
}
.topic-header .topic-icon {
  font-size: 44px;
  margin-bottom: 8px;
}
.topic-header h2 {
  font-size: clamp(1.4rem, 2.5vw, 1.9rem);
  font-weight: 900;
  color: var(--text);
  margin-bottom: 4px;
}
.topic-header .topic-subtitle {
  font-size: 0.95rem;
  color: var(--accent-dark);
  font-weight: 500;
  margin-bottom: 8px;
}
.topic-header .topic-desc {
  font-size: 0.88rem;
  color: var(--text-light);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.7;
}

/* Stats row */
.stats-row {
  display: flex; gap: 12px; flex-wrap: wrap;
  justify-content: center;
  margin: 20px 0;
}
.stat-badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 24px;
  font-size: 0.82rem;
  color: var(--text-light);
}
.stat-badge .num {
  font-weight: 700;
  color: var(--accent-dark);
  font-size: 1rem;
}

/* ============================================================
   ARTICLE CARDS
   ============================================================ */
.articles-list {
  display: flex; flex-direction: column;
  gap: 14px;
  margin-top: 20px;
}

.article-card {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  padding: 20px 24px;
  transition: all var(--transition);
  border-left: 4px solid transparent;
}
.article-card:hover {
  box-shadow: var(--shadow);
  border-left-color: var(--accent);
}
.article-card .art-num {
  display: inline-block;
  font-size: 0.7rem;
  color: var(--text-lighter);
  background: var(--border-light);
  padding: 2px 8px;
  border-radius: 10px;
  margin-bottom: 6px;
  font-family: monospace;
}
.article-card h4 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 6px;
  line-height: 1.4;
}
.article-card .art-summary {
  font-size: 0.85rem;
  color: var(--text-light);
  line-height: 1.65;
  margin-bottom: 8px;
}
.article-card .art-insights {
  display: flex; flex-wrap: wrap; gap: 6px;
}
.article-card .insight-tag {
  font-size: 0.75rem;
  color: var(--accent-dark);
  background: var(--accent-light);
  padding: 2px 10px;
  border-radius: 12px;
}

/* ============================================================
   KEY CONCEPTS section
   ============================================================ */
.section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text);
  margin: 40px 0 20px;
  padding-bottom: 10px;
  border-bottom: 3px solid var(--accent);
  display: inline-block;
}
.concepts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
  margin-top: 16px;
}
.concept-card {
  background: var(--card-bg);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  padding: 16px 20px;
  transition: all var(--transition);
}
.concept-card:hover {
  box-shadow: var(--shadow);
  border-color: var(--accent);
}
.concept-card .concept-num {
  display: inline-block;
  width: 28px; height: 28px; line-height: 28px;
  text-align: center;
  background: var(--accent);
  color: #fff;
  border-radius: 50%;
  font-size: 0.8rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.concept-card h5 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 6px;
}
.concept-card p {
  font-size: 0.82rem;
  color: var(--text-light);
  line-height: 1.6;
}

/* ============================================================
   FOOTER
   ============================================================ */
.footer {
  text-align: center;
  padding: 32px 20px 16px;
  color: var(--text-lighter);
  font-size: 0.72rem;
  border-top: 1px solid var(--border-light);
  margin-top: 48px;
}
.footer a { color: var(--accent-dark); }

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 768px) {
  .topics-grid {
    grid-template-columns: 1fr;
  }
  .container {
    padding: 16px 12px 40px;
  }
  .article-card {
    padding: 16px;
  }
  .hero {
    padding: 24px 12px 20px;
  }
  .top-nav {
    padding: 8px 12px;
    gap: 10px;
  }
  .concepts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .topics-grid,
  .concepts-grid {
    grid-template-columns: 1fr;
  }
  .topic-card {
    padding: 20px 16px;
  }
  .article-card h4 {
    font-size: 0.92rem;
  }
}
'''

# ============================================================
# GENERATE INDEX.HTML
# ============================================================
def gen_index():
    cards_html = ''
    for tkey in TOPICS:
        t = TOPICS[tkey]
        count = len(topic_articles[tkey])
        cards_html += f'''
    <a href="{t['filename']}" class="topic-card">
      <div class="card-icon">{t['icon']}</div>
      <h3>{t['title']}</h3>
      <div class="card-subtitle">{t['subtitle']}</div>
      <div class="card-desc">{t['desc']}</div>
      <div class="card-count">
        <span class="badge">{count} 篇文章</span>
      </div>
    </a>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>科技参考3 · 卓克 · MKS 知识主板</title>
<style>
{COMMON_CSS}
</style>
</head>
<body>

<div class="top-nav">
  <a href="../index.html" class="home-btn">← 返回知识总库</a>
  <span class="breadcrumb">卓克 · 科技参考3</span>
</div>

<div class="container">
  <div class="hero">
    <div class="icon-row">🔬🚀🤖🧬📐</div>
    <h1>卓克 · <span class="accent">科技参考3</span></h1>
    <p class="subtitle">311篇精选 · 七大知识领域 · 最小知识集</p>
    <p class="meta">2023-2024年度 · 科技前沿与科学思维的系统梳理</p>
  </div>

  <div class="divider"><div class="dot"></div></div>

  <div class="topics-grid">
    {cards_html}
  </div>

  <footer class="footer">
    <p>卓克 · 科技参考3 · MKS 最小知识集 · <a href="../index.html">返回知识总库</a></p>
    <p>共 311 篇文章，覆盖 7 大知识领域</p>
  </footer>
</div>

</body>
</html>'''

    with open(os.path.join(OUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("Generated: index.html")

# ============================================================
# GENERATE TOPIC PAGES
# ============================================================
def gen_topic_page(tkey):
    t = TOPICS[tkey]
    arts = topic_articles[tkey]

    # Generate article cards
    article_cards = ''
    for i, a in enumerate(arts, 1):
        title = a['title']
        # Clean title (remove leading numbers like "001｜")
        clean_title = re.sub(r'^\d+\s*[｜|]\s*', '', title)
        summary = a.get('summary', '')
        insights = a.get('insights', [])[:2]

        insight_tags = ''
        for ins in insights:
            safe_ins = ins[:120]
            insight_tags += f'<span class="insight-tag">{html_mod.escape(safe_ins)}</span>\n'

        article_cards += f'''
      <div class="article-card">
        <span class="art-num">#{a['sort_order']}</span>
        <h4>{html_mod.escape(clean_title)}</h4>
        <div class="art-summary">{html_mod.escape(summary)}</div>
        {f'<div class="art-insights">{insight_tags}</div>' if insight_tags else ''}
      </div>'''

    # Generate key concept cards (from article titles grouped by sub-themes)
    # Extract concepts from article titles
    concepts = []
    for a in arts:
        clean_title = re.sub(r'^\d+\s*[｜|]\s*', '', a['title'])
        clean_title = re.sub(r'^问答：', '', clean_title)
        clean_title = re.sub(r'^追踪：', '', clean_title)
        # Split on common separators
        parts = re.split(r'[：:？?]+', clean_title)
        for p in parts:
            p = p.strip()
            if 4 <= len(p) <= 40 and '｜' not in p:
                concepts.append(p)

    # Deduplicate and pick top concepts
    from collections import Counter
    concept_counts = Counter(concepts)
    top_concepts = [(c, n) for c, n in concept_counts.most_common(15) if n >= 1][:12]

    concept_cards = ''
    for j, (concept, count) in enumerate(top_concepts, 1):
        concept_cards += f'''
      <div class="concept-card">
        <div class="concept-num">{j}</div>
        <h5>{html_mod.escape(concept)}</h5>
        <p>相关文章 {count} 篇</p>
      </div>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t['title']} — 科技参考3 MKS</title>
<style>
{COMMON_CSS}
</style>
</head>
<body>

<div class="top-nav">
  <a href="index.html" class="home-btn">← 科技参考3 主板</a>
  <span class="breadcrumb">{t['title']} · {len(arts)} 篇文章</span>
</div>

<div class="container">
  <div class="topic-header">
    <div class="topic-icon">{t['icon']}</div>
    <h2>{t['title']}</h2>
    <p class="topic-subtitle">{t['subtitle']}</p>
    <p class="topic-desc">{t['desc']}</p>
  </div>

  <div class="stats-row">
    <div class="stat-badge"><span class="num">{len(arts)}</span> 篇文章</div>
    <div class="stat-badge">📅 2023-2024</div>
    <div class="stat-badge">🎯 MKS 最小知识集</div>
  </div>

  <!-- Key Concepts -->
  <div class="section-title">核心概念</div>
  <div class="concepts-grid">
    {concept_cards}
  </div>

  <!-- Article List -->
  <div class="section-title">全部文章</div>
  <div class="articles-list">
    {article_cards}
  </div>

  <footer class="footer">
    <p><a href="index.html">← 返回科技参考3 主板</a> · 卓克 · 科技参考3 · MKS</p>
  </footer>
</div>

</body>
</html>'''

    filepath = os.path.join(OUT_DIR, t['filename'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: {t['filename']} ({len(arts)} articles)")

# ============================================================
# GENERATE ALL
# ============================================================
import html as html_mod

gen_index()
for tkey in TOPICS:
    gen_topic_page(tkey)

print("\nAll HTML files generated successfully!")
print(f"Output directory: {OUT_DIR}")
print(f"Files: index.html + {len(TOPICS)} topic pages")
