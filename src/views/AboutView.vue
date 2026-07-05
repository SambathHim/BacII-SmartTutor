<template>
  <section class="about">
    <div class="about-header">
      <span class="about-eyebrow">{{ $t('about.eyebrow') }}</span>
      <h2 class="about-title">{{ $t('about.title') }}</h2>
      <p class="about-subtitle">{{ $t('about.subtitle') }}</p>
    </div>

    <div class="about-body">
      <div class="about-text">
        <p v-html="$t('about.intro')"></p>

        <p v-html="$t('about.philosophy')"></p>

        <p class="copyright-text">
          <strong>{{ $t('about.copyrightNotice') }}</strong>
        </p>
        <router-link to="/bot" class="about-cta">{{ $t('about.cta') }} →</router-link>
      </div>

      <div class="about-features">
        <div class="feature" v-for="f in features" :key="f.key">
          <span class="feature-icon" :style="{ color: f.color }" v-html="f.icon"></span>
          <div>
            <p class="feature-title">{{ $t('about.features.' + f.key + '.title') }}</p>
            <p class="feature-desc">{{ $t('about.features.' + f.key + '.desc') }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
export default {
  name: 'AboutView',
  data() {
    return {
        features: [
          { 
            key: 'aiPowered', 
            color: '#3b82f6', 
            icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>` 
          },
          { 
            key: 'pastExams', 
            color: '#a855f7', 
            icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>` 
          },
          { 
            key: 'examFocused', 
            color: '#ef4444', 
            icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>` 
          },
          { 
            key: 'completelyFree', 
            color: '#22c55e', 
            icon: `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01"/><path d="M18 12h.01"/></svg>` 
          },
        ]

    }
  },
}
</script>
<style scoped>
.about {
  background: var(--navy);
  border-radius: 20px;
  padding: 48px;
  display: flex;
  flex-direction: column;
  gap: 36px;
}
@media (max-width: 768px) {
  .about {
    padding: 32px;
    gap: 28px;
  }
}

.about-header {
  text-align: center;
}

.about-eyebrow {
  display: inline-block;
  background: rgba(245, 166, 35, 0.15);
  color: var(--amber);
  font-size: 11px;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 20px;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.about-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--white);
  margin-bottom: 8px;
}

.about-subtitle {
  font-size: 13.5px;
  color: #8fa3c8;
}

.about-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.about-text {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.about-text p {
  font-size: 13px;
  color: #b8c8e0;
  line-height: 1.8;
}

.about-text strong {
  color: var(--white);
  font-weight: 700;
}
.copyright-text {
  font-size: 13px;
  color: #8fa3c8;
  line-height: 1.8;
  font-style: italic;
  text-decoration: underline;
}
.about-cta {
  display: inline-block;
  margin-top: 8px;
  background: var(--amber);
  color: var(--navy);
  font-size: 13px;
  font-weight: 700;
  padding: 11px 22px;
  border-radius: 9px;
  width: fit-content;
  transition: opacity 0.15s;
}

.about-cta:hover {
  opacity: 0.88;
}

/* Feature cards */
.about-features {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.feature {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 16px 18px;
  transition: background 0.15s;
}

.feature:hover {
  background: rgba(255, 255, 255, 0.08);
}

.feature-icon {
  font-size: 22px;
  flex-shrink: 0;
  margin-top: 1px;
  color: white;
}

.feature-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--white);
  margin-bottom: 3px;
}

.feature-desc {
  font-size: 12px;
  color: #8fa3c8;
  line-height: 1.5;
}
@media (max-width: 900px) {
  .about-body {
    grid-template-columns: 1fr;
    gap: 28px;
  }
}

@media (max-width: 640px) {
  .about {
    padding: 24px 20px;
    gap: 22px;
    border-radius: 16px;
  }

  .about-eyebrow {
    font-size: 10px;
    padding: 3px 10px;
  }

  .about-title {
    font-size: 22px;
  }

  .about-subtitle {
    font-size: 12.5px;
  }

  .about-body {
    gap: 22px;
  }

  .about-text p {
    font-size: 12.5px;
    line-height: 1.7;
  }

  .copyright-text {
    font-size: 12px;
  }

  .about-cta {
    width: 100%;
    text-align: center;
    padding: 12px 18px;
  }

  .feature {
    padding: 14px 15px;
    gap: 12px;
  }

  .feature-icon svg {
    width: 18px;
    height: 18px;
  }

  .feature-title {
    font-size: 12.5px;
  }

  .feature-desc {
    font-size: 11px;
  }
}

@media (max-width: 400px) {
  .about {
    padding: 20px 16px;
  }

  .about-title {
    font-size: 19px;
  }

  .feature {
    flex-direction: column;
    gap: 8px;
  }

  .feature-icon {
    margin-top: 0;
  }
}
</style>