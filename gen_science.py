#!/usr/bin/env python3
"""卓克·科学思维课 MKS HTML 生成器
从 SQLite 读取 334 篇文章，分类为7个专题，生成 HTML 文件。
"""

import sqlite3
import html as html_mod
import re
import os
import json

DB_PATH = '/home/admin/zhuoke_data/dedao.db'
OUT_DIR = '/home/admin/mks-knowledge/科学思维课'
COURSE_ID = 'R2Eq7l8xrPkQvlMjaX9dk7vPq4Jkz8d'

# ============================================================
# 7 大专题定义
# ============================================================
TOPICS = [
    {
        'id': 1,
        'slug': '科学思维工具箱',
        'icon': '🧰',
        'subtitle': '极限 · 务实 · 数字 · 复杂 · 变量 · 模型 · 证据 · 计算',
        'desc': '掌握科学思维的底层工具箱：从数量级感知到模型构建，从极限思维到严谨测量——构建看待世界的"操作系统"。',
        'color': '#D97706',
        'match_concepts': ['极限', '务实', '数字', '复杂', '变量', '模型', '证据', '计算', '现代数学'],
        'match_titles': ['极限', '务实', '数字', '复杂', '变量', '模型', '证据', '计算', '现代数学', '严谨', '测量', '1米', '1千克', '角度'],
        'articles': []
    },
    {
        'id': 2,
        'slug': '演化与生命科学',
        'icon': '🧬',
        'subtitle': '真理 · 起源 · 旁证 · 宏观 · 演化',
        'desc': '从达尔文进化论到基因平移，从生命起源到物种灭绝，从人类迁徙到文明兴衰——用演化思维理解万物生灭的宏大叙事。',
        'color': '#059669',
        'match_concepts': ['真理', '起源', '旁证', '宏观'],
        'match_titles': ['进化论', '演化论', '基因平移', '转基因', '复活节岛', '食人族', '起源', '性别', '肤色', '冰雪覆盖',
                        '海洋', '五谷', '水稻', '家猫', '黑猩猩', '日本人', '语言', '文字', '人类祖先',
                        '物种大灭绝', '保护动物', '农业', '地理决定论', '族群', '技术裁决',
                        '旁证', '寻找衣服', '狗是怎么', '乌龟', '人类是怎么分布', '酵母菌',
                        '晒伤', '维生素D', '换头术', '科学共同体'],
        'articles': []
    },
    {
        'id': 3,
        'slug': '医学健康与人体',
        'icon': '🏥',
        'subtitle': '发展 · 疾病 · 免疫 · 衰老 · 问答精选',
        'desc': '从天花到HIV，从近视到癌症，从衰老机制到疫苗原理——用科学思维理解人体、疾病与健康的底层逻辑。',
        'color': '#DC2626',
        'match_concepts': ['发展', '衰老'],
        'match_titles': ['近视', '啤酒肚', '天花', 'HIV', '白血病', '植物人', '流感', '梅毒', '大脑的寿命',
                        '免疫力', '感冒', '分娩', '乙肝', '零热量', '蛋白粉', '黑眼圈', '减肥',
                        '肾虚', '带状疱疹', '朊病毒', '老寒腿', '秋裤', '皮肤瘙痒', '坐月子',
                        '基因检测', '大蒜杀菌', '晕车', '反季节', '偏头痛', '献血',
                        '猪肉', '抗生素', '养殖场', '口臭', 'Y染色体', '人会疼死',
                        '补钙', '贫血', '感冒药', '发物', '痛风', '食用油', '打呼噜',
                        '排毒', '排宿便', '干细胞', '充电宝', '狗权', '药酒',
                        '冥想', '灵修', 'Wi-Fi', '巧克力', '驱蚊', '抑郁症',
                        '颈椎病', '医院自制药', '葡萄籽', '面膜',
                        '衰老', '线粒体', '自由基', '端粒', '脑死亡', '死亡基因',
                        '体温', '细胞死亡', '癌症', '寿命', '细菌大小',
                        '跨鸿沟', '真核生物', '性别出现', '衰老假说'],
        'articles': []
    },
    {
        'id': 4,
        'slug': '破解伪科学与谬误',
        'icon': '🔍',
        'subtitle': '边界 · 泡沫 · 成瘾 · 谬误 · 流变',
        'desc': '识破伪科学、认知偏误和思维陷阱：从尼斯湖水怪到放血疗法，从潜意识神话到全球变暖争议——构建科学真相的防火墙。',
        'color': '#7C3AED',
        'match_concepts': ['边界', '泡沫', '成瘾', '谬误', '流变'],
        'match_titles': ['钢铁侠', '24帧', '恐怖记忆', '镜子', '绿色恒星', '情感',
                        '煤和石油', '石油', '尼斯湖', '民科', '伪科学', '神药',
                        '放血疗法', '牙膏', '太空长城', '马桶', '潜意识', '核辐射',
                        '海洛因', '网游', '毒品疫苗', '大脑电极', '全球变暖',
                        '催眠', '雷雨天', '空调', '1度电',
                        '信仰科学', '杨振宁', '抠鼻子', '搞笑诺贝尔', '面包',
                        '上帝假设', '物理学家挑衅', '圣经密码', '预测未来', '潜规则',
                        '真性情论文', '神话传说', '记忆力狂人', '最强大脑',
                        '科技威胁', '搜索引擎', '人为什么会信神', '宗教出现',
                        '颈椎病', '破除'],
        'articles': []
    },
    {
        'id': 5,
        'slug': '科学史与文明',
        'icon': '📜',
        'subtitle': '源头 · 遗憾 · 追赶 · 平凡 · 反省',
        'desc': '追溯科学诞生的历史脉络：从第一所大学到科学院，从中国科学的遗憾到追赶之路——理解科学如何塑造现代文明。',
        'color': '#0891B2',
        'match_concepts': ['源头', '遗憾', '追赶', '平凡', '反省'],
        'match_titles': ['大学', '科学院', '牛顿与胡克', '科学诞生', '天体运行论',
                        '明朝', '科学与宗教', '清朝', '康熙', '中国古代',
                        '中国科学', '留美幼童', '庚子赔款', '科学在中国',
                        '巨人肩膀', '科学家拉下神坛', '四大发明', '天文历法',
                        '利益左右', '自我审查', '海洋垃圾', '大脑可塑性'],
        'articles': []
    },
    {
        'id': 6,
        'slug': '心理学与认知科学',
        'icon': '🧠',
        'subtitle': '心理 · 味道 · 批判性思维 · 认知偏误',
        'desc': '从心理学科学化历程到双盲实验，从味觉演化到批判性思维——探索人类心智的运作规律与认知局限。',
        'color': '#E11D48',
        'match_concepts': ['心理', '味道', '批判性思维'],
        'match_titles': ['苦味', '滋味', '口味', '食欲', '良药苦口', '针灸',
                        '心理学', '安慰剂', '双盲', '相关性', '因果性', '梦境',
                        '演化角度看基因', '潜意识', '测量大脑', '阿尔茨海默', '病毒引发',
                        '批判性思维', '说服他人', '不说谎也能误导', '心理技巧'],
        'articles': []
    },
    {
        'id': 7,
        'slug': '前沿科学与总览',
        'icon': '🔭',
        'subtitle': '荣耀 · 诺贝尔奖 · 考古 · 加餐 · 全年总结',
        'desc': '诺贝尔奖深度解读、前沿科学发现、考古学思维、年度总结——站在科学最前沿，理解知识的边界与演进。',
        'color': '#4F46E5',
        'match_concepts': ['荣耀', '考古'],
        'match_titles': ['诺贝尔', '霍金', '引力波', '黎曼猜想', '黑洞', '密码学',
                        '全年总结', '复习手册', '加餐', '直播', '考古', '读心术',
                        '人类13万年', '代孕', '新课', '答疑合集',
                        '发刊词', '科学思维课-全年'],
        'articles': []
    }
]

def clean_summary(text, title):
    """从 content_text 提取干净摘要"""
    if not text:
        return ''

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove multiple newlines/blanks
    text = re.sub(r'\n{2,}', '\n', text)
    # Remove concept headers like "概念01：极限"
    text = re.sub(r'概念\d+[：:][^\n]*\n?', '', text)
    # Remove the article title if it appears at beginning
    title_clean = re.sub(r'^\d+\s*[｜|]\s*', '', title).strip()
    text = re.sub(r'^' + re.escape(title_clean) + r'\s*', '', text)
    text = re.sub(r'^' + re.escape(title) + r'\s*', '', text)
    # Remove leading whitespace
    text = text.strip()

    # Split into paragraphs, filter out boilerplate and too-short ones
    boilerplate = ['今天集中回答', '又到了问答时间', '今天我们来集中回答',
                   '这期节目', '欢迎收听', '你好，我是卓克',
                   '你好我是卓克', '大家好，我是卓克',
                   '问答时间', '本节课', '同学们好',
                   '概念', '模块', '复习手册',
                   '上期节目', '上节课', '上一讲',
                   '这节课我们', '这一讲我们', '今天这节课',
                   '今天是', '今天是问答', '又到问答时间']

    raw_paragraphs = [p.strip() for p in text.split('\n') if p.strip()]

    # Filter: skip paragraphs that are boilerplate, too short, or just punctuation
    meaningful = []
    for p in raw_paragraphs:
        p_clean = p.strip()
        if len(p_clean) < 20:
            continue
        if any(p_clean.startswith(b) for b in boilerplate):
            continue
        # Skip paragraphs that are mostly just the Q&A question format
        if re.match(r'^问答\d+', p_clean) or re.match(r'^问题[：:]', p_clean):
            continue
        # Skip "Q:" only paragraphs
        if p_clean.startswith('Q：') or p_clean.startswith('Q:'):
            continue
        meaningful.append(p_clean)

    if not meaningful:
        # Fallback: use raw paragraphs and take the longest non-boilerplate one
        for p in raw_paragraphs:
            if len(p) > 30 and not any(p.startswith(b) for b in boilerplate):
                meaningful.append(p)
                break

    if meaningful:
        # Combine paragraphs to reach ~200 chars target for good summary
        summary = ''
        for p in meaningful:
            if len(summary) < 180:
                if summary:
                    summary += ' '
                summary += p
            else:
                break
        # Truncate to reasonable final length
        if len(summary) > 300:
            summary = summary[:297] + '…'
        return summary

    # Ultimate fallback
    fallback = text.strip()[:280]
    return fallback if fallback else ''

def categorize_article(title, content_text, sort_order):
    """基于标题和内容将文章分类到专题"""
    title_lower = title.lower()
    content_first = (content_text or '')[:500]

    scores = []
    for topic in TOPICS:
        score = 0
        for kw in topic['match_titles']:
            if kw.lower() in title_lower:
                score += 10
        for kw in topic['match_concepts']:
            if kw in content_first:
                score += 5
        scores.append(score)

    # Find best match
    max_score = max(scores)
    if max_score > 0:
        best = scores.index(max_score)
        return best

    # Fallback: sort_order based ranges
    if sort_order <= 62:
        return 0  # 科学思维工具
    elif sort_order <= 107:
        return 1  # 演化与生命
    elif sort_order <= 148:
        return 2  # 医学健康
    elif sort_order <= 196:
        return 3  # 伪科学
    elif sort_order <= 252:
        return 4  # 科学史
    elif sort_order <= 297:
        return 5  # 心理学
    else:
        return 6  # 前沿

def extract_concept(text):
    """从 content_text 提取概念标签"""
    m = re.search(r'概念\d+[：:]([^\n]*)', text or '')
    if m:
        return m.group(1).strip()
    return ''

def generate_html_files():
    """主生成函数"""
    os.makedirs(OUT_DIR, exist_ok=True)

    # Read all articles
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT article_id, title, content_text, sort_order FROM articles WHERE course_id='{COURSE_ID}' ORDER BY sort_order")
    articles = cur.fetchall()
    conn.close()

    print(f"读取 {len(articles)} 篇文章")

    # Categorize
    for art in articles:
        article_id, title, content_text, sort_order = art
        topic_idx = categorize_article(title, content_text, sort_order)
        concept = extract_concept(content_text)
        summary = clean_summary(content_text, title)

        TOPICS[topic_idx]['articles'].append({
            'article_id': article_id,
            'title': title,
            'sort_order': sort_order,
            'concept': concept,
            'summary': summary
        })

    # Print distribution
    for t in TOPICS:
        print(f"  专题{t['id']}「{t['slug']}」: {len(t['articles'])} 篇")

    # Generate CSS
    generate_css()

    # Generate each topic HTML
    for topic in TOPICS:
        generate_topic_html(topic)

    # Generate index
    generate_index_html()

    print(f"\n✅ 生成完成！输出目录: {OUT_DIR}")

def generate_css():
    """生成独立的 CSS 文件"""
    css = '''/* ============================================================
   卓克·科学思维课 MKS — 白底琥珀色强调 · 卡片式布局 · 移动端响应式
   配色：白底(#fefcf8) + 琥珀(#F59E0B) + 深棕文字
   ============================================================ */
:root {
  --bg: #fefcf8;
  --card: #ffffff;
  --card-hover: #fffdf5;
  --amber: #F59E0B;
  --amber-light: #FEF3C7;
  --amber-dark: #B45309;
  --amber-ghost: rgba(245,158,11,0.08);
  --text: #3d2f1f;
  --text-mid: #5c4a32;
  --text-light: #8a7560;
  --border: #e8dcc8;
  --border-light: #f0e8d5;
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.05);
  --shadow: 0 4px 16px rgba(0,0,0,0.07);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.10);
  --radius: 12px;
  --radius-sm: 8px;
  --font-serif: "Noto Serif SC", "Source Han Serif SC", "PingFang SC", "Microsoft YaHei", serif;
  --font-sans: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: var(--font-serif);
  background: linear-gradient(180deg, #fefcf8 0%, #fdf8f0 30%, #fef9f4 60%, #fefcf8 100%);
  color: var(--text);
  line-height: 1.75;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

a { color: var(--amber-dark); text-decoration: none; transition: color 0.2s; }
a:hover { color: var(--amber); }

/* 顶部导航栏 */
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: linear-gradient(135deg, #3d2f1f 0%, #5a3e2e 100%);
  color: #fefcf8; padding: 10px 20px;
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.top-nav .brand { font-size: clamp(13px, 2vw, 15px); font-weight: 700; letter-spacing: 0.05em; white-space: nowrap; }
.top-nav .brand .icon { margin-right: 6px; }
.top-nav .home-btn {
  color: var(--amber); font-size: 13px;
  border: 1px solid var(--amber); padding: 4px 12px;
  border-radius: 20px; white-space: nowrap;
  transition: all 0.25s; font-family: var(--font-sans);
}
.top-nav .home-btn:hover { background: var(--amber); color: #3d2f1f; text-decoration: none; }

.container { max-width: 1000px; margin: 0 auto; padding: 0 20px 60px; }

/* 专题头部 */
.topic-header { text-align: center; padding: 40px 0 30px; }
.topic-header .icon { font-size: 48px; margin-bottom: 12px; display: block; }
.topic-header h1 { font-size: clamp(22px, 4vw, 32px); font-weight: 900; color: var(--amber-dark); letter-spacing: 0.06em; margin-bottom: 8px; }
.topic-header .subtitle { font-size: clamp(12px, 2vw, 14px); color: var(--text-light); letter-spacing: 0.08em; margin-bottom: 12px; }
.topic-header .desc { font-size: clamp(13px, 2.2vw, 15px); color: var(--text-mid); max-width: 640px; margin: 0 auto; line-height: 1.8; }

/* 分割线 */
.divider { display: flex; align-items: center; gap: 16px; max-width: 400px; margin: 0 auto 32px; }
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, transparent, var(--amber), transparent); }
.divider span { color: var(--amber); font-size: 20px; opacity: 0.7; }

/* 概念标签 */
.concept-tags { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 16px 0 24px; }
.concept-tag { display: inline-block; padding: 4px 14px; background: var(--amber-light); color: var(--amber-dark); border-radius: 14px; font-size: 12px; font-family: var(--font-sans); font-weight: 600; letter-spacing: 0.04em; }

/* 进度条 */
.progress-wrap { margin: 16px 0 24px; display: flex; align-items: center; gap: 10px; }
.progress-wrap .label { font-size: 12px; color: var(--text-light); white-space: nowrap; }
.progress-bar { flex: 1; height: 8px; background: var(--border-light); border-radius: 4px; overflow: hidden; }
.progress-bar .fill { height: 100%; background: linear-gradient(90deg, var(--amber), var(--amber-dark)); border-radius: 4px; }

/* 导航页网格 */
.nav-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 40px; }
.nav-card {
  background: var(--card); border-radius: var(--radius);
  border: 1px solid var(--border); box-shadow: var(--shadow-sm);
  padding: 24px 22px 20px; text-decoration: none; color: inherit;
  transition: all 0.3s; display: flex; flex-direction: column;
  position: relative; overflow: hidden;
}
.nav-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--amber), var(--amber-dark));
  border-radius: var(--radius) var(--radius) 0 0; opacity: 0; transition: opacity 0.3s;
}
.nav-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: var(--amber); }
.nav-card:hover::before { opacity: 1; }
.nav-card .card-icon { font-size: 36px; margin-bottom: 12px; }
.nav-card h2 { font-size: clamp(17px, 2.5vw, 20px); font-weight: 700; color: var(--amber-dark); margin-bottom: 6px; }
.nav-card .card-subtitle { font-size: 12px; color: var(--text-light); letter-spacing: 0.05em; margin-bottom: 10px; }
.nav-card .card-desc { font-size: 13px; color: var(--text-mid); line-height: 1.7; flex: 1; }
.nav-card .card-count { margin-top: 12px; font-size: 11px; color: var(--text-light); font-family: var(--font-sans); }
.nav-card .card-count span { display: inline-block; background: var(--amber-light); color: var(--amber-dark); padding: 2px 8px; border-radius: 10px; font-weight: 600; }

/* 课程头部 */
.course-header { text-align: center; padding: 48px 20px 32px; }
.course-header h1 { font-size: clamp(24px, 5vw, 40px); font-weight: 900; color: var(--amber-dark); letter-spacing: 0.08em; margin-bottom: 8px; }
.course-header .course-sub { font-size: clamp(13px, 2vw, 16px); color: var(--text-light); letter-spacing: 0.1em; }
.course-header .course-meta { margin-top: 12px; font-size: 13px; color: var(--text-mid); letter-spacing: 0.04em; }
.title-accent { display: inline-block; background: linear-gradient(180deg, #F59E0B 0%, #D97706 50%, #B45309 100%); color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-left: 8px; vertical-align: middle; letter-spacing: 0.05em; }

/* 文章区块 */
.article-section { margin-bottom: 32px; }
.article-section h2 { font-size: clamp(16px, 2.5vw, 20px); font-weight: 700; color: var(--amber-dark); margin-bottom: 16px; padding-bottom: 8px; border-bottom: 3px solid var(--amber); display: flex; align-items: center; gap: 8px; }
.article-section h2 .badge { font-size: 12px; background: var(--amber); color: #fff; padding: 2px 10px; border-radius: 12px; font-weight: 600; font-family: var(--font-sans); }
.article-card {
  background: var(--card); border-radius: var(--radius-sm);
  border: 1px solid var(--border-light); box-shadow: var(--shadow-sm);
  padding: 18px 20px; margin-bottom: 10px; transition: all 0.2s;
}
.article-card:hover { border-color: var(--amber); box-shadow: var(--shadow); background: var(--card-hover); }
.article-card .art-header { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; margin-bottom: 6px; }
.article-card .art-num { font-size: 11px; color: var(--amber); font-weight: 700; font-family: var(--font-sans); letter-spacing: 0.05em; white-space: nowrap; }
.article-card .art-title { font-size: clamp(14px, 2vw, 16px); font-weight: 600; color: var(--text); }
.article-card .art-concept { font-size: 10px; background: var(--amber-light); color: var(--amber-dark); padding: 1px 8px; border-radius: 8px; font-family: var(--font-sans); white-space: nowrap; }
.article-card .art-summary { font-size: 13px; color: var(--text-mid); line-height: 1.7; }

/* 关键概念框 */
.concept-box { background: var(--amber-light); border-left: 4px solid var(--amber); border-radius: 0 var(--radius-sm) var(--radius-sm) 0; padding: 16px 20px; margin: 20px 0; }
.concept-box h3 { font-size: 14px; color: var(--amber-dark); font-weight: 700; margin-bottom: 8px; }
.concept-box p, .concept-box li { font-size: 13px; color: var(--text-mid); line-height: 1.8; }

/* 统计 */
.stats-row { display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; margin: 20px 0; }
.stat-item { text-align: center; padding: 16px 24px; background: var(--card); border-radius: var(--radius-sm); box-shadow: var(--shadow-sm); border: 1px solid var(--border-light); min-width: 120px; }
.stat-item .stat-num { font-size: 28px; font-weight: 700; color: var(--amber-dark); }
.stat-item .stat-lbl { font-size: 12px; color: var(--text-light); margin-top: 4px; }

/* 页脚 */
.footer { text-align: center; padding: 32px 20px; margin-top: 40px; border-top: 1px solid var(--border); font-size: 12px; color: var(--text-light); }
.footer a { color: var(--amber-dark); }

/* index 专属 — 暖旧纸背景 */
body.index-page {
  background: linear-gradient(180deg, #fefcf8 0%, #fdf6ec 8%, #faf0e0 30%, #f5ead5 55%, #faf0e0 78%, #fefcf8 100%), repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(180,120,20,0.01) 2px, rgba(180,120,20,0.01) 4px);
}

/* 响应式 */
@media (max-width: 640px) {
  .container { padding: 0 12px 40px; }
  .topic-header { padding: 24px 0 20px; }
  .topic-header .icon { font-size: 36px; }
  .nav-grid { grid-template-columns: 1fr; gap: 14px; }
  .article-card { padding: 14px 16px; }
  .course-header { padding: 32px 16px 24px; }
}
@media (min-width: 641px) and (max-width: 1024px) {
  .nav-grid { grid-template-columns: repeat(2, 1fr); }
}
'''
    path = os.path.join(OUT_DIR, 'mks-style.css')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("  ✓ mks-style.css")

def generate_topic_html(topic):
    """生成单个专题 HTML 文件"""
    articles = topic['articles']
    filename = f"{topic['id']}-{topic['slug']}.html"
    filepath = os.path.join(OUT_DIR, filename)

    # Collect unique concepts
    concepts = list(dict.fromkeys([a['concept'] for a in articles if a['concept']]))

    # Build concept tags HTML
    concept_tags_html = '\n'.join(f'<span class="concept-tag">{html_mod.escape(c)}</span>' for c in concepts[:12])

    # Build article cards
    article_cards = []
    for a in articles:
        concept_html = f'<span class="art-concept">{html_mod.escape(a["concept"])}</span>' if a['concept'] else ''
        article_cards.append(f'''  <div class="article-card">
    <div class="art-header">
      <span class="art-num">第{a['sort_order']}讲</span>
      <span class="art-title">{html_mod.escape(a['title'])}</span>
      {concept_html}
    </div>
    <div class="art-summary">{html_mod.escape(a['summary'])}</div>
  </div>''')

    articles_html = '\n'.join(article_cards)

    # Key concepts section
    key_concepts = []
    concept_descriptions = {
        '极限': '技术或系统在物理规律约束下能达到的边界，理解极限是理性思考的起点。',
        '务实': '用工程师的视角看世界——只解决迫在眉睫的问题，不追求不必要的完美。',
        '数字': '从数量级的角度理解世界，避免在数量级上犯错。',
        '复杂': '复杂技术并非不可触及——分解到基本原理，每个环节都可以被理解。',
        '变量': '识别影响结果的关键变量，区分相关性与因果性。',
        '模型': '用数学模型简化现实，在不确定中寻找可预测的规律。',
        '证据': '科学结论建立在可验证的证据之上——追问信息来源是科学思维的基本动作。',
        '计算': '数学是科学的基础语言——从极限到微积分，计算能力决定了科学探索的深度。',
        '真理': '科学结论不等于真理——科学中最好的结论也只是"尚未被证明存在错误"。',
        '起源': '事物的出现有三种方式：强大需求驱动、灭绝后幸存、随机涌现。',
        '发展': '从历史维度理解疾病与人体——天花塑造了人类史，HIV有不发病的感染者。',
        '旁证': '考古学式的思维方式——从碎片化的证据中重建历史图景。',
        '边界': '科学有其边界——知道什么不能被科学解释，与知道科学能解释什么同样重要。',
        '泡沫': '伪科学经不起实验检验——识破它们需要的是方法论，而非更多知识。',
        '成瘾': '从神经科学角度理解成瘾——不是意志力问题，而是大脑回路被劫持。',
        '谬误': '常见的科学谬误往往源于把相关性当作因果性。',
        '流变': '科学认知是流动的——今天的"常识"可能明天就被修正。',
        '源头': '追溯大学和科学院的诞生——理解科学作为一种社会制度的演进。',
        '遗憾': '中国与近代科学失之交臂的历史教训——不是技术落后，而是思维方式的分叉。',
        '追赶': '从留美幼童到庚子赔款办学——科学在中国的艰难扎根之路。',
        '平凡': '伟大科学家也是凡人——把他们拉下神坛，反而更能理解科学发现的真实过程。',
        '宏观': '农业文明的地理决定论——族群的命运由技术裁决。',
        '反省': '科学界也有潜规则和自我审查——保持反省才能保持科学的自我纠错能力。',
        '味道': '味觉的演化逻辑——苦味是毒物预警，口味偏好改变了人类命运的走向。',
        '心理': '心理学从哲学思辨到实验科学的历程——双盲实验是最有力的思维武器之一。',
        '衰老': '从线粒体角度理解衰老——自由基、端粒、细胞死亡，多重假说交织的未解之谜。',
        '批判性思维': '在信息洪流中保持清醒——不轻信、不盲从、追问证据和方法论。',
        '考古': '考古学的终极目标不是挖宝——而是通过物质遗存重建人类行为的演化史。',
        '荣耀': '诺贝尔奖的颁发逻辑与历史趣闻——理解科学荣誉体系如何影响研究方向。',
        '严谨': '1米有多长？1千克是多少？——测量定义了我们对世界的认知框架。'
    }

    for c in concepts[:8]:
        desc = concept_descriptions.get(c, '')
        if desc:
            key_concepts.append(f'      <li><strong>{html_mod.escape(c)}</strong>：{html_mod.escape(desc)}</li>')

    key_concepts_html = '\n'.join(key_concepts) if key_concepts else '<li>本专题涵盖多个科学思维核心概念，详见各篇文章。</li>'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(topic['slug'])} — 卓克·科学思维课 MKS</title>
<link rel="stylesheet" href="mks-style.css">
</head>
<body>

<nav class="top-nav">
  <span class="brand"><span class="icon">🔬</span>卓克·科学思维课 MKS</span>
  <a class="home-btn" href="index.html">← 返回主书架</a>
</nav>

<div class="container">

<header class="topic-header">
  <span class="icon">{topic['icon']}</span>
  <h1>{html_mod.escape(topic['slug'])}</h1>
  <p class="subtitle">{html_mod.escape(topic['subtitle'])}</p>
  <p class="desc">{html_mod.escape(topic['desc'])}</p>
</header>

<div class="divider"><span>◇</span></div>

<div class="concept-tags">
{concept_tags_html}
</div>

<div class="stats-row">
  <div class="stat-item">
    <div class="stat-num">{len(articles)}</div>
    <div class="stat-lbl">篇文章</div>
  </div>
  <div class="stat-item">
    <div class="stat-num">{len(concepts)}</div>
    <div class="stat-lbl">个核心概念</div>
  </div>
</div>

<div class="concept-box">
  <h3>🔑 关键概念</h3>
  <ul>
{key_concepts_html}
  </ul>
</div>

<section class="article-section">
  <h2>📖 全部文章 <span class="badge">{len(articles)}篇</span></h2>
{articles_html}
</section>

<footer class="footer">
  <p>卓克·科学思维课 MKS · 最小知识集 · <a href="index.html">返回知识主书架</a></p>
</footer>

</div>
</body>
</html>'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ {filename} ({len(articles)} 篇)")

def generate_index_html():
    """生成导航页 index.html"""
    total = sum(len(t['articles']) for t in TOPICS)

    cards = []
    for t in TOPICS:
        count = len(t['articles'])
        cards.append(f'''  <a class="nav-card" href="{t['id']}-{t['slug']}.html">
    <div class="card-icon">{t['icon']}</div>
    <h2>{html_mod.escape(t['slug'])}</h2>
    <p class="card-subtitle">{html_mod.escape(t['subtitle'])}</p>
    <p class="card-desc">{html_mod.escape(t['desc'])}</p>
    <p class="card-count"><span>{count}篇</span> 文章</p>
  </a>''')

    cards_html = '\n'.join(cards)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>卓克·科学思维课 — 知识主书架</title>
<link rel="stylesheet" href="mks-style.css">
</head>
<body class="index-page">

<nav class="top-nav">
  <span class="brand"><span class="icon">🔬</span>卓克·科学思维课</span>
  <span style="font-size:12px;opacity:.7;">知识主书架 · {total}讲</span>
</nav>

<div class="container">

<header class="course-header">
  <h1>卓克·科学思维课</h1>
  <p class="course-sub">你身边的万物简史 <span class="title-accent">MKS</span></p>
  <p class="course-meta">共{total}讲 · 7大专题 · 最小知识集 · 白底琥珀色</p>
</header>

<div class="divider"><span>◇</span></div>

<div class="nav-grid">
{cards_html}
</div>

<footer class="footer">
  <p>卓克·科学思维课 MKS · 最小知识集</p>
  <p>内容来源：得到App · 数据提取自 dedao.db · 共{total}讲</p>
  <p style="margin-top:8px;">科学思维不是记住更多知识，而是掌握迭代认知的方法。</p>
</footer>

</div>
</body>
</html>'''

    path = os.path.join(OUT_DIR, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✓ index.html ({total} 篇总计)")

if __name__ == '__main__':
    generate_html_files()
