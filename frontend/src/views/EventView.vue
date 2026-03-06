<template>
  <div v-if="event" class="animate-fade-in">
    <!-- Event Header -->
    <div class="mb-6">
      <router-link to="/events" class="inline-flex items-center gap-1 text-gray-500 hover:text-white text-sm transition-colors mb-3">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        {{ $t('nav.events') }}
      </router-link>

      <div class="card p-5 sm:p-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h1 class="text-xl sm:text-2xl font-extrabold tracking-tight">{{ event.name }}</h1>
            <p class="text-gray-400 text-sm mt-1">{{ formatDate(event.date) }} &middot; {{ event.location }}</p>
          </div>
          <div class="flex items-center gap-3">
            <span
              :class="[
                'badge',
                event.status === 'upcoming' ? 'badge-upcoming' :
                event.status === 'live' ? 'badge-live' :
                'badge-completed'
              ]"
            >
              {{ event.status }}
            </span>
            <span v-if="event.last_synced" class="text-gray-600 text-xs">
              {{ $t('common.lastUpdated') }}: {{ timeAgo(event.last_synced) }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Section Tabs -->
    <div class="flex gap-1.5 mb-5 overflow-x-auto pb-1 scrollbar-none">
      <button
        v-for="section in sections"
        :key="section.key"
        @click="activeSection = section.key"
        :class="[
          'px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all',
          activeSection === section.key
            ? 'bg-ufc-red text-white shadow-lg shadow-ufc-red/20'
            : 'bg-ufc-dark text-gray-400 hover:text-white hover:bg-ufc-surface border border-gray-800/40'
        ]"
      >
        {{ section.label }}
        <span
          v-if="sectionCounts[section.key]"
          :class="[
            'ml-1.5 text-[10px] px-1.5 py-0.5 rounded-full',
            activeSection === section.key ? 'bg-white/20' : 'bg-gray-700'
          ]"
        >
          {{ sectionCounts[section.key] }}
        </span>
      </button>
    </div>

    <!-- Fight List -->
    <div class="space-y-3">
      <FightCard
        v-for="fight in filteredFights"
        :key="fight.id"
        :fight="fight"
        class="animate-slide-up"
      />
      <div v-if="filteredFights.length === 0" class="text-center py-12">
        <p class="text-gray-500">{{ $t('common.noFights') }}</p>
      </div>
    </div>
  </div>

  <div v-else class="flex items-center justify-center py-16">
    <div class="w-6 h-6 border-2 border-ufc-red/30 border-t-ufc-red rounded-full animate-spin"></div>
  </div>
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

const sectionCounts = computed(() => {
  if (!event.value?.fights) return {}
  const counts = {}
  for (const s of sections) {
    counts[s.key] = event.value.fights.filter(f => f.card_section === s.key).length
  }
  return counts
})

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
