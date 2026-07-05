<template>
  <div class="calculator-page">
    <div class="calc-header">
      <div>
        <h2 class="calc-title">{{ $t('calculator.title') }}</h2>
        <p class="calc-subtitle">{{ $t('calculator.subtitle') }}</p>
      </div>
      <div class="class-toggle">
        <button
          class="toggle-btn"
          :class="{ 'toggle-btn--active': selectedClass === 'Science' }"
          @click="selectedClass = 'Science'"
        >
          {{ $t('calculator.science') }}
        </button>
        <button
          class="toggle-btn"
          :class="{ 'toggle-btn--active': selectedClass === 'Social' }"
          @click="selectedClass = 'Social'"
        >
          {{ $t('calculator.social') }}
        </button>
      </div>
    </div>

    <div class="calc-body">
      <div class="subject-group">
        <p class="group-label"><span class="dot"></span> {{ $t('calculator.mainSubject') }}</p>
        <div class="subject-grid">
          <div class="subject-card" v-for="subject in mainSubjects" :key="subject.key">
            <div class="subject-card-top">
              <span class="subject-icon" v-html="subject.icon"></span>
              <p class="subject-name">{{ $t('calculator.subjects.' + subject.key) }}</p>
            </div>
            <div class="subject-card-bottom">
              <input
                type="number"
                class="score-input"
                :placeholder="$t('calculator.score')"
                v-model.number="subject.score"
                min="0"
                :max="subject.maxScore"
                @input="subject.score = clamp(subject.score, subject.maxScore)"
              />
              <span class="max-score">/ {{ subject.maxScore }}</span>
              <span class="grade-badge">
                {{
                  subject.score !== '' && subject.score !== null
                    ? calculate(subject.score, subject.maxScore)
                    : '—'
                }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="subject-group">
        <p class="group-label"><span class="dot"></span> {{ $t('calculator.selectionSubject') }}</p>
        <div class="subject-grid">
          <div class="subject-card" v-for="subject in selectionSubjects" :key="subject.key">
            <div class="subject-card-top">
              <span class="subject-icon" v-html="subject.icon"></span>
              <p class="subject-name">{{ $t('calculator.subjects.' + subject.key) }}</p>
            </div>
            <div class="subject-card-bottom">
              <input
                type="number"
                class="score-input"
                :placeholder="$t('calculator.score')"
                v-model.number="subject.score"
                min="0"
                :max="subject.maxScore"
                @input="subject.score = clamp(subject.score, subject.maxScore)"
              />
              <span class="max-score">/ {{ subject.maxScore }}</span>
              <span class="grade-badge">
                {{
                  subject.score !== '' && subject.score !== null
                    ? calculate(subject.score, subject.maxScore)
                    : '—'
                }}
              </span>
            </div>
          </div>

          <button class="find-total-btn" @click="calculateTotal">{{ $t('calculator.findTotal') }}</button>
        </div>
      </div>

      <div class="result-section">
        <div class="result-header">
          <p class="result-title">
            {{ $t('calculator.resultTable') }}: <span>{{ selectedClass === 'Science' ? $t('calculator.science') : $t('calculator.social') }} {{ $t('calculator.class') }}</span>
          </p>
          <button class="delete-btn" @click="resetAll">
            <svg class="delete-vector" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
            {{ $t('calculator.delete') }}
          </button>
        </div>
        <div class="result-table">
          <div class="result-cell">
            <p class="result-cell-label">{{ $t('calculator.result') }}</p>
            <p class="result-cell-value">
              {{ calculated ? (result === 'Pass' ? $t('calculator.pass') : $t('calculator.fail')) : '—' }}
            </p>
          </div>
          <div class="result-cell result-cell--highlight">
            <p class="result-cell-label">{{ $t('calculator.total') }}</p>
            <p class="result-cell-value">{{ calculated ? totalScore + ' ' + $t('calculator.pts') : '—' }}</p>
          </div>
          <div class="result-cell">
            <p class="result-cell-label">{{ $t('calculator.grade') }}</p>
            <p class="result-cell-value grade-large">
              {{ calculated ? overallGrade : '—' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CalculatorView',
  data() {
  return {
    selectedClass: 'Science',
    totalScore: 0,
    totalMax: 0,
    overallGrade: '',
    calculated: false,
    result: '',
        scienceMain: [
      { key: 'mathematics', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#2563EB" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 15.3a2.82 2.82 0 0 1 0 4c-1 1-2.5 1-3.5 0L2.8 4.3c-1-1-1-2.5 0-3.5s2.5-1 3.5 0Z"/><path d="M5.6 7.2 7.2 5.6"/><path d="M9.9 11.5l1.6-1.6"/><path d="M14.2 15.8l1.6-1.6"/></svg>`, score: null, maxScore: 125 },
      { key: 'physics', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#2563EB" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 21h2"/><path d="M12 17v4"/><path d="M14 4A22 22 0 0 0 3 15"/><path d="M17 14A22 22 0 0 0 6 3"/><circle cx="12" cy="12" r="3"/><path d="m14.2 14.2 4.3 4.3"/></svg>`, score: null, maxScore: 75 },
      { key: 'chemistry', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#EA580C" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 3h15"/><path d="M6 3v13a4 4 0 0 0 4 4h4a4 4 0 0 0 4-4V3"/><path d="M6 14h12"/></svg>`, score: null, maxScore: 75 },
      { key: 'biology', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#0D9488" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 10.5C7.8 13.8 13.2 13.8 16.5 10.5c.3-.3.3-.8 0-1.1-.3-.3-.8-.3-1.1 0-2.7 2.7-7.1 2.7-9.8 0-.3-.3-.8 0-1.1.3-.3.8-.3 1.1 0Z"/><path d="M12 12c-1.5 0-2.7-1.2-2.7-2.7S10.5 6.6 12 6.6s2.7 1.2 2.7 2.7S13.5 12 12 12Z"/></svg>`, score: null, maxScore: 75 },
      { key: 'khmerLiterature', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#EA580C" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2-2.5z"/><path d="M6 6h10"/><path d="M6 10h10"/><path d="M6 14h10"/></svg>`, score: null, maxScore: 75 },
      { key: 'english', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#DC2626" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`, score: null, maxScore: 50, half: true },
    ],
    scienceSelection: [{ key: 'history', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#B45309" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/><path d="M14 3v5h5"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>`, score: null, maxScore: 50 }],
    socialMain: [
      { key: 'khmerLanguage', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#EA580C" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`, score: null, maxScore: 125 },
      { key: 'mathematics', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#2563EB" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 15.3a2.82 2.82 0 0 1 0 4c-1 1-2.5 1-3.5 0L2.8 4.3c-1-1-1-2.5 0-3.5s2.5-1 3.5 0Z"/><path d="M5.6 7.2 7.2 5.6"/><path d="M9.9 11.5l1.6-1.6"/><path d="M14.2 15.8l1.6-1.6"/></svg>`, score: null, maxScore: 75 },
      { key: 'history', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#B45309" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/><path d="M14 3v5h5"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>`, score: null, maxScore: 75 },
      { key: 'moralCivics', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#4F46E5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="22"/><line x1="5" y1="7" x2="19" y2="7"/><path d="M19 7c0 5-3.5 8-7 8s-7-3-7-8"/></svg>`, score: null, maxScore: 75 },
      { key: 'geography', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#0D9488" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" y1="3" x2="9" y2="18"/><line x1="15" y1="6" x2="15" y2="21"/></svg>`, score: null, maxScore: 75 },
      { key: 'foreignLanguage', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#DB2777" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`, score: null, maxScore: 50, half: true },
    ],
    socialSelection: [{ key: 'earthScience', icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="#10B981" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>`, score: null, maxScore: 50 }],
  }
},
  computed: {
    mainSubjects() {
      return this.selectedClass === 'Science' ? this.scienceMain : this.socialMain
    },
    selectionSubjects() {
      return this.selectedClass === 'Science' ? this.scienceSelection : this.socialSelection
    },
  },
  methods: {
    clamp(score, maxScore) {
      if (score < 0) return 0
      if (score > maxScore) return maxScore
      return score
    },
    calculate(score, maxScore) {
      const percentage = (score / maxScore) * 100
      const grades = [
        { min: 90, grade: 'A' },
        { min: 80, grade: 'B' },
        { min: 70, grade: 'C' },
        { min: 60, grade: 'D' },
        { min: 49.894736842, grade: 'E' },
      ]
      for (const grade of grades) {
        if (percentage >= grade.min) return grade.grade
      }
      return 'F'
    },
    calculateTotal() {
      this.totalScore = 0
      this.totalMax = 0
      this.calculated = true

      const allSubjects = [...this.mainSubjects, ...this.selectionSubjects]

      this.totalScore = allSubjects.reduce((s, c) => {
        let score
        if (c.half) {
          if (c.score >= 25) {
            score = (c.score || 0) - 25
          } else {
            score = 0
          }
        } else {
          score = c.score || 0
        }
        return score + s
      }, 0)

      this.result = this.totalScore >= 237 ? 'Pass' : 'Fail'
      this.overallGrade = this.calculate(this.totalScore, 475)
    },
    resetAll() {
      const allSubjects = [
        ...this.scienceMain,
        ...this.socialMain,
        ...this.socialSelection,
        ...this.scienceSelection,
      ]
      allSubjects.forEach((s) => (s.score = null))
      this.calculated = false
      this.totalScore = 0
      this.totalMax = 0
      this.overallGrade = ''
    },
  },
}
</script>

<style scoped>
.calculator-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-left: 180px;
  max-width: 860px;
}
@media (max-width: 1024px) {
  .calculator-page {
    margin-left: 0;
    padding: 0 20px;
  }
}
@media (max-width: 768px) {
  .calculator-page {
    padding: 0 12px;
  }
}

.calc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: 16px;
  padding: 20px 24px;
}

.calc-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 3px;
}

.calc-subtitle {
  font-size: 12px;
  color: var(--gray-500);
}

.class-toggle {
  display: flex;
  background: var(--gray-100);
  border-radius: 10px;
  padding: 4px;
  gap: 4px;
}

.toggle-btn {
  padding: 8px 20px;
  border-radius: 7px;
  border: none;
  background: transparent;
  font-size: 13px;
  font-weight: 600;
  color: var(--gray-500);
  transition: all 0.15s;
}

.toggle-btn--active {
  background: var(--navy);
  color: var(--white);
}

.calc-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.subject-group {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: 16px;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.group-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: var(--navy);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e74c3c;
  display: inline-block;
  flex-shrink: 0;
}

.subject-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.subject-card {
  border: 1px solid var(--gray-100);
  border-radius: 12px;
  overflow: hidden;
  transition: border-color 0.15s;
}
@media (max-width: 768px) {
  .subject-grid {
    grid-template-columns: 1fr;
  }
}

.subject-card:hover {
  border-color: var(--amber);
}

.subject-card-top {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px 10px;
}

.subject-icon {
  font-size: 18px;
}

.subject-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--navy);
}

.subject-card-bottom {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--gray-50);
  padding: 9px 14px;
  border-top: 1px solid var(--gray-100);
}

.score-input {
  width: 70px;
  padding: 5px 8px;
  border: 1.5px solid var(--gray-100);
  border-radius: 7px;
  font-size: 13px;
  font-family: inherit;
  color: var(--navy);
  font-weight: 600;
  outline: none;
  background: var(--white);
  transition: border-color 0.15s;
}

.score-input:focus {
  border-color: var(--navy);
}

.max-score {
  font-size: 11px;
  color: var(--gray-500);
  flex: 1;
}

.grade-badge {
  font-size: 15px;
  font-weight: 800;
  width: 28px;
  height: 28px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.find-total-btn {
  background: var(--navy);
  color: var(--white);
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.find-total-btn:hover {
  opacity: 0.85;
}

.result-section {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: 16px;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.result-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--navy);
}

.result-title span {
  color: var(--amber);
}

.delete-btn {
  background: transparent;
  border: 1.5px solid #ffd0d0;
  color: #c0392b;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
  display: flex;
}
@media (max-width: 480px) {
  .delete-btn {
    padding: 4px 10px;
  }
  .find-total-btn {
    font-size: 16px;
    padding: 8px 16px;
  }
}

.delete-btn:hover {
  background: #fff5f5;
}

.result-table {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--gray-100);
}

.result-cell {
  padding: 24px;
  text-align: center;
  background: var(--gray-50);
  border-right: 1px solid var(--gray-100);
}

.result-cell:last-child {
  border-right: none;
}

.result-cell--highlight {
  background: var(--navy);
}

.result-cell--highlight .result-cell-label,
.result-cell--highlight .result-cell-value {
  color: var(--white);
}

.result-cell-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-500);
  margin-bottom: 12px;
}

.result-cell-value {
  font-size: 20px;
  font-weight: 800;
  color: var(--navy);
}

.grade-large {
  font-size: 28px;
  padding: 4px 12px;
  border-radius: 8px;
  display: inline-block;
}
</style>
