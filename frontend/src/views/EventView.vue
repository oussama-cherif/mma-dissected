<template>
  <div v-if="event">
    <div class="mb-6">
      <router-link to="/events" class="text-gray-400 hover:text-white text-sm">&larr; {{ $t('nav.events') }}</router-link>
      <h1 class="text-2xl font-bold mt-2">{{ event.name }}</h1>
      <p class="text-gray-400">{{ formatDate(event.date) }} &middot; {{ event.location }}</p>
      <p v-if="event.last_synced" class="text-gray-600 text-xs mt-1">
        {{ $t('common.lastUpdated') }}: {{ timeAgo(event.last_synced) }}
      </p>
    </div>

    <div class="flex gap-2 mb-6 overflow-x-auto">
      <button
        v-for="section in sections"
        :key="section.key"
        @click="activeSection = section.key"
        :class="[
          'px-4 py-2 rounded-lg text-sm whitespace-nowrap transition-colors',
          activeSection === section.key
            ? 'bg-ufc-red text-white'
            : 'bg-ufc-dark text-gray-400 hover:text-white'
        ]"
      >
        {{ section.label }}
      </button>
    </div>

    <div class="space-y-3">
      <FightCard
        v-for="fight in filteredFights"
        :key="fight.id"
        :fight="fight"
      />
      <p v-if="filteredFights.length === 0" class="text-gray-500 text-center py-8">
        {{ $t('common.noFights') }}
      </p>
    </div>
  </div>
  <div v-else class="text-gray-400">{{ $t('common.loading') }}</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useEventsStore } from '../stores/events'
import FightCard from '../components/FightCard.vue'

const props = defineProps({ id: [String, Number] })
const { t } = useI18n()
const store = useEventsStore()
const event = ref(null)
const activeSection = ref('main')

const sections = [
  { key: 'main', label: t('fight.mainCard') },
  { key: 'prelim', label: t('fight.prelims') },
  { key: 'early', label: t('fight.earlyPrelims') },
]

const filteredFights = computed(() => {
  if (!event.value?.fights) return []
  return event.value.fights.filter(f => f.card_section === activeSection.value)
})

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime()
  const hours = Math.floor(diff / 3600000)
  if (hours < 1) return t('common.justNow')
  if (hours < 24) return `${hours}h ago`
  return `${Math.floor(hours / 24)}d ago`
}

onMounted(async () => {
  await store.fetchEvent(props.id)
  event.value = store.currentEvent
})
</script>
