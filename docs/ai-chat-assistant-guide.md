# MKS 页面 AI 小助手实现指南

> 提取自 吴军思想体系 concept_cards.html，供曼妮参考复用。

---

## 架构概述

纯前端实现，零依赖。一个 `fetch()` 搞定一切。核心三要素：

- **HTML 骨架** — 浮动按钮 + 弹出面板
- **CSS 样式** — 暗色主题，毛玻璃面板
- **JavaScript 逻辑** — API 调用、离线降级、Markdown 渲染

---

## 1. HTML 骨架

放在 `</body>` 前任意位置：

```html
<div class="ai-chat-widget" id="aiChatWidget">
  <button class="ai-chat-toggle" id="aiChatToggle" title="AI 助手">
    <span style="line-height:1;">💬</span>
    <span class="ai-chat-indicator" id="aiChatIndicator"></span>
  </button>
  <div class="ai-chat-panel" id="aiChatPanel">
    <div class="ai-chat-header">
      <span class="ai-chat-status">
        <span class="ai-chat-dot" id="aiChatDot"></span>
        <span id="aiChatStatusText">AI 在线</span>
      </span>
      <button class="ai-chat-close" id="aiChatClose">✕</button>
    </div>
    <div class="ai-chat-messages" id="aiChatMessages"></div>
    <div class="ai-chat-input-area">
      <input type="text" class="ai-chat-input" id="aiChatInput" placeholder="问一个问题…" autocomplete="off">
      <button class="ai-chat-send" id="aiChatSend">发送</button>
    </div>
  </div>
</div>
```

---

## 2. CSS 样式

```css
/* ===== AI Chat Widget ===== */
.ai-chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 200;
  font-family: "PingFang SC", "Noto Sans SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}

/* 浮动按钮 */
.ai-chat-toggle {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.18);
  background: linear-gradient(140deg, #1a3450 0%, #264a66 100%);
  color: #fff;
  font-size: 1.35rem;
  cursor: pointer;
  box-shadow: 0 4px 22px rgba(0,0,0,0.32);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
}
.ai-chat-toggle:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 30px rgba(0,0,0,0.42);
}
.ai-chat-toggle:active { transform: scale(0.94); }

/* 在线/离线指示点 */
.ai-chat-indicator {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #4caf50;
  border: 2px solid #1a3450;
  transition: background 0.3s;
}
.ai-chat-indicator.offline { background: #f44336; }

/* 对话面板 */
.ai-chat-panel {
  position: absolute;
  bottom: 66px;
  right: 0;
  width: 350px;
  max-height: 490px;
  background: rgba(16, 24, 38, 0.97);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  box-shadow: 0 18px 52px rgba(0,0,0,0.45);
  display: none;
  flex-direction: column;
  overflow: hidden;
}
.ai-chat-panel.open { display: flex; }

/* 面板头部 */
.ai-chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  background: rgba(255,255,255,0.025);
  flex-shrink: 0;
}
.ai-chat-status {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 0.72rem;
  color: #a0bcd0;
}
.ai-chat-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #4caf50;
  flex-shrink: 0;
  transition: background 0.3s;
}
.ai-chat-dot.offline { background: #f44336; }
.ai-chat-close {
  background: none;
  border: none;
  color: #7a8ea0;
  font-size: 1.05rem;
  cursor: pointer;
  padding: 2px 7px;
  border-radius: 5px;
  line-height: 1;
  transition: color 0.15s, background 0.15s;
}
.ai-chat-close:hover { color: #fff; background: rgba(255,255,255,0.08); }

/* 消息区域 */
.ai-chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 310px;
  min-height: 120px;
}
.ai-chat-messages::-webkit-scrollbar { width: 4px; }
.ai-chat-messages::-webkit-scrollbar-track { background: transparent; }
.ai-chat-messages::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.07);
  border-radius: 4px;
}

/* 消息气泡 */
.ai-chat-msg {
  max-width: 86%;
  padding: 8px 13px;
  border-radius: 13px;
  font-size: 0.78rem;
  line-height: 1.55;
  word-break: break-word;
  animation: ai-msg-in 0.26s ease-out;
}
@keyframes ai-msg-in {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.ai-chat-msg.user {
  align-self: flex-end;
  background: #2563eb;
  color: #fff;
  border-bottom-right-radius: 4px;
}
.ai-chat-msg.assistant {
  align-self: flex-start;
  background: rgba(255,255,255,0.075);
  color: #ced8e4;
  border-bottom-left-radius: 4px;
}
.ai-chat-msg.assistant strong { color: #e8f0f8; font-weight: 700; }
.ai-chat-msg.assistant code {
  background: rgba(255,255,255,0.10);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.72rem;
  font-family: 'SF Mono', 'Fira Code', monospace;
}
.ai-chat-msg.assistant ul,
.ai-chat-msg.assistant ol { margin: 3px 0; padding-left: 18px; }
.ai-chat-msg.assistant li { margin: 1px 0; }

/* 输入中动画 */
.ai-chat-typing {
  align-self: flex-start;
  background: rgba(255,255,255,0.05);
  color: #6a8090;
  padding: 10px 16px;
  border-radius: 13px;
  border-bottom-left-radius: 4px;
  font-size: 0.72rem;
  display: flex;
  gap: 5px;
  align-items: center;
}
.ai-chat-typing span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #6a8090;
  animation: ai-dot-bounce 1.3s ease-in-out infinite;
}
.ai-chat-typing span:nth-child(2) { animation-delay: 0.18s; }
.ai-chat-typing span:nth-child(3) { animation-delay: 0.36s; }
@keyframes ai-dot-bounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.35; }
  30% { transform: translateY(-5px); opacity: 1; }
}

/* 输入区域 */
.ai-chat-input-area {
  display: flex;
  gap: 7px;
  padding: 10px 12px;
  border-top: 1px solid rgba(255,255,255,0.07);
  background: rgba(255,255,255,0.02);
  flex-shrink: 0;
}
.ai-chat-input {
  flex: 1;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 10px;
  padding: 8px 12px;
  color: #d0dce8;
  font-size: 0.76rem;
  outline: none;
  transition: border-color 0.2s;
}
.ai-chat-input::placeholder { color: #5a6a7a; }
.ai-chat-input:focus { border-color: rgba(100,160,220,0.45); }
.ai-chat-send {
  background: linear-gradient(140deg, #2563eb, #3b82f6);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 8px 17px;
  font-size: 0.76rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.15s, transform 0.1s;
}
.ai-chat-send:hover { opacity: 0.88; }
.ai-chat-send:active { transform: scale(0.95); }
.ai-chat-send:disabled { opacity: 0.45; cursor: not-allowed; }

/* 移动端适配 */
@media (max-width: 480px) {
  .ai-chat-panel {
    width: calc(100vw - 32px);
    right: -2px;
    max-height: 420px;
  }
  .ai-chat-messages { max-height: 240px; }
  .ai-chat-toggle {
    width: 46px;
    height: 46px;
    font-size: 1.2rem;
  }
}
```

---

## 3. JavaScript 完整实现

```javascript
(function() {
  // ════════════ 配置（改这三行即可） ════════════
  var API_URL = 'https://api.siliconflow.cn/v1/chat/completions';
  var API_KEY = '***';   // 从 localStorage 读取，或让用户输入
  var MODEL   = 'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B';
  var HEALTH_URL = 'https://api.siliconflow.cn/v1/models';
  var REQUEST_TIMEOUT = 30000;
  var HEALTH_TIMEOUT = 5000;

  var chatPanel = document.getElementById('aiChatPanel');
  var chatMessages = document.getElementById('aiChatMessages');
  var chatInput = document.getElementById('aiChatInput');
  var chatSend = document.getElementById('aiChatSend');
  var chatClose = document.getElementById('aiChatClose');
  var chatToggle = document.getElementById('aiChatToggle');
  var chatDot = document.getElementById('aiChatDot');
  var chatIndicator = document.getElementById('aiChatIndicator');
  var chatStatusText = document.getElementById('aiChatStatusText');
  var isOnline = true;

  // ── 开关面板 ──
  chatToggle.addEventListener('click', function() {
    if (chatPanel.classList.contains('open')) {
      chatPanel.classList.remove('open');
    } else {
      chatPanel.classList.add('open');
      setTimeout(function() { chatInput.focus(); }, 150);
    }
  });
  chatClose.addEventListener('click', function() {
    chatPanel.classList.remove('open');
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && chatPanel.classList.contains('open') && document.activeElement !== chatInput) {
      chatPanel.classList.remove('open');
    }
  });

  // ── Enter 发送 ──
  chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
  chatSend.addEventListener('click', sendMessage);

  // ── 构建 System Prompt（动态注入页面上下文）──
  function buildSystemPrompt() {
    return '你是本知识库的 AI 助手。请用简洁有洞察力的语言回答（200字内），引用知识库中的具体概念。' +
      '若问题与知识库完全无关，礼貌引导回知识库话题。';
    // 👆 实际项目里这里注入页面状态：当前筛选、图案名称、知识库概况等
  }

  // ── 简易 Markdown → HTML ──
  function renderMarkdown(text) {
    if (!text) return '';
    var html = text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\n\s*[-•]\s+(.+)/g, '\n<li>$1</li>')
      .replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>')
      .replace(/\n/g, '<br>');
    return html;
  }

  // ── 添加消息气泡 ──
  function addMessage(role, content) {
    var div = document.createElement('div');
    div.className = 'ai-chat-msg ' + role;
    if (role === 'assistant') {
      div.innerHTML = renderMarkdown(content);
    } else {
      div.textContent = content;
    }
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
  }

  // ── 输入中动画 ──
  function showTyping() {
    var el = document.createElement('div');
    el.className = 'ai-chat-typing';
    el.id = 'aiTyping';
    el.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(el);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  function hideTyping() {
    var el = document.getElementById('aiTyping');
    if (el) el.remove();
  }

  // ── 在线状态切换 ──
  function setOnline(online) {
    isOnline = online;
    var method = online ? 'remove' : 'add';
    chatDot.classList[method]('offline');
    chatIndicator.classList[method]('offline');
    chatStatusText.textContent = online ? 'AI 在线' : '离线模式';
  }

  // ── 离线兜底回复（本地规则引擎）──
  function getMockReply(msg) {
    var lower = msg.toLowerCase();
    if (lower.indexOf('你好') !== -1 || lower.indexOf('hello') !== -1) {
      return '你好！我是知识库 AI 助手，当前处于离线模式。可以问我关于知识库内容的任何问题。';
    }
    if (lower.indexOf('统计') !== -1 || lower.indexOf('多少') !== -1) {
      return '我正在离线模式，无法获取实时统计。请等待网络恢复后重试。';
    }
    return '我正在离线模式，无法连接 AI API。请尝试刷新页面检查网络连接。';
  }

  // ── 发送消息（核心逻辑）──
  function sendMessage() {
    var text = chatInput.value.trim();
    if (!text) return;

    chatInput.value = '';
    chatSend.disabled = true;
    addMessage('user', text);
    showTyping();

    // 离线降级
    if (!isOnline) {
      setTimeout(function() {
        hideTyping();
        addMessage('assistant', getMockReply(text));
        chatSend.disabled = false;
        chatInput.focus();
      }, 700 + Math.random() * 500);
      return;
    }

    // API 调用
    var controller = new AbortController();
    var tid = setTimeout(function() { controller.abort(); }, REQUEST_TIMEOUT);

    fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + API_KEY
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [
          { role: 'system', content: buildSystemPrompt() },
          { role: 'user', content: text }
        ],
        max_tokens: 600,
        temperature: 0.6
      }),
      signal: controller.signal
    })
    .then(function(res) {
      clearTimeout(tid);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(function(data) {
      hideTyping();
      var reply = '';
      if (data.choices && data.choices[0] && data.choices[0].message) {
        reply = data.choices[0].message.content || '';
      }
      if (!reply) reply = '（AI 未返回内容，请重试）';
      addMessage('assistant', reply);
      chatSend.disabled = false;
      chatInput.focus();
    })
    .catch(function(err) {
      clearTimeout(tid);
      hideTyping();
      console.warn('API 不可达，切换离线模式:', err.message);
      setOnline(false);
      addMessage('assistant', getMockReply(text));
      chatSend.disabled = false;
      chatInput.focus();
    });
  }

  // ── 健康检查 ──
  function healthCheck() {
    var ctrl = new AbortController();
    var tid = setTimeout(function() { ctrl.abort(); }, HEALTH_TIMEOUT);
    fetch(HEALTH_URL, {
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + API_KEY },
      signal: ctrl.signal
    })
    .then(function(res) {
      clearTimeout(tid);
      setOnline(res.ok);
    })
    .catch(function(err) {
      clearTimeout(tid);
      setOnline(false);
    });
  }

  // ── 欢迎消息 ──
  function showWelcome() {
    addMessage('assistant', '你好！我是知识库 AI 助手。可以问我任何关于知识库内容的问题。');
  }

  // ── 初始化 ──
  healthCheck();
  setTimeout(function() {
    if (chatMessages.children.length === 0) showWelcome();
  }, 350);
})();
```

---

## 4. 设计要点

### 离线降级策略
```
页面加载 → 健康检查(GET /models)
  ├─ 成功 → isOnline=true，绿色指示灯
  └─ 失败 → isOnline=false，红色指示灯，启用本地规则引擎
```

每次发送消息前检查 `isOnline`，API 调用失败后自动切离线。

### 关键设计决策

| 决策 | 做法 | 原因 |
|------|------|------|
| System Prompt | 动态注入页面上下文 | AI 回答能贴合用户当前浏览状态 |
| 超时控制 | AbortController + setTimeout 30s | 避免请求挂起 |
| 简易 Markdown | 正则替换，无第三方库 | 零依赖，体积小 |
| 离线兜底 | 本地规则匹配关键词 | 断网也能给出有意义的回复 |
| API Key | `***` 占位，运行时从 localStorage 读 | 不硬编码进仓库 |

### 适配其他 API 提供商

只需改三行配置：
```javascript
// DeepSeek 官方 → 
var API_URL = 'https://api.deepseek.com/v1/chat/completions';
var MODEL   = 'deepseek-chat';

// OpenAI →
var API_URL = 'https://api.openai.com/v1/chat/completions';
var MODEL   = 'gpt-4o';

// 任何 OpenAI 兼容接口都一样用
```

---

## 5. 曼妮接入建议

1. **复制 HTML + CSS** → 页面布局不变
2. **复制 JS** → 改顶部三行配置
3. **重写 `buildSystemPrompt()`** → 注入自己知识库的上下文（概念数量、分类、来源等）
4. **重写 `getMockReply()`** → 匹配自己知识库的关键词做离线兜底
5. **Key 管理** → 建议从 `localStorage` 读取，首次使用时弹窗让用户输入
