<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">{{ $t('nav.events') }}</h1>
    <div v-if="loading" class="text-gray-400">{{ $t('common.loading') }}</div>
    <div v-else class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="event in events"
        :key="event.id"
        :to="`/event/${event.id}`"
        class="bg-ufc-dark rounded-lg p-5 border border-gray-800 hover:border-ufc-red/50 transition-colors"
      >
        <h3 class="font-semibold mb-1">{{ event.name }}</h3>
        <p class="text-gray-400 text-sm">{{ formatDate(event.date) }}</p>
        <p class="text-gray-500 text-sm">{{ event.location }}</p>
        <div class="flex items-center justify-between mt-3">
          <span class="text-xs text-gray-500">{{ event.fight_count }} {{ $t('home.fights') }}</span>
          <span
            :class="[
              'text-xs px-2 py-1 rounded',
              event.status === 'upcoming' ? 'bg-green-900 text-green-300' :
              event.status === 'live' ? 'bg-red-900 text-red-300' :
              'bg-gray-700 text-gray-400'
            ]"
          >
            {{ event.status }}
          </span>
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
