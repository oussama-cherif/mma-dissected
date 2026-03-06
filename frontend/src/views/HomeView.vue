<template>
  <div class="animate-fade-in">
    <!-- Hero: Next Event -->
    <section v-if="nextEvent" class="mb-10">
      <div class="relative overflow-hidden rounded-2xl border border-ufc-red/20 bg-gradient-to-br from-ufc-red/10 via-ufc-dark to-ufc-darker p-6 sm:p-8">
        <div class="absolute top-0 right-0 w-64 h-64 bg-ufc-red/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>

        <p class="text-ufc-gold text-xs font-semibold uppercase tracking-[0.2em] mb-3">{{ $t('home.nextEvent') }}</p>
        <h1 class="text-2xl sm:text-4xl font-extrabold tracking-tight mb-2">{{ nextEvent.name }}</h1>
        <p class="text-gray-400 text-sm mb-5">{{ formatDate(nextEvent.date) }} &middot; {{ nextEvent.location }}</p>

        <!-- Countdown -->
        <div v-if="countdown" class="flex gap-4 mb-6">
          <div v-for="unit in countdownUnits" :key="unit.label" class="text-center">
            <div class="bg-ufc-dark/80 border border-gray-700/50 rounded-lg px-3 py-2 min-w-[56px]">
              <span class="text-xl sm:text-2xl font-bold tabular-nums">{{ unit.value }}</span>
            </div>
            <span class="text-gray-500 text-[10px] uppercase tracking-wider mt-1 block">{{ unit.label }}</span>
          </div>
        </div>

        <!-- Main event preview -->
        <div v-if="mainEventFight" class="bg-ufc-darker/60 rounded-xl p-4 border border-gray-800/40 mb-5">
          <p class="text-gray-500 text-[10px] uppercase tracking-wider mb-2">{{ $t('fight.mainCard') }}</p>
          <div class="flex items-center justify-between">
            <div class="text-center flex-1">
              <p class="font-bold text-sm sm:text-base">{{ mainEventFight.fighter_a.name }}</p>
              <p class="text-gray-500 text-xs">{{ mainEventFight.fighter_a.record }}</p>
            </div>
            <span class="text-ufc-red font-bold text-xs px-3">{{ $t('fight.vs') }}</span>
            <div class="text-center flex-1">
              <p class="font-bold text-sm sm:text-base">{{ mainEventFight.fighter_b.name }}</p>
              <p class="text-gray-500 text-xs">{{ mainEventFight.fighter_b.record }}</p>
            </div>
          </div>
        </div>

        <router-link :to="`/event/${nextEvent.id}`" class="btn-primary inline-block">
          {{ $t('home.viewCard') }}
        </router-link>
      </div>
    </section>

    <!-- All Events -->
    <section>
      <h2 class="section-title mb-4">{{ $t('home.allEvents') }}</h2>
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="w-6 h-6 border-2 border-ufc-red/30 border-t-ufc-red rounded-full animate-spin"></div>
      </div>
      <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <router-link
          v-for="event in events"
          :key="event.id"
          :to="`/event/${event.id}`"
          class="card card-hover p-5 group animate-slide-up"
        >
          <div class="flex items-start justify-between mb-3">
            <h3 class="font-semibold text-sm group-hover:text-ufc-red-light transition-colors">{{ event.name }}</h3>
            <span
              :class="[
                'badge shrink-0 ml-2',
                event.status === 'upcoming' ? 'badge-upcoming' :
                event.status === 'live' ? 'badge-live' :
                'badge-completed'
              ]"
            >
              {{ event.status }}
            </span>
          </div>
          <p class="text-gray-400 text-sm">{{ formatDate(event.date) }}</p>
          <p class="text-gray-600 text-xs mt-0.5">{{ event.location }}</p>
          <div class="flex items-center gap-2 mt-3 pt-3 border-t border-gray-800/40">
            <span class="text-[10px] text-gray-500 uppercase tracking-wider">{{ event.fight_count || '—' }} {{ $t('home.fights') }}</span>
          </div>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useEventsStore } from '../stores/events'

const { t } = useI18n()
const store = useEventsStore()
const events = ref([])
const nextEvent = ref(null)
const loading = ref(true)
const countdown = ref(null)
let timer = null

const mainEventFight = computed(() => {
  if (!nextEvent.value?.fights) return null
  return nextEvent.value.fights.find(f => f.card_section === 'main' && f.order === 1) ||
         nextEvent.value.fights.find(f => f.card_section === 'main') ||
         nextEvent.value.fights[0] || null
})

const countdownUnits = computed(() => {
  if (!countdown.value) return []
  return [
    { value: countdown.value.days, label: t('common.days') || 'Days' },
    { value: countdown.value.hours, label: t('common.hours') || 'Hrs' },
    { value: countdown.value.mins, label: t('common.mins') || 'Min' },
    { value: countdown.value.secs, label: t('common.secs') || 'Sec' },
  ]
})

function updateCountdown() {
  if (!nextEvent.value) return
  const diff = new Date(nextEvent.value.date).getTime() - Date.now()
  if (diff <= 0) { countdown.value = null; return }
  countdown.value = {
    days: String(Math.floor(diff / 86400000)).padStart(2, '0'),
    hours: String(Math.floor((diff % 86400000) / 3600000)).padStart(2, '0'),
    mins: String(Math.floor((diff % 3600000) / 60000)).padStart(2, '0'),
    secs: String(Math.floor((diff % 60000) / 1000)).padStart(2, '0'),
  }
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

onMounted(async () => {
  await store.fetchEvents()
  events.value = store.events
  nextEvent.value = store.nextEvent

  if (nextEvent.value) {
    await store.fetchEvent(nextEvent.value.id)
    nextEvent.value = store.currentEvent
    updateCountdown()
    timer = setInterval(updateCountdown, 1000)
  }
  loading.value = false
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>
