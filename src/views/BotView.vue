<template>
  <div class="chat-page">
    <div class="chat-layout">
      <div class="chat-panel">
        <div class="chat-messages" ref="messagesEl">
          <div v-if="chatHistory.length === 0" class="chat-empty">
            <span class="empty-icon">💬</span>
            <h2>{{ $t('chat.emptyTitle') }}</h2>
            <p>{{ $t('chat.emptyBody') }}</p>
            <div class="quick-questions">
              <button v-for="q in quickQuestions" :key="q.key" class="quick-chip" @click="sendQuick(q.key)">
                {{ $t('chat.quickQuestions.' + q.key) }}
              </button>
            </div>
          </div>

          <div v-for="(entry, i) in chatHistory" :key="i" class="chat-entry">
            <div class="msg msg-user">
              <div class="msg-bubble msg-bubble-user">{{ entry.question }}</div>
              <span class="msg-avatar">👤</span>
            </div>
            <div class="msg msg-bot">
              <span class="msg-avatar">🤖</span>
              <div class="msg-bubble msg-bubble-bot" v-html="renderMarkdown(entry.answer)"></div>
            </div>
          </div>

          <div v-if="loading" class="msg msg-bot">
            <span class="msg-avatar">🤖</span>
            <div class="typing-dots"><span></span><span></span><span></span></div>
          </div>
        </div>

        <div class="chat-input-area">
          <div class="chat-input-wrap" :class="{ focused: inputFocused }">
            <textarea class="typing"
              v-model="question"
              :placeholder="$t('chat.inputPlaceholder')"
              rows="1"
              ref="inputEl"
              :disabled="loading"
              @keydown.enter.exact.prevent="sendQuestion"
              @keydown.enter.shift.exact="addNewline"
              @focus="inputFocused = true"
              @blur="inputFocused = false"
            ></textarea>
            <button class="send-btn" :disabled="!question.trim() || loading" @click="sendQuestion">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
          <p class="input-hint">{{ $t('chat.inputHint') }}</p>
        </div>
      </div>

      <aside class="right-panel">
        <div class="panel-card">
          <h3 class="panel-title">{{ $t('chat.recentQuestions') }}</h3>
          <p v-if="chatHistory.length === 0" class="panel-empty">{{ $t('chat.noQuestionsYet') }}</p>
          <ul v-else class="recent-list">
            <li
              v-for="(entry, i) in [...chatHistory].reverse().slice(0, 6)"
              :key="i"
              class="recent-item"
            >
              {{ entry.question }}
            </li>
          </ul>
        </div>

        <div class="panel-card">
          <h3 class="panel-title">{{ $t('chat.studyTips') }}</h3>
          <ul class="tips-list">
            <li v-for="tip in tips" :key="tip.key">✔ {{ $t('chat.tips.' + tip.key) }}</li>
          </ul>
        </div>

        <button class="reset-btn" @click="resetChat">🗑 {{ $t('chat.clearChat') }}</button>
      </aside>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import { v4 as uuidv4 } from 'uuid'

export default {
  name: 'BotView',
  data() {
    return {
      question: '',
      chatHistory: [],
      loading: false,
      inputFocused: false,
      sessionId: uuidv4(),
      quickQuestions: [
        { key: 'explainPhotosynthesis' },
        { key: 'newtonsSecondLaw' },
        { key: 'quizKhmerHistory' },
        { key: 'solveQuadratic' },
      ],
      tips: [
        { key: 'practiceDaily' },
        { key: 'reviewMistakes' },
        { key: 'focusWeakSubjects' },
        { key: 'takeBreaks' },
        { key: 'askFollowUp' },
      ],
    }
  },
  methods: {
    renderMarkdown(text) {
      if (!text) return ''
      return marked.parse(text)
    },

    async sendQuestion() {
      const q = this.question.trim()
      if (!q || this.loading) return

      this.question = ''
      this.loading = true
      this.scrollDown()

      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/ask`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question: q,
            session_id: this.sessionId,
          }),
        })

        if (!res.ok) throw new Error(`Server error ${res.status}`)

        const data = await res.json()
        this.chatHistory.push({ question: q, answer: data.answer })
      } catch (err) {
        this.chatHistory.push({
          question: q,
          answer: `⚠️ Could not reach the backend. Make sure your Python server is running on port 5000.\n\n*${err.message}*`,
        })
      } finally {
        this.loading = false
        this.scrollDown()
      }
    },

    sendQuick(key) {
      this.question = this.$t('chat.quickQuestions.' + key)
      this.sendQuestion()
    },

    async resetChat() {
      try {
        await fetch(`${import.meta.env.VITE_API_URL}/reset`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: this.sessionId }),
        })
      } catch (err) {
        console.warn('Reset request failed:', err)
      } finally {
        this.chatHistory = []
        this.sessionId = uuidv4()
      }
    },

    addNewline() {
      this.question += '\n'
    },

    scrollDown() {
      this.$nextTick(() => {
        const el = this.$refs.messagesEl
        if (el) el.scrollTop = el.scrollHeight
      })
    },
  },
}
</script>

<style scoped>
.chat-page {
  height: calc(100vh - 57px - 56px);
}

.chat-layout {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 18px;
  height: 100%;
}
@media (max-width: 1024px) {
  .chat-layout {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 768px) {
  .chat-layout {
    gap: 12px;
  }
}
.chat-panel {
  background: var(--white);
  border-radius: 18px;
  border: 1px solid var(--gray-100);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  scroll-behavior: smooth;
}

.chat-messages::-webkit-scrollbar {
  width: 3px;
}
.chat-messages::-webkit-scrollbar-thumb {
  background: var(--gray-300);
  border-radius: 3px;
}

.chat-empty {
  margin: auto;
  text-align: center;
  max-width: 340px;
}

.empty-icon {
  font-size: 44px;
  display: block;
  margin-bottom: 14px;
}

.chat-empty h2 {
  font-size: 18px;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 7px;
}

.chat-empty p {
  color: var(--gray-500);
  font-size: 13px;
  margin-bottom: 18px;
}

.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  justify-content: center;
}

.quick-chip {
  background: var(--gray-50);
  border: 1px solid var(--gray-100);
  color: var(--navy);
  padding: 7px 13px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.15s;
}

.quick-chip:hover {
  border-color: var(--amber);
  background: var(--amber-light);
}

.chat-entry {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.msg {
  display: flex;
  align-items: flex-end;
  gap: 9px;
}
.msg-user {
  justify-content: flex-end;
}
.msg-bot {
  justify-content: flex-start;
}

.msg-avatar {
  font-size: 18px;
  flex-shrink: 0;
}

.msg-bubble {
  padding: 11px 15px;
  border-radius: 14px;
  font-size: 13px;
  line-height: 1.7;
  max-width: 72%;
}

.msg-bubble-user {
  background: var(--navy);
  color: var(--white);
  border-bottom-right-radius: 3px;
}

.msg-bubble-bot {
  background: var(--gray-50);
  color: var(--text);
  border: 1px solid var(--gray-100);
  border-bottom-left-radius: 3px;
}

.msg-bubble-bot :deep(strong) {
  color: var(--navy);
}
.msg-bubble-bot :deep(code) {
  background: var(--gray-100);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 12px;
}
.msg-bubble-bot :deep(p) {
  margin-bottom: 8px;
}
.msg-bubble-bot :deep(p:last-child) {
  margin-bottom: 0;
}
.msg-bubble-bot :deep(ul),
.msg-bubble-bot :deep(ol) {
  padding-left: 18px;
  margin-bottom: 8px;
}

.typing-dots {
  display: flex;
  gap: 4px;
  padding: 13px 16px;
  background: var(--gray-50);
  border: 1px solid var(--gray-100);
  border-radius: 14px;
  border-bottom-left-radius: 3px;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--amber);
  animation: bounce 1.2s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  40% {
    transform: translateY(-6px);
    opacity: 1;
  }
}

.chat-input-area {
  padding: 14px 18px 16px;
  border-top: 1px solid var(--gray-100);
}

.chat-input-wrap {
  display: flex;
  align-items: flex-end;
  gap: 9px;
  background: var(--gray-50);
  border: 1.5px solid var(--gray-100);
  border-radius: 12px;
  padding: 9px 13px;
  transition: border-color 0.2s;
}

.chat-input-wrap.focused {
  border-color: var(--navy);
}

textarea {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-family: inherit;
  font-size: 13px;
  color: var(--text);
  resize: none;
  max-height: 100px;
  overflow-y: auto;
  line-height: 1.6;
  margin-bottom: 6px;
}

textarea::placeholder {
  color: var(--gray-300);
}

.send-btn {
  background: var(--navy);
  border: none;
  border-radius: 8px;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition:
    background 0.15s,
    opacity 0.15s;
}

.send-btn:hover:not(:disabled) {
  background: var(--navy-mid);
}
.send-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
.send-btn svg {
  width: 14px;
  height: 14px;
  stroke: white;
}

.input-hint {
  font-size: 10px;
  color: var(--gray-300);
  margin-top: 7px;
  text-align: center;
}

.right-panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.panel-card {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: var(--radius);
  padding: 18px;
}

.panel-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--navy);
  margin-bottom: 12px;
}

.panel-empty {
  font-size: 12px;
  color: var(--gray-300);
}

.recent-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recent-item {
  font-size: 12px;
  color: var(--gray-700);
  padding-bottom: 8px;
  border-bottom: 1px solid var(--gray-100);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.recent-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.tips-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 7px;
}
.tips-list li {
  font-size: 12px;
  color: var(--gray-700);
  line-height: 1.5;
}

.reset-btn {
  background: var(--white);
  border: 1.5px solid #ffd0d0;
  color: #c0392b;
  border-radius: 9px;
  padding: 9px;
  font-size: 12px;
  font-weight: 600;
  transition: background 0.15s;
}

.reset-btn:hover {
  background: #fff5f5;
}
</style>
