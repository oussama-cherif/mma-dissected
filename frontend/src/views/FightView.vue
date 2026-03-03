<template>
  <div v-if="fight">
    <router-link :to="`/event/${fight.event}`" class="text-gray-400 hover:text-white text-sm">
      &larr; {{ $t('common.back') }}
    </router-link>

    <div class="mt-4 grid md:grid-cols-2 gap-6">
      <FighterStats :fighter="fight.fighter_a" />
      <FighterStats :fighter="fight.fighter_b" />
    </div>

    <PredictionPanel v-if="prediction" :prediction="prediction" class="mt-6" />

    <div v-if="prediction?.vulnerability_note" class="mt-4 bg-red-900/30 border border-red-700 rounded-lg p-4">
      <h3 class="text-red-400 font-semibold text-sm uppercase mb-2">{{ $t('betting.vulnerability') }}</h3>
      <p class="text-gray-300 text-sm">{{ prediction.vulnerability_note }}</p>
    </div>

    <div v-if="prediction?.betting_insight" class="mt-4 bg-ufc-dark rounded-lg p-4 border border-gray-800">
      <h3 class="text-ufc-gold font-semibold text-sm uppercase mb-2">{{ $t('betting.insight') }}</h3>
      <p class="text-gray-300 text-sm">{{ prediction.betting_insight }}</p>
    </div>
  </div>
  <div v-else class="text-gray-400">{{ $t('common.loading') }}</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEventsStore } from '../stores/events'
import { usePredictionsStore } from '../stores/predictions'
import FighterStats from '../components/FighterStats.vue'
import PredictionPanel from '../components/PredictionPanel.vue'

const props = defineProps({ id: [String, Number] })
const eventsStore = useEventsStore()
const predictionsStore = usePredictionsStore()
const fight = ref(null)
const prediction = ref(null)

onMounted(async () => {
  await eventsStore.fetchFight(props.id)
  fight.value = eventsStore.currentFight

  await predictionsStore.fetchPrediction(props.id)
  prediction.value = predictionsStore.currentPrediction
})
</script>
