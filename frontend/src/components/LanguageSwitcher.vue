<template>
  <div class="flex items-center bg-ufc-dark/80 rounded-lg border border-gray-800/40 p-0.5">
    <button
      v-for="lang in languages"
      :key="lang.code"
      @click="switchLanguage(lang.code)"
      :class="[
        'px-2 py-1 text-xs font-medium rounded-md transition-all',
        locale === lang.code
          ? 'bg-ufc-red text-white shadow-sm'
          : 'text-gray-500 hover:text-gray-300'
      ]"
    >
      {{ lang.label }}
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const languages = [
  { code: 'en', label: 'EN' },
  { code: 'fr', label: 'FR' },
  { code: 'ar', label: 'AR' },
]

function switchLanguage(code) {
  locale.value = code
  localStorage.setItem('locale', code)

  if (code === 'ar') {
    document.documentElement.dir = 'rtl'
    document.documentElement.lang = 'ar'
  } else {
    document.documentElement.dir = 'ltr'
    document.documentElement.lang = code
  }
}
</script>
