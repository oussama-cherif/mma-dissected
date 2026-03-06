<template>
  <div class="animate-fade-in">
    <h1 class="text-2xl font-extrabold tracking-tight mb-6">{{ $t('nav.events') }}</h1>

    <div v-if="loading" class="flex items-center justify-center py-16">
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
        <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-800/40">
          <span class="text-[10px] text-gray-500 uppercase tracking-wider">{{ event.fight_count || '—' }} {{ $t('home.fights') }}</span>
          <svg class="w-4 h-4 text-gray-600 group-hover:text-ufc-red transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEventsStore } from '../stores/events'

const store = useEventsStore()
const events = ref([])
const loading = ref(true)

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

onMounted(async () => {
  await store.fetchEvents()
  events.value = store.events
  loading.value = false
})
</script>
