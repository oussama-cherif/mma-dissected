<template>
  <div class="min-h-screen bg-ufc-darker">
    <nav class="bg-ufc-dark border-b border-gray-800 px-4 py-3">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <router-link to="/" class="text-xl font-bold text-ufc-red">
          MMA Dissected
        </router-link>
        <div class="flex items-center gap-4">
          <router-link to="/" class="text-gray-300 hover:text-white text-sm">
            {{ $t('nav.home') }}
          </router-link>
          <router-link to="/events" class="text-gray-300 hover:text-white text-sm">
            {{ $t('nav.events') }}
          </router-link>
          <LanguageSwitcher />
        </div>
      </div>
    </nav>
    <main class="max-w-7xl mx-auto px-4 py-6">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import LanguageSwitcher from './components/LanguageSwitcher.vue'
</script>
