<template>
  <main
    class="relative flex items-center justify-center min-h-screen overflow-hidden bg-blue-950 px-6"
  >
    <section
      class="relative z-10 flex flex-col items-center text-center w-full max-w-2xl rounded-3xl bg-white/10 backdrop-blur-lg border border-white/20 shadow-2xl p-12 pb-16"
    >
      <h1
        class="text-8xl md:text-9xl font-extrabold text-white tracking-wider"
      >
        {{ $t('notFound.number') }}
      </h1>

      <h2 class="mt-4 text-3xl font-bold text-white">
        {{ $t('notFound.title') }}
      </h2>

      <p class="mt-4 max-w-md text-blue-100 leading-relaxed">
        {{ $t('notFound.body') }}
      </p>

      <router-link
        to="/"
        style="margin-top: 10px; margin-bottom: 10px;"
        class="inline-flex items-center justify-center gap-2 mt-10 mb-4 px-8 py-4 rounded-lg bg-white text-blue-900 font-semibold text-lg transition-all duration-300 hover:bg-blue-600 hover:text-white shadow-lg"
      >
        <span aria-hidden="true">←</span>
        <span>{{ $t('notFound.backHome') }}</span>
      </router-link>
    </section>
  </main>
</template>