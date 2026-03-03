<template>
  <div class="flex items-center gap-1">
    <button
      v-for="lang in languages"
      :key="lang.code"
      @click="switchLanguage(lang.code)"
      :class="[
        'px-2 py-1 text-xs rounded transition-colors',
        locale === lang.code
          ? 'bg-ufc-red text-white'
          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
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
