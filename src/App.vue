<template>
  <div class="layout">
    <div 
      v-if="isMobileMenuOpen" 
      class="sidebar-overlay" 
      @click="toggleMobileMenu"
    ></div>

    <aside class="sidebar" :class="{ 'sidebar--open': isMobileMenuOpen }">
      <div class="brand">
        <svg class="brand-icon" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M6 18.8v-4L2 13"/><path d="M12 14.5V20a2 2 0 0 0 2 2h2"/></svg>
        <div @click="goBackHome" class="cursor-pointer">
          <p class="brand-name">BacII</p>
          <p class="brand-sub">SmartTutor</p>
        </div>
        <button class="mobile-close" @click="toggleMobileMenu">✕</button>
      </div>
      
      <nav class="nav" @click="closeMobileMenu">
        <router-link to="/" class="nav-link" active-class="nav-link--active" exact>
          <svg class="nav-icon-home" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          {{ $t('nav.home') }}
        </router-link>
        <router-link to="/bot" class="nav-link" active-class="nav-link--active">
          <svg class="nav-icon-chatbot" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          {{ $t('nav.chatbot') }}
        </router-link>
        <router-link to="/pasttests" class="nav-link" active-class="nav-link--active">
          <svg class="nav-icon-passtests" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          {{ $t('nav.pastexams') }}
        </router-link>
        <router-link to="/calculator" class="nav-link" active-class="nav-link--active">
          <svg class="nav-icon-calculator" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/></svg>
          {{ $t('nav.calculator') }}
        </router-link>
        <router-link to="/quiz" class="nav-link" active-class="nav-link--active">
          <svg class="nav-icon-quiz" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          {{ $t('nav.quiz') }}
        </router-link>
        <router-link to="/about" class="nav-link" active-class="nav-link--active">
          <svg class="nav-icon-about" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          {{ $t('nav.about') }}
        </router-link>
      </nav>

      <div class="sidebar-card">
        <p class="sidebar-card-title">{{ $t('sidebar.title') }}</p>
        <p class="sidebar-card-body">{{ $t('sidebar.body') }}</p>
        <router-link to="/bot" class="sidebar-card-btn" @click="closeMobileMenu">{{ $t('sidebar.cta') }}</router-link>
      </div>
    </aside>

    <div class="main-wrap">
      <header class="topbar">
        <div class="topbar-left">
          <button class="mobile-toggle" @click="toggleMobileMenu">☰</button>
            <div class="topbar-countdown">
              <div class="tc-label-row">
                <svg class="topbar-countdown-icon"  xmlns="http://www.w3.org/2000/svg" width="24" height="24"  
                  fill="darkblue" viewBox="0 0 24 20" >
                  <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                  <path d="M19.07 4.93a9.9 9.9 0 0 0-3.18-2.14A9.95 9.95 0 0 0 12 2c-.55 0-1 .45-1 1v5h2V4.06c.73.09 1.44.28 2.11.57.95.4 1.81.98 2.54 1.72.74.73 1.31 1.59 1.71 2.54.42.99.63 2.03.63 3.11s-.21 2.13-.63 3.11c-.4.95-.98 1.81-1.72 2.54-.73.74-1.59 1.31-2.54 1.71-1.97.83-4.26.83-6.23 0-.95-.4-1.81-.98-2.54-1.72a7.8 7.8 0 0 1-1.71-2.54c-.42-.99-.63-2.03-.63-3.11s.21-2.13.63-3.11c.4-.95.98-1.81 1.72-2.54L4.93 4.92c-.92.92-1.64 1.99-2.14 3.18C2.27 9.33 2 10.64 2 11.99s.26 2.66.79 3.89c.5 1.19 1.23 2.26 2.14 3.18s1.99 1.64 3.18 2.14c1.23.52 2.54.79 3.89.79s2.66-.26 3.89-.79c1.19-.5 2.26-1.23 3.18-2.14s1.64-1.99 2.14-3.18c.52-1.23.79-2.54.79-3.89s-.26-2.66-.79-3.89c-.5-1.19-1.23-2.26-2.14-3.18Z"></path><path d="M12.88 11.12 8 8l3.12 4.88c1.22 1.68 3.45-.55 1.77-1.77Z"></path>
                  </svg>
                <span class="tc-label">{{ $t('message.countdown') }}</span>
              </div>
                <div class="tc-chips">
                  <div class="tc-chip">
                    <span class="tc-num">{{ toKhmerDigits(countdown.days) }}</span>
                    <span class="tc-unit">{{ $t('message.days') }}</span>
                  </div>
                  <span class="tc-sep">:</span>
                  <div class="tc-chip">
                    <span class="tc-num">{{ toKhmerDigits(countdown.hours) }}</span>
                    <span class="tc-unit">{{ $t('message.hours') }}</span>
                  </div>
                  <span class="tc-sep">:</span>
                  <div class="tc-chip">
                    <span class="tc-num">{{ toKhmerDigits(countdown.minutes) }}</span>
                    <span class="tc-unit">{{ $t('message.minutes') }}</span>
                  </div>
                  <span class="tc-sep">:</span>
                  <div class="tc-chip">
                    <span class="tc-num">{{ toKhmerDigits(countdown.seconds) }}</span>
                    <span class="tc-unit">{{ $t('message.seconds') }}</span>
                  </div>
                </div>
            </div>
        </div>
        
        <div class="flex gap-5">
          <button v-if="$i18n.locale == 'kh'" 
                class="topbar-change-lang-en" @click="changeLanguage('en')" :class="{ active: $i18n.locale === 'en' }">
                ENG
          </button>
          <button v-if="$i18n.locale == 'en'" 
                class="topbar-change-lang-kh" @click="changeLanguage('kh')" :class="{ active: $i18n.locale === 'kh' }">
                KHM
          </button>
          <div class="topbar-user"><svg class="topbar-user-icon"  xmlns="http://www.w3.org/2000/svg" width="18" height="18"  
            fill="currentColor" viewBox="0 0 24 24" >
            <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
            <path d="M12 12c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5m0-8c1.65 0 3 1.35 3 3s-1.35 3-3 3-3-1.35-3-3 1.35-3 3-3M4 22h16c.55 0 1-.45 1-1v-1c0-3.86-3.14-7-7-7h-4c-3.86 0-7 3.14-7 7v1c0 .55.45 1 1 1m6-7h4c2.76 0 5 2.24 5 5H5c0-2.76 2.24-5 5-5"></path>
            </svg> {{$t('message.student')}}</div>
        </div>
      </header>
      <main class="content">
        <router-view v-slot="{ Component }">
          <keep-alive include="BotView">
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'App',
  name: 'BotView',

  data() {
    return {
      isMobileMenuOpen: false,
      examDate: new Date('2026-08-10T00:00:00'),
      countdown: {
        days: '00',
        hours: '00',
        minutes: '00',
        seconds: '00'
      },
      countdownTimer: null
    }
  },

  created() {
    this.$route = useRoute()
    this.$router = useRouter()
  },

  mounted() {
    this.timer()
    this.countdownTimer = setInterval(this.timer, 1000)
  },

  beforeUnmount() {
    clearInterval(this.countdownTimer)
  },

  methods: {
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen
    },
    closeMobileMenu() {
      this.isMobileMenuOpen = false
    },
    goBackHome() {
      this.closeMobileMenu()
      this.$router.push('/')
    },
    changeLanguage(lang) {
      this.$i18n.locale = lang
      localStorage.setItem('language', lang)
    },
    timer() {
      const now = new Date()
      const timeDifference = this.examDate - now
      if (timeDifference <= 0) {
        this.countdown.days = '00'
        this.countdown.hours = '00'
        this.countdown.minutes = '00'
        this.countdown.seconds = '00'
        clearInterval(this.countdownTimer)
        return
      }
      this.countdown.days = Math.floor(timeDifference / 1000 / 60 / 60 / 24)
        .toString()
        .padStart(2, '0')
      this.countdown.hours = Math.floor((timeDifference / 1000 / 60 / 60) % 24)
        .toString()
        .padStart(2, '0')
      this.countdown.minutes = Math.floor((timeDifference / 1000 / 60) % 60)
        .toString()
        .padStart(2, '0')
      this.countdown.seconds = Math.floor((timeDifference / 1000) % 60)
        .toString()
        .padStart(2, '0')
    },
    toKhmerDigits(str) {
      if (this.$i18n.locale !== 'kh') return str
      const khmerDigits = ['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩']
      return str.toString().replace(/[0-9]/g, (d) => khmerDigits[d])
    },
  },
  
}
</script>

<style>
:root {
  --sidebar-w: 260px;
}

.layout {
  display: flex;
  min-height: 100vh;
}

.main-wrap {
  margin-left: var(--sidebar-w);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: calc(100% - var(--sidebar-w));
}

.content {
  padding: 28px;
  flex: 1;
  min-width: 0;
}

.topbar {
  flex-wrap: nowrap;
  overflow-x: auto; 
  -webkit-overflow-scrolling: touch;
}

.topbar-left {
  flex-wrap: nowrap;
  flex-shrink: 1;
  min-width: 0;
}

.topbar-countdown {
  flex-wrap: nowrap;
  min-width: 0;
}

.tc-label-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 3px;
  flex-shrink: 0;
}

.tc-chips {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-wrap: wrap;
}

.tc-chip {
  display: flex;
  align-items: baseline;
  gap: 2px;
  border-radius: 6px;
  padding: 4px 8px;
  background: var(--gray-50, #f4f6fb);
}

.tc-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.tc-label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 90px;
}

.tc-num {
  font-size: 18px;
  font-weight: 800;
  color: rgb(0, 0, 122);
  font-variant-numeric: tabular-nums;
}

.tc-unit {
  font-size: 10px;
  font-weight: 600;
  color: rgb(0, 0, 144);
}

.tc-sep {
  font-size: 12px;
  font-weight: 700;
  color: var(--gray-300);
}

.topbar-user {
  display: flex;
  align-items: center;
  background: var(--gray-100);
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-700);
  white-space: nowrap;
  flex-shrink: 0;
}

.topbar-user-icon {
  margin-right: 6px;
  color: rgb(0, 0, 86);
}

.topbar-change-lang-en,
.topbar-change-lang-kh {
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  flex-shrink: 0;
}

.topbar-change-lang-en {
  background: rgb(0, 0, 122);
}
.topbar-change-lang-kh {
  background: rgb(123, 0, 0);
}
.topbar-change-lang-en:hover {
  background: rgb(0, 0, 86);
}

.mobile-toggle,
.mobile-close {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
}

.mobile-toggle {
  font-size: 24px;
  color: var(--gray-700);
  padding: 4px 8px;
}

.mobile-close {
  color: #8fa3c8;
  font-size: 20px;
  margin-left: auto;
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 9;
}

.sidebar {
  width: var(--sidebar-w);
  background: var(--navy);
  display: flex;
  flex-direction: column;
  padding: 24px 14px;
  gap: 28px;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 10;
  transition: transform 0.3s ease;
  overflow-y: auto;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 6px;
  width: 100%;
}

.brand-icon {
  font-size: 26px;
  color: var(--amber);
  flex-shrink: 0;
}

.brand-name {
  font-size: 17px;
  font-weight: 800;
  color: var(--white);
  line-height: 1;
}

.brand-sub {
  font-size: 11px;
  color: var(--amber);
  font-weight: 700;
  letter-spacing: 0.04em;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.nav-link {
  margin-top: 5px;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 10px 12px;
  border-radius: 9px;
  color: #8fa3c8;
  font-size: 13.5px;
  font-weight: 500;
  transition: all 0.15s;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.07);
  color: var(--white);
}

.nav-link--active {
  background: var(--amber) !important;
  color: var(--navy) !important;
  font-weight: 700;
}

.sidebar-card {
  margin-top: auto;
  background: var(--navy-mid);
  border-radius: var(--radius);
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.sidebar-card-title {
  font-weight: 700;
  color: var(--white);
  font-size: 13px;
  margin-bottom: 5px;
}

.sidebar-card-body {
  font-size: 11.5px;
  color: #8fa3c8;
  margin-bottom: 12px;
  line-height: 1.5;
}

.sidebar-card-btn {
  display: block;
  text-align: center;
  background: var(--amber);
  color: var(--navy);
  font-weight: 700;
  font-size: 12px;
  padding: 8px;
  border-radius: 7px;
  transition: opacity 0.15s;
}

@media (max-width: 1024px) {
  .mobile-toggle,
  .mobile-close {
    display: block;
  }

  .main-wrap {
    margin-left: 0;
    width: 100%;
  }

  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar--open {
    transform: translateX(0);
  }

  .topbar {
    padding: 12px 20px;
  }

  .content {
    padding: 22px;
  }
}

@media (max-width: 768px) {
  .topbar {
    padding: 10px 16px;
    gap: 10px;
  }

  .topbar-countdown-icon {
    width: 18px;
    height: 18px;
  }

  .tc-label,
  .tc-num,
  .tc-unit {
    font-size: 12px;
  }

  .tc-num {
    font-size: 15px;
  }

  .content {
    padding: 18px;
  }

  .topbar-user span {
    display: none;
  }
}

@media (max-width: 480px) {
  .tc-label {
    font-size: 9px;
    max-width: 70px;
  }
  .tc-num {
    font-size: 11px;
  }
  .tc-unit {
    font-size: 8px;
  }
  .tc-chip {
    padding: 2px 5px;
  }

  .topbar-user,
  .topbar-change-lang-en,
  .topbar-change-lang-kh {
    padding: 4px 8px;
    font-size: 9px;
  }
}

@media (max-width: 380px) {
  .tc-label {
    display: none; 
  }

  .topbar-user {
    padding: 5px 8px;
  }

  .topbar-user svg + span,
  .topbar-user {
    font-size: 10px;
  }
}
</style>