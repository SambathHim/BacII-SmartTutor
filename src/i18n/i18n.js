// src/i18n.js
import { createI18n } from 'vue-i18n';
import en from '../locales/en';
import kh from '../locales/kh';

const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: 'kh', // Default language
  fallbackLocale: 'en', // Fallback language
  messages: {
    en,
    kh
  }
});

export default i18n;