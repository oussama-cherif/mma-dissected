import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import en from './locales/en.json'
import fr from './locales/fr.json'
import ar from './locales/ar.json'
import './style.css'

const savedLocale = localStorage.getItem('locale') || 'en'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: { en, fr, ar },
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')

// Handle RTL for Arabic
if (savedLocale === 'ar') {
  document.documentElement.dir = 'rtl'
  document.documentElement.lang = 'ar'
}
