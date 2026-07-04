<template>
  <div class="home">
    <section class="hero">
      <div class="hero-text">
        <span class="hero-eyebrow">{{ $t('message.useAIforFree') }}</span>
        <h1 class="hero-title">
          Your BacII Exam<br />
          <span class="hero-accent">Smart Tutor</span>
        </h1>
        <p class="hero-body">
          {{ $t('message.asking') }} {{ $t('message.asking2') }}
        </p>
        <div class="hero-actions">
          <router-link to="/bot" class="btn-primary">{{ $t('message.askQuestion') }}</router-link>
          <router-link to="/pasttests" class="btn-ghost">{{ $t('message.browsePastTests') }}</router-link>
        </div>
      </div>

      <div class="hero-visual">
        <div class="chat-preview">
          <div class="pb pb-user">{{ $t('message.question') }}</div>
          <div class="pb pb-bot">
            {{ $t('message.answer') }}
          </div>
          <div class="pb pb-user">{{ $t('message.followUp') }}</div>
          <div class="pb-typing"><span></span><span></span><span></span></div>
        </div>
      </div>
    </section>

    <section class="stats">
      <div class="stat" v-for="s in stats" :key="s.labelKey">
        <p class="stat-value">{{ $t('message.stats.' + s.value) }}</p>
        <p class="stat-label">{{ $t('message.stats.' + s.labelKey) }}</p>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <h2 class="section-title">{{ $t('message.subjectsCovered') }}</h2>
        <router-link to="/pasttests" class="section-link">{{ $t('message.viewAll') }} →</router-link>
      </div>

      <div class="subject-cards">
        <router-link to="/bot" v-for="subject in subjects" :key="subject.key" class="subject-card">
          <div class="subject-card-cover" :style="{ background: subject.gradient }">
            <img
              :src="subject.image"
              :alt="$t('tests.subjects.' + subject.key)"
              class="subject-card-icon"
              v-if="subject.image"
            />
          </div>
          <div class="subject-card-body">
            <p class="subject-card-name">{{ $t('tests.subjects.' + subject.key) }}</p>
            <p class="subject-card-desc">{{ $t('home.subjectDescs.' + subject.key) }}</p>
            <div class="subject-card-footer">
              <span class="subject-card-cta">{{ $t('home.askAbout') }} {{ $t('tests.subjects.' + subject.key) }}</span>
              <span class="subject-card-arrow">→</span>
            </div>
          </div>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      stats: [
        { value: 'subjectsValue', labelKey: 'subjects' },
        { value: 'yearsOfPastTestsValue', labelKey: 'yearsOfPastTests' },
        { value: 'alwaysAvailableValue', labelKey: 'alwaysAvailable' },
        { value: 'noCostNoSignupValue', labelKey: 'noCostNoSignup' }
      ],
      subjects: [
        {
          key: 'mathematics',
          image: 'files/math.jpg',
          gradient: 'linear-gradient(135deg, #1a3a7a, #3a5fb0)',
        },
        {
          key: 'physics',
          image: 'files/physic.jpg',
          gradient: 'linear-gradient(135deg, #0f4c5c, #1a7a8f)',
        },
        {
          key: 'chemistry',
          image: 'files/chemistry.jpg',
          gradient: 'linear-gradient(135deg, #6a2a7a, #a3459c)',
        },
        {
          key: 'biology',
          image: 'files/biology.jpg',
          topicCount: 11,
          gradient: 'linear-gradient(135deg, #1e6b3a, #3fa35c)',
        },
        {
          key: 'history',
          image: 'files/history.jpg',
          topicCount: 8,
          gradient: 'linear-gradient(135deg, #8a4a1a, #c17a3a)',
        },
        {
          key: 'literatureenglish',
          image: 'files/english.jpg',
          topicCount: 10,
          gradient: 'linear-gradient(135deg, #a3251f, #d64a3f)',
        },
        {
          key: 'khmerliterature',
          image: 'files/khmer-literature.jpg',
          topicCount: 7,
          gradient: 'linear-gradient(135deg, #7a1f4a, #b8447a)',
        },
        {
          key: 'geography',
          image: 'files/geography.jpg',
          topicCount: 6,
          gradient: 'linear-gradient(135deg, #1f6b6b, #3fa3a3)',
        },
        {
          key: 'earthScience',
          image: 'files/earth-science.jpg',
          topicCount: 8,
          gradient: 'linear-gradient(135deg, #2a5a1f, #5c9c3f)',
        },
        {
          key: 'moralCivics',
          image: 'files/moral-and-civics.jpg',
          topicCount: 6,
          gradient: 'linear-gradient(135deg, #3a3a6a, #6060a3)',
        },
      ],
    }
  },
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: center;
  background: var(--white);
  border-radius: 18px;
  padding: 40px;
  border: 1px solid var(--gray-100);
}
@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

.hero-eyebrow {
  display: inline-block;
  background: var(--amber-light);
  color: #b97d0a;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 11px;
  border-radius: 20px;
  letter-spacing: 0.03em;
  margin-bottom: 14px;
}

.hero-title {
  font-size: 36px;
  font-weight: 800;
  line-height: 1.15;
  color: var(--navy);
  margin-bottom: 13px;
}

.hero-accent {
  color: var(--amber);
}

.hero-body {
  color: var(--gray-500);
  font-size: 13.5px;
  line-height: 1.7;
  margin-bottom: 22px;
  max-width: 360px;
}

.hero-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-primary {
  background: var(--navy);
  color: var(--white);
  padding: 11px 20px;
  border-radius: 9px;
  font-weight: 700;
  font-size: 13px;
  transition: opacity 0.15s;
}

.btn-primary:hover {
  opacity: 0.85;
}

.btn-ghost {
  background: var(--gray-100);
  color: var(--navy);
  padding: 11px 20px;
  border-radius: 9px;
  font-weight: 600;
  font-size: 13px;
  transition: background 0.15s;
}

.btn-ghost:hover {
  background: var(--gray-300);
}

.hero-visual {
  display: flex;
  justify-content: center;
}

.chat-preview {
  background: var(--gray-50);
  border: 1px solid var(--gray-100);
  border-radius: 14px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  max-width: 320px;
}

.pb {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 12.5px;
  line-height: 1.6;
  max-width: 85%;
}

.pb-user {
  background: var(--navy);
  color: var(--white);
  align-self: flex-end;
  border-bottom-right-radius: 3px;
}

.pb-bot {
  background: var(--white);
  color: var(--text);
  border: 1px solid var(--gray-100);
  align-self: flex-start;
  border-bottom-left-radius: 3px;
}

.pb-typing {
  display: flex;
  gap: 4px;
  padding: 11px 14px;
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: 12px;
  border-bottom-left-radius: 3px;
  width: fit-content;
}

.pb-typing span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--amber);
  animation: bounce 1.2s infinite;
}

.pb-typing span:nth-child(2) {
  animation-delay: 0.2s;
}
.pb-typing span:nth-child(3) {
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
    transform: translateY(-5px);
    opacity: 1;
  }
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
@media (max-width: 768px) {
  .stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: var(--radius);
  padding: 20px;
  text-align: center;
}

.stat-value {
  font-size: 26px;
  font-weight: 800;
  color: var(--navy);
  margin-bottom: 3px;
}

.stat-label {
  font-size: 11px;
  color: var(--gray-500);
  font-weight: 500;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.section-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--navy);
}

.section-link {
  font-size: 12px;
  font-weight: 600;
  color: var(--amber);
}

.subject-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.subject-card {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: 16px;
  overflow: hidden;
  display: grid;
  grid-template-rows: auto 1fr;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    border-color 0.18s ease;
}
@media (max-width: 1024px) {
  .subject-cards {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 768px) {
  .subject-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

.subject-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 26px rgba(15, 32, 68, 0.12);
  border-color: transparent;
}

.subject-card-cover {
  position: relative;
  height: 165px;
  display: grid;
  place-items: center;
  overflow: hidden;
}

.subject-card-cover::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 75% 20%, rgba(255, 255, 255, 0.18), transparent 60%);
}

.subject-card-icon {
  font-size: 40px;
  filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.25));
  z-index: 1;
}

.subject-card-topics {
  position: absolute;
  bottom: 8px;
  right: 10px;
  background: rgba(0, 0, 0, 0.28);
  backdrop-filter: blur(2px);
  color: var(--white);
  font-size: 10px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 20px;
  z-index: 1;
}

.subject-card-body {
  padding: 14px 16px 16px;
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 6px;
}

.subject-card-name {
  font-size: 14.5px;
  font-weight: 800;
  color: var(--navy);
}

.subject-card-desc {
  font-size: 11.5px;
  color: var(--gray-500);
  line-height: 1.5;
  flex: 1;
}

.subject-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
  padding-top: 10px;
  border-top: 1px solid var(--gray-100);
}

.subject-card-cta {
  font-size: 11px;
  font-weight: 700;
  color: var(--navy);
}

.subject-card-arrow {
  font-size: 13px;
  font-weight: 700;
  color: var(--amber);
  transition: transform 0.18s ease;
}

.subject-card:hover .subject-card-arrow {
  transform: translateX(3px);
}
</style>