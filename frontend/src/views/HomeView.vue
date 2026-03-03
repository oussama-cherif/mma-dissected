<template>
  <div>
    <section v-if="nextEvent" class="mb-10">
      <div class="bg-gradient-to-r from-ufc-red/20 to-ufc-dark rounded-xl p-8 border border-ufc-red/30">
        <p class="text-ufc-gold text-sm uppercase tracking-widest mb-2">{{ $t('home.nextEvent') }}</p>
        <h1 class="text-3xl font-bold mb-2">{{ nextEvent.name }}</h1>
        <p class="text-gray-400 mb-4">{{ formatDate(nextEvent.date) }} &middot; {{ nextEvent.location }}</p>
        <router-link
          :to="`/event/${nextEvent.id}`"
          class="inline-block bg-ufc-red hover:bg-red-700 text-white px-6 py-2 rounded-lg transition-colors"
        >
          {{ $t('home.viewCard') }}
        </router-link>
      </div>
    </section>

    <section>
      <h2 class="text-xl font-semibold mb-4">{{ $t('home.allEvents') }}</h2>
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
          <span
            :class="[
              'inline-block mt-3 text-xs px-2 py-1 rounded',
              event.status === 'upcoming' ? 'bg-green-900 text-green-300' :
              event.status === 'live' ? 'bg-red-900 text-red-300' :
              'bg-gray-700 text-gray-400'
            ]"
          >
            {{ event.status }}
          </span>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEventsStore } from '../stores/events'

const store = useEventsStore()
const events = ref([])
const nextEvent = ref(null)
const loading = ref(true)

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

onMounted(async () => {
  await store.fetchEvents()
  events.value = store.events
  nextEvent.value = store.nextEvent
  loading.value = false
})
</script>
