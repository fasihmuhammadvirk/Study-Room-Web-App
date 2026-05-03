/* =============================================
   StudyBot — Gemini-powered chat widget JS
   ============================================= */

(function () {
  'use strict';

  /* ---- DOM refs ---- */
  const toggle     = document.getElementById('studybot-toggle');
  const panel      = document.getElementById('studybot-panel');
  const iconOpen   = document.getElementById('studybot-icon-open');
  const iconClose  = document.getElementById('studybot-icon-close');
  const msgBox     = document.getElementById('studybot-messages');
  const input      = document.getElementById('studybot-input');
  const sendBtn    = document.getElementById('studybot-send');
  const clearBtn   = document.getElementById('studybot-clear');

  /* ---- Conversation history (for multi-turn context) ---- */
  let history = [];
  let isOpen  = false;
  let isTyping = false;

  /* ---- Toggle panel ---- */
  toggle.addEventListener('click', () => {
    isOpen = !isOpen;
    panel.classList.toggle('studybot-hidden', !isOpen);
    iconOpen.style.display  = isOpen ? 'none'  : 'inline';
    iconClose.style.display = isOpen ? 'inline': 'none';
    if (isOpen) {
      input.focus();
      scrollBottom();
    }
  });

  /* ---- Clear chat ---- */
  clearBtn.addEventListener('click', () => {
    history = [];
    msgBox.innerHTML = `
      <div class="studybot-msg studybot-msg--bot">
        <div class="studybot-bubble">
          👋 Hi! I'm <strong>StudyBot</strong>. Ask me anything — concepts, tips, problems, resources.
        </div>
      </div>`;
  });

  /* ---- Send on Enter (Shift+Enter = newline) ---- */
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  /* ---- Auto-resize textarea ---- */
  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 100) + 'px';
  });

  sendBtn.addEventListener('click', sendMessage);

  /* ---- Core send function ---- */
  function sendMessage() {
    const text = input.value.trim();
    if (!text || isTyping) return;

    appendMessage('user', text);
    history.push({ role: 'user', content: text });
    input.value = '';
    input.style.height = 'auto';

    showTyping();
    isTyping = true;
    sendBtn.disabled = true;

    // Get CSRF token from cookie
    const csrfToken = getCookie('csrftoken');

    fetch('/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ message: text, history: history.slice(0, -1) }),
    })
      .then((res) => res.json())
      .then((data) => {
        removeTyping();
        isTyping = false;
        sendBtn.disabled = false;

        if (data.error) {
          appendMessage('bot', `⚠️ ${data.error}`);
        } else {
          const reply = data.reply || '';
          history.push({ role: 'bot', content: reply });
          appendMessage('bot', reply);
        }
      })
      .catch((err) => {
        removeTyping();
        isTyping = false;
        sendBtn.disabled = false;
        appendMessage('bot', '⚠️ Network error. Please try again.');
        console.error('StudyBot error:', err);
      });
  }

  /* ---- Append a chat bubble ---- */
  function appendMessage(role, text) {
    const wrapper = document.createElement('div');
    wrapper.className = `studybot-msg studybot-msg--${role === 'user' ? 'user' : 'bot'}`;

    const bubble = document.createElement('div');
    bubble.className = 'studybot-bubble';
    bubble.innerHTML = formatText(text);

    wrapper.appendChild(bubble);
    msgBox.appendChild(wrapper);
    scrollBottom();
  }

  /* ---- Typing indicator ---- */
  function showTyping() {
    const el = document.createElement('div');
    el.className = 'studybot-msg studybot-msg--bot';
    el.id = 'studybot-typing';
    el.innerHTML = `
      <div class="studybot-bubble studybot-typing-indicator">
        <span></span><span></span><span></span>
      </div>`;
    msgBox.appendChild(el);
    scrollBottom();
  }

  function removeTyping() {
    const el = document.getElementById('studybot-typing');
    if (el) el.remove();
  }

  /* ---- Simple markdown-like formatter ---- */
  function formatText(raw) {
    // Escape HTML
    let text = raw
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Bold **text**
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Italic *text*
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    // Inline code `text`
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Bullet points (lines starting with - or *)
    text = text.replace(/^[\-\*] (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    // Line breaks
    text = text.replace(/\n/g, '<br>');

    return text;
  }

  /* ---- Scroll to bottom of messages ---- */
  function scrollBottom() {
    msgBox.scrollTop = msgBox.scrollHeight;
  }

  /* ---- Get cookie by name (for CSRF) ---- */
  function getCookie(name) {
    let value = null;
    document.cookie.split(';').forEach((c) => {
      const [k, v] = c.trim().split('=');
      if (k === name) value = decodeURIComponent(v);
    });
    return value;
  }
})();
