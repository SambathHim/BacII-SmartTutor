<template>
  <div class="tests-page">
    <div class="tabs">
      <button
        class="tab"
        :class="{ 'tab--active': activeTab === 'past' }"
        @click="activeTab = 'past'"
      >
        {{ $t('tests.pastTests') }} <span class="tab-badge">{{ $t('tests.yearsOfPastTests') }}</span>
      </button>
      <button
        class="tab"
        :class="{ 'tab--active': activeTab === 'special' }"
        @click="activeTab = 'special'"
      >
        {{ $t('tests.specialTests') }}
      </button>
    </div>

    <div class="tests-list">
      <div
        v-for="subject in activeTab === 'past' ? pastTests : specialTests"
        :key="subject.name"
        class="test-card-wrapper"
      >
        <div
          class="test-card"
          @click="toggleSubject(subject.name)"
        >
          <span class="test-icon" v-html="subject.icon"></span>

          <div class="test-info">
            <p class="test-name">{{ $t(`tests.subjects.${subject.slug}`) }}</p>
            <p class="test-years">
              {{ activeTab === 'past' ? $t('tests.yearsOfPastTests') : $t('tests.specialEdition') }}
            </p>
          </div>

          <span class="expand-btn">
            <svg v-if="expandedSubject === subject.name" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
          </span>
        </div>

        <div
          v-if="expandedSubject === subject.name"
          class="file-row"
        >
          <button
            v-if="subject.file"
            class="file-btn"
            @click.stop="openPDF(subject)"
          >
            <svg class="file-vector" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>
            {{ $t(`PastTests.subjects.${subject.slug}`) }}.pdf
          </button>
          <p v-else class="no-file">No file available yet.</p>
        </div>
      </div>
    </div>

    <div v-if="activePDF" class="pdf-modal" @click.self="closePDF">
      <div class="pdf-modal-content">
        <div class="pdf-modal-header">
          <span>{{ activePDFName }}</span>
          <button class="pdf-close-btn" @click="closePDF">✕</button>
        </div>
        <iframe :src="activePDF" class="pdf-frame"></iframe>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TestsView",

  data() {
    return {
      activeTab: "past",
      expandedSubject: null,
      activePDF: null,
      activePDFName: "",

      pastTests: [
        { name: "Mathematics", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#2563EB" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 15.3a2.82 2.82 0 0 1 0 4c-1 1-2.5 1-3.5 0L2.8 4.3c-1-1-1-2.5 0-3.5s2.5-1 3.5 0Z"/><path d="M5.6 7.2 7.2 5.6"/><path d="M9.9 11.5l1.6-1.6"/><path d="M14.2 15.8l1.6-1.6"/></svg>`, slug: "mathematics", file: "/files/mathematics.pdf" },
        { name: "Physics", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#7C3AED " stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 21h2"/><path d="M12 17v4"/><path d="M14 4A22 22 0 0 0 3 15"/><path d="M17 14A22 22 0 0 0 6 3"/><circle cx="12" cy="12" r="3"/><path d="m14.2 14.2 4.3 4.3"/></svg>`, slug: "physics", file: "/files/physics.pdf" },
        { name: "Chemistry", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#16A34A" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 3h15"/><path d="M6 3v13a4 4 0 0 0 4 4h4a4 4 0 0 0 4-4V3"/><path d="M6 14h12"/></svg>`, slug: "chemistry", file: "/files/chemistry.pdf" },
        { name: "Biology", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#0D9488" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 10.5C7.8 13.8 13.2 13.8 16.5 10.5c.3-.3.3-.8 0-1.1-.3-.3-.8-.3-1.1 0-2.7 2.7-7.1 2.7-9.8 0-.3-.3-.8-.3-1.1 0-.3.3-.3.8 0 1.1z"/><path d="M19.5 13.5c-3.3-3.3-8.7-3.3-12 0-.3.3-.3.8 0 1.1.3.3.8.3 1.1 0 2.7-2.7 7.1-2.7 9.8 0 .3.3.8.3 1.1 0 .3-.3-.3-.8 0-1.1z"/><path d="m3.5 3.5 17 17"/></svg>`, slug: "biology", file: "/files/biology.pdf" },
        { name: "History", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#B45309" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/><path d="M14 3v5h5"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>`, slug: "history", file: "/files/history.pdf" },
        { name: "English Literature", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#DC2626" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`, slug: "englishliterature", file: "/files/english literature.pdf" },
        { name: "Khmer Literature", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#EA580C" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`, slug: "khmerliterature", file: "/files/khmer literature.pdf" },
      ],

      specialTests: [
        { name: "Physics Special", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#2563EB" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 21h2"/><path d="M12 17v4"/><path d="M14 4A22 22 0 0 0 3 15"/><path d="M17 14A22 22 0 0 0 6 3"/><circle cx="12" cy="12" r="3"/><path d="m14.2 14.2 4.3 4.3"/></svg>`, slug: "physicsspecial", file: "/files/physics_exam.pdf" },
        { name: "History Special", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#B45309" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/><path d="M14 3v5h5"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>`, slug: "historyspecial", file: "/files/combined.pdf" },
        { name: "Math Special", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#16A34A" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 15.3a2.82 2.82 0 0 1 0 4c-1 1-2.5 1-3.5 0L2.8 4.3c-1-1-1-2.5 0-3.5s2.5-1 3.5 0Z"/><path d="M5.6 7.2 7.2 5.6"/><path d="M9.9 11.5l1.6-1.6"/><path d="M14.2 15.8l1.6-1.6"/></svg>`, slug: "mathspecial", file: "/files/math_exam.pdf" },
        { name: "Chemistry Special", icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="#EA580C" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 3h15"/><path d="M6 3v13a4 4 0 0 0 4 4h4a4 4 0 0 0 4-4V3"/><path d="M6 14h12"/></svg>`, slug: "chemistryspecial", file: "/files/chemistry_exam.pdf" },
      ],

    };
  },

  methods: {
    toggleSubject(name) {
      this.expandedSubject = this.expandedSubject === name ? null : name;
    },
    openPDF(subject) {
      this.activePDF = subject.file;
      this.activePDFName = `${this.$t(`PastTests.subjects.${subject.slug}`)}`;
    },
    closePDF() {
      this.activePDF = null;
      this.activePDFName = "";
    },
  },
};
</script>

<style scoped>
.tests-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 700px;
  margin-left: 250px;
}

.tabs {
  display: flex;
  gap: 8px;
}

.tab {
  padding: 9px 18px;
  border-radius: 9px;
  border: 1.5px solid var(--gray-100);
  background: var(--white);
  font-size: 13px;
  font-weight: 600;
  color: var(--gray-500);
  display: flex;
  align-items: center;
  gap: 7px;
  transition: all 0.15s;
}

.tab:hover {
  border-color: var(--gray-300);
}

.tab--active {
  background: var(--navy);
  border-color: var(--navy);
  color: var(--white);
}
.tab-badge {
  background: var(--amber);
  color: var(--navy);
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 20px;
}

.tab--active .tab-badge {
  background: rgba(255, 255, 255, 0.2);
  color: var(--white);
}

.tests-list {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

@media (max-width: 640px) {
  .tests-list {
    grid-template-columns: 1fr;
  }

  .test-card {
    padding: 14px 16px;
  }

  .test-name {
    font-size: 13px;
  }

  .test-years {
    font-size: 10px;
  }
}

.test-card {
  background: var(--white);
  border: 1px solid var(--gray-100);
  border-radius: var(--radius);
  padding: 16px 22px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: border-color 0.15s;
}

.test-card:hover {
  border-color: var(--gray-300);
  cursor: pointer;
}

.test-icon {
  font-size: 26px;
  flex-shrink: 0;
}

.test-info {
  flex: 1;
}

.test-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--navy);
  margin-bottom: 2px;
}
.test-years {
  font-size: 11px;
  color: var(--gray-500);
}

.expand-btn {
  font-size: 12px;
  color: var(--gray-500);
  flex-shrink: 0;
}

.file-row {
  padding: 0 22px 18px;
  border-top: 1px solid var(--gray-100);
  padding-top: 14px;
}

.file-btn {
  background: var(--amber-light, #fef3c7);
  color: #b97d0a;
  font-size: 13px;
  font-weight: 600;
  padding: 10px 16px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  text-align: left;
  transition: background 0.15s;
}

.file-btn:hover {
  background: #fde9a8;
}

.no-file {
  font-size: 12px;
  color: var(--gray-500);
}

.pdf-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 24px;
}

.pdf-modal-content {
  background: var(--white);
  width: 100%;
  max-width: 900px;
  height: 90vh;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.pdf-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--gray-100);
  font-weight: 700;
  color: var(--navy);
  font-size: 14px;
}

.pdf-close-btn {
  background: none;
  font-size: 16px;
  color: var(--gray-500);
  padding: 4px 8px;
}

.pdf-close-btn:hover {
  color: var(--navy);
}

.pdf-frame {
  flex: 1;
  border: none;
  width: 100%;
}
</style>
