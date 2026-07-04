<template>
  <div class="quiz-page">
    <div v-if="screen === 'pick'" class="screen">
      <div class="screen-header">
        <h1 class="screen-title">{{ $t('quiz.title') }}</h1>
        <p class="screen-sub">{{ $t('quiz.subtitle') }}</p>
      </div>

      <div v-if="loadingSubjects" class="loading-state">{{ $t('quiz.loadingSubjects') }}</div>
      <div v-else class="subject-grid">
        <button
          v-for="s in subjects"
          :key="s.name"
          class="subject-card"
          :class="{ selected: selectedSubject === s.name }"
          @click="selectedSubject = s.name"
        >
          <span class="s-icon" v-html="s.icon"></span>
          <span class="s-name">{{ $t('tests.subjects.' + s.slug) }}</span>
          <span v-if="selectedSubject === s.name" class="s-check">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          </span>
        </button>
      </div>

      <div class="pick-footer">
        <button class="btn-start" :disabled="!selectedSubject" @click="startQuiz">
          {{ $t('quiz.startQuiz') }} →
        </button>
      </div>
    </div>

    <div v-else-if="screen === 'quiz'" class="screen">
      <div v-if="loadingQuiz" class="loading-state">{{ $t('quiz.loadingQuestions') }}</div>

      <template v-else>
        <div class="quiz-progress">
          <div class="progress-meta">
            <span class="progress-subject">{{ $t('tests.subjects.' + selectedSubjectSlug) }}</span>
            <span class="progress-count">{{ currentIndex + 1 }} / {{ questions.length }}</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: progressPct + '%' }"></div>
          </div>
        </div>
        <div class="q-card" v-if="currentQ">
          <div class="q-type-badge" :class="currentQ.type">
            {{ currentQ.type === 'mcq' ? $t('quiz.multipleChoice') : $t('quiz.trueFalse') }}
          </div>
          <p class="q-text">{{ currentQ.question }}</p>

          <!-- MCQ options -->
          <div v-if="currentQ.type === 'mcq'" class="options">
            <button
              v-for="(text, key) in currentQ.options"
              :key="key"
              class="opt-btn"
              :class="optClass(key)"
              :disabled="answered"
              @click="submitAnswer(key)"
            >
              <span class="opt-key">{{ key }}</span>
              <span class="opt-text">{{ text }}</span>
              <span v-if="answered && key === currentQ.answer" class="opt-tick">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              </span>
              <span v-if="answered && key === userAnswer && key !== currentQ.answer" class="opt-cross">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </span>
            </button>
          </div>

          <div v-else class="options tf-options">
            <button
              v-for="val in tfOptions"
              :key="val"
              class="opt-btn tf-btn"
              :class="tfClass(val)"
              :disabled="answered"
              @click="submitAnswer(val)"
            >
              <span class="tf-icon">
                <svg v-if="val === tfOptions[0]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </span>
              {{ val }}
            </button>
          </div>

          <transition name="fade">
            <div v-if="answered" class="feedback" :class="isCorrect ? 'correct' : 'incorrect'">
              <span class="feedback-icon">
                <svg v-if="isCorrect" class="vector-celebrate" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34"/><path d="M12 2a6 6 0 0 1 6 6v5a6 6 0 0 1-6 6 6 6 0 0 1-6-6V8a6 6 0 0 1 6-6z"/></svg>
                <svg v-else class="vector-idea" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A5 5 0 0 0 8 8c0 1 .3 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>
              </span>
              <span>{{ isCorrect ? $t('quiz.correct') : $t('quiz.incorrect') + currentQ.answer }}</span>
            </div>
          </transition>
        </div>

        <div class="quiz-nav">
          <button v-if="answered" class="btn-next" @click="nextQuestion">
            {{ currentIndex < questions.length - 1 ? $t('quiz.nextQuestion') : $t('quiz.seeResults') }} →
          </button>
        </div>
      </template>
    </div>

    <div v-else-if="screen === 'results'" class="screen results-screen">
      <div class="results-top">
        <div class="results-left">
          <div class="score-badge" :class="scoreBadgeClass">
            <span class="score-num">{{ score }}</span>
            <span class="score-den">/ {{ questions.length }}</span>
          </div>
          <p class="score-label">{{ scoreMessage }}</p>
          <p class="score-subject">{{ $t('tests.subjects.' + selectedSubjectSlug) }}</p>

          <div class="pie-wrap">
            <svg viewBox="0 0 120 120" class="pie-svg">
              <circle cx="60" cy="60" r="50" fill="none" stroke="#eef0f7" stroke-width="18" />
              <circle
                cx="60"
                cy="60"
                r="50"
                fill="none"
                stroke="#22c55e"
                stroke-width="18"
                stroke-dasharray="314.16"
                :stroke-dashoffset="correctOffset"
                stroke-linecap="round"
                transform="rotate(-90 60 60)"
                style="transition: stroke-dashoffset 1s ease"
              />
              <circle
                cx="60"
                cy="60"
                r="50"
                fill="none"
                stroke="#ef4444"
                stroke-width="18"
                stroke-dasharray="314.16"
                :stroke-dashoffset="wrongOffset"
                stroke-linecap="round"
                :transform="`rotate(${correctDeg - 90} 60 60)`"
                style="transition: stroke-dashoffset 1s ease"
              />
              <text x="60" y="56" text-anchor="middle" font-size="18" font-weight="800" fill="#0f2044">{{ scorePct }}%</text>
              <text x="60" y="72" text-anchor="middle" font-size="9" fill="#7a82a0">{{ $t('quiz.score') }}</text>
            </svg>
            <div class="pie-legend">
              <div class="legend-item">
                <span class="legend-dot correct-dot"></span> {{ $t('quiz.correctLabel') }} ({{ score }})
              </div>
              <div class="legend-item">
                <span class="legend-dot wrong-dot"></span> {{ $t('quiz.incorrectLabel') }} ({{ questions.length - score }})
              </div>
            </div>
          </div>
        </div>

        <div class="review-panel">
          <h3 class="review-title">{{ $t('quiz.answerReview') }}</h3>
          <div
            v-for="(q, i) in questions"
            :key="i"
            class="review-item"
            :class="userAnswers[i] === q.answer ? 'r-correct' : 'r-wrong'"
          >
            <div class="review-q-header">
              <span class="review-num">{{ $t('quiz.questionAbbrev') }}{{ i + 1 }}</span>
              <span class="review-verdict">
                <svg v-if="userAnswers[i] === q.answer" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:3px;"><polyline points="20 6 9 17 4 12"/></svg>
                <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:3px;"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                {{ userAnswers[i] === q.answer ? $t('quiz.correct') : $t('quiz.incorrectShort') }}
              </span>
            </div>
            <p class="review-q-text">{{ q.question }}</p>
            <div class="review-answers">
              <span class="review-yours">
                {{ $t('quiz.yourAnswer') }} <strong>{{ userAnswers[i] }}</strong>
                <template v-if="q.type === 'mcq' && q.options[userAnswers[i]]">
                  — {{ q.options[userAnswers[i]] }}
                </template>
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="results-actions">
        <button class="btn-retry" @click="retrySubject">↺ {{ $t('quiz.retry') }} {{ $t('tests.subjects.' + selectedSubjectSlug) }}</button>
        <button class="btn-home" @click="goHome">← {{ $t('quiz.chooseAnother') }}</button>
      </div>
    </div>
  </div>
</template>

<script>
const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

const SUBJECT_ICONS = {
  Mathematics: { slug: 'mathematics', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>` },
  Physics: { slug: 'physics', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 21h2"/><path d="M12 17v4"/><path d="M14 4A22 22 0 0 0 3 15"/><path d="M17 14A22 22 0 0 0 6 3"/><circle cx="12" cy="12" r="3"/><path d="m14.2 14.2 4.3 4.3"/></svg>` },
  Chemistry: { slug: 'chemistry', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 3h15"/><path d="M6 3v13a4 4 0 0 0 4 4h4a4 4 0 0 0 4-4V3"/><path d="M6 14h12"/></svg>` },
  Biology: { slug: 'biology', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 10.5C7.8 13.8 13.2 13.8 16.5 10.5c.3-.3.3-.8 0-1.1-.3-.3-.8-.3-1.1 0-2.7 2.7-7.1 2.7-9.8 0-.3-.3-.8-.3-1.1 0-.3.3-.3.8 0 1.1z"/><path d="M19.5 13.5c-3.3-3.3-8.7-3.3-12 0-.3.3-.3.8 0 1.1.3.3.8.3 1.1 0 2.7-2.7 7.1-2.7 9.8 0 .3.3.8.3 1.1 0 .3-.3-.3-.8 0-1.1z"/><path d="m3.5 3.5 17 17"/></svg>` },
  History: { slug: 'history', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/><path d="M14 3v5h5"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>` },
  English: { slug: 'english', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>` },
  EarthScience: { slug: 'earthScience', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>` },
  Geography: { slug: 'geography', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/></svg>` },
  MoralCivics: { slug: 'moralCivics', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="22"/><line x1="5" y1="7" x2="19" y2="7"/><path d="M19 7c0 5-3.5 8-7 8s-7-3-7-8"/></svg>` },
}

export default {
  name: 'QuizView',

  data() {
    return {
      screen: 'pick',
      subjects: [],
      loadingSubjects: true,
      selectedSubject: null,

      questions: [],
      loadingQuiz: false,
      currentIndex: 0,
      userAnswer: null,
      userAnswers: [],
      answered: false,
      score: 0,
    }
  },

  computed: {
    selectedSubjectSlug() {
      return SUBJECT_ICONS[this.selectedSubject]?.slug || ''
    },
    tfOptions() {
      return ['ពិត', 'មិនពិត']
    },
    currentQ() {
      return this.questions[this.currentIndex] || null
    },
    progressPct() {
      return (this.currentIndex / this.questions.length) * 100
    },
    isCorrect() {
      return this.userAnswer === this.currentQ?.answer
    },
    scorePct() {
      return this.questions.length ? Math.round((this.score / this.questions.length) * 100) : 0
    },
    scoreMessage() {
      const p = this.scorePct
      if (p === 100) return '🟢 ' + this.$t('quiz.perfectScore')
      if (p >= 80) return '🟡 ' + this.$t('quiz.greatWork')
      if (p >= 60) return '🔵 ' + this.$t('quiz.goodEffort')
      if (p >= 40) return '⚪ ' + this.$t('quiz.niceTry')
      return '🎯 ' + this.$t('quiz.dontGiveUp')
    },
    scoreBadgeClass() {
      const p = this.scorePct
      if (p >= 80) return 'badge-green'
      if (p >= 60) return 'badge-amber'
      return 'badge-red'
    },
    circumference() {
      return 2 * Math.PI * 50
    },
    correctDeg() {
      return (this.score / this.questions.length) * 360
    },
    correctOffset() {
      const filled = (this.score / this.questions.length) * this.circumference
      return this.circumference - filled
    },
    wrongOffset() {
      const wrong = this.questions.length - this.score
      const filled = (wrong / this.questions.length) * this.circumference
      return this.circumference - filled
    },
  },

  methods: {
    async fetchSubjects() {
      try {
        const res = await fetch(`${API}/api/subjects`, { cache: 'no-store' })
        const data = await res.json()
        this.subjects = data.subjects.map((name) => ({
          name,
          slug: SUBJECT_ICONS[name]?.slug || name.toLowerCase(),
          icon: SUBJECT_ICONS[name]?.icon || '📘',
        }))
      } catch {
        this.subjects = Object.keys(SUBJECT_ICONS).map((name) => ({
          name,
          slug: SUBJECT_ICONS[name].slug,
          icon: SUBJECT_ICONS[name].icon,
        }))
      } finally {
        this.loadingSubjects = false
      }
    },

    async startQuiz() {
      this.screen = 'quiz'
      this.loadingQuiz = true
      this.questions = []
      this.currentIndex = 0
      this.userAnswers = []
      this.score = 0
      this.answered = false
      this.userAnswer = null

      try {
        const res = await fetch(
          `${API}/api/quiz?subject=${encodeURIComponent(this.selectedSubject)}&count=10`,
        )
        const data = await res.json()
        this.questions = data.questions
      } catch {
        alert(this.$t('quiz.loadError'))
        this.screen = 'pick'
      } finally {
        this.loadingQuiz = false
      }
    },

    submitAnswer(key) {
      if (this.answered) return
      this.userAnswer = key
      this.answered = true
      this.userAnswers.push(key)
      if (key === this.currentQ.answer) this.score++
    },

    nextQuestion() {
      if (this.currentIndex < this.questions.length - 1) {
        this.currentIndex++
        this.answered = false
        this.userAnswer = null
      } else {
        this.screen = 'results'
      }
    },

    optClass(key) {
      if (!this.answered) return ''
      if (key === this.currentQ.answer) return 'opt-correct'
      if (key === this.userAnswer && key !== this.currentQ.answer) return 'opt-wrong'
      return 'opt-dim'
    },

    tfClass(val) {
      if (!this.answered) return ''
      if (val === this.currentQ.answer) return 'opt-correct'
      if (val === this.userAnswer && val !== this.currentQ.answer) return 'opt-wrong'
      return 'opt-dim'
    },

    retrySubject() {
      this.startQuiz()
    },
    goHome() {
      this.screen = 'pick'
      this.selectedSubject = null
    },
  },

  mounted() {
    this.fetchSubjects()
  },
}
</script>

<style scoped>
.quiz-page {
  max-width: 900px;
  margin: 0 auto;
}

.screen {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.screen-title {
  font-size: 26px;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 6px;
}
.screen-sub {
  color: var(--gray-500);
  font-size: 13.5px;
}

.subject-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
@media (max-width: 768px) {
  .subject-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.subject-card {
  background: var(--white);
  border: 2px solid var(--gray-100);
  border-radius: var(--radius);
  padding: 22px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.15s;
  position: relative;
}
.subject-card:hover {
  border-color: var(--amber);
  transform: translateY(-2px);
}
.subject-card.selected {
  border-color: var(--navy);
  background: #f0f3fa;
}
.s-icon {
  font-size: 30px;
  color: var(--amber)
}
.s-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--navy);
}
.s-check {
  position: absolute;
  top: 8px;
  right: 10px;
  color: var(--navy);
  font-weight: 800;
  font-size: 14px;
}

.pick-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.pick-info {
  font-size: 12px;
  color: var(--gray-500);
}
.btn-start {
  background: var(--navy);
  color: var(--white);
  border: none;
  border-radius: 9px;
  padding: 12px 28px;
  font-size: 14px;
  font-weight: 700;
  transition: opacity 0.15s;
}
.btn-start:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.btn-start:not(:disabled):hover {
  opacity: 0.85;
}

.quiz-progress {
  background: var(--white);
  border-radius: var(--radius);
  padding: 16px 20px;
  border: 1px solid var(--gray-100);
}
.progress-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}
.progress-subject {
  font-size: 13px;
  font-weight: 700;
  color: var(--navy);
}
.progress-count {
  font-size: 13px;
  font-weight: 600;
  color: var(--gray-500);
}
.progress-track {
  height: 6px;
  background: var(--gray-100);
  border-radius: 3px;
}
.progress-fill {
  height: 6px;
  background: var(--amber);
  border-radius: 3px;
  transition: width 0.4s ease;
}

.q-card {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: 18px;
  padding: 28px 28px 22px;
}
.q-type-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 20px;
  margin-bottom: 14px;
  letter-spacing: 0.03em;
}
.q-type-badge.mcq {
  background: #e8f0fe;
  color: #1a56c4;
}
.q-type-badge.tf {
  background: var(--amber-light);
  color: #a06a00;
}

.q-text {
  font-size: 17px;
  font-weight: 600;
  color: var(--navy);
  line-height: 1.55;
  margin-bottom: 22px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.tf-options {
  flex-direction: row;
  gap: 14px;
}

.opt-btn {
  background: var(--gray-50);
  border: 1.5px solid var(--gray-100);
  border-radius: 10px;
  padding: 13px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: var(--text);
  text-align: left;
  transition: all 0.15s;
  cursor: pointer;
}
.opt-btn:hover:not(:disabled) {
  border-color: var(--navy);
  background: #f0f3fa;
}
.opt-btn:disabled {
  cursor: default;
}

.opt-key {
  width: 26px;
  height: 26px;
  background: var(--white);
  border: 1px solid var(--gray-300);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--navy);
  flex-shrink: 0;
}
.opt-text {
  flex: 1;
}
.opt-tick {
  margin-left: auto;
  color: #16a34a;
  font-weight: 800;
}
.opt-cross {
  margin-left: auto;
  color: #dc2626;
  font-weight: 800;
}

.opt-correct {
  background: #f0fdf4 !important;
  border-color: #22c55e !important;
}
.opt-correct .opt-key {
  background: #22c55e;
  color: white;
  border-color: #22c55e;
}

.opt-wrong {
  background: #fef2f2 !important;
  border-color: #ef4444 !important;
}
.opt-wrong .opt-key {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

.opt-dim {
  opacity: 0.45;
}

.tf-btn {
  flex: 1;
  justify-content: center;
  font-size: 15px;
  font-weight: 700;
  gap: 8px;
  padding: 16px;
}
.tf-icon {
  font-size: 18px;
}

.feedback {
  margin-top: 16px;
  padding: 12px 16px;
  border-radius: 9px;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
}
.feedback.correct {
  background: #f0fdf4;
  color: #15803d;
}
.feedback.incorrect {
  background: #fef2f2;
  color: #b91c1c;
}
.feedback-icon {
  font-size: 18px;
}

.quiz-nav {
  display: flex;
  justify-content: flex-end;
}
.btn-next {
  background: var(--navy);
  color: var(--white);
  border: none;
  border-radius: 9px;
  padding: 12px 26px;
  font-size: 14px;
  font-weight: 700;
  transition: opacity 0.15s;
}
.btn-next:hover {
  opacity: 0.85;
}

.results-screen {
  gap: 28px;
}
.results-top {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 20px;
  align-items: start;
}

.results-left {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: 18px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.score-badge {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 2px;
}
.badge-green {
  background: #dcfce7;
}
.badge-amber {
  background: var(--amber-light);
}
.badge-red {
  background: #fee2e2;
}

.score-num {
  font-size: 32px;
  font-weight: 800;
  color: var(--navy);
  margin-top: 12px;
}
.score-den {
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-500);
}
.score-label {
  font-size: 15px;
  font-weight: 700;
  color: var(--navy);
  text-align: center;
}
.score-subject {
  font-size: 12px;
  color: var(--gray-500);
}

.pie-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}
.pie-svg {
  width: 120px;
  height: 120px;
}
.pie-legend {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.legend-item {
  font-size: 12px;
  color: var(--gray-700);
  display: flex;
  align-items: center;
  gap: 7px;
}
.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.correct-dot {
  background: #22c55e;
}
.wrong-dot {
  background: #ef4444;
}

.review-panel {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: 18px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 500px;
  overflow-y: auto;
}
.review-title {
  font-size: 15px;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 4px;
}

.review-item {
  border-radius: 10px;
  padding: 12px 14px;
  border-left: 3px solid transparent;
}
.r-correct {
  background: #f0fdf4;
  border-color: #22c55e;
}
.r-wrong {
  background: #fef2f2;
  border-color: #ef4444;
}

.review-q-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}
.review-num {
  font-size: 11px;
  font-weight: 700;
  color: var(--gray-500);
}
.review-verdict {
  font-size: 11px;
  font-weight: 700;
}
.r-correct .review-verdict {
  color: #16a34a;
}
.r-wrong .review-verdict {
  color: #dc2626;
}

.review-q-text {
  font-size: 13px;
  font-weight: 600;
  color: var(--navy);
  margin-bottom: 7px;
  line-height: 1.4;
}
.review-answers {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.review-yours,
.review-correct {
  font-size: 12px;
  color: var(--gray-700);
}
.review-correct {
  color: #16a34a;
}

.results-actions {
  display: flex;
  gap: 12px;
}
.btn-retry {
  background: var(--navy);
  color: var(--white);
  border: none;
  border-radius: 9px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 700;
  transition: opacity 0.15s;
}
.btn-retry:hover {
  opacity: 0.85;
}
.btn-home {
  background: var(--white);
  color: var(--navy);
  border: 1.5px solid var(--gray-300);
  border-radius: 9px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.15s;
}
.btn-home:hover {
  background: var(--gray-100);
}

.loading-state {
  text-align: center;
  padding: 60px;
  color: var(--gray-500);
  font-size: 14px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
