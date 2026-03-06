<template>
  <div v-if="fight" class="animate-fade-in">
    <!-- Back Link -->
    <router-link :to="`/event/${fight.event}`" class="inline-flex items-center gap-1 text-gray-500 hover:text-white text-sm transition-colors mb-5">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
      {{ $t('common.back') }}
    </router-link>

    <!-- Matchup Header -->
    <div class="card p-5 sm:p-6 mb-6">
      <div class="flex items-center justify-between">
        <div class="text-center flex-1">
          <p :class="['text-lg sm:text-xl font-extrabold', isWinnerA ? 'text-green-400' : 'text-white']">
            {{ fight.fighter_a.name }}
          </p>
          <p class="text-gray-500 text-xs mt-1">{{ fight.fighter_a.record }}</p>
        </div>
        <div class="px-4 sm:px-6 shrink-0">
          <div class="w-12 h-12 rounded-full bg-ufc-red/10 border border-ufc-red/20 flex items-center justify-center">
            <span class="text-ufc-red text-xs font-bold">{{ $t('fight.vs') }}</span>
          </div>
          <p class="text-gray-600 text-[10px] text-center mt-1.5">{{ fight.weight_class }}</p>
        </div>
        <div class="text-center flex-1">
          <p :class="['text-lg sm:text-xl font-extrabold', isWinnerB ? 'text-green-400' : 'text-white']">
            {{ fight.fighter_b.name }}
          </p>
          <p class="text-gray-500 text-xs mt-1">{{ fight.fighter_b.record }}</p>
        </div>
      </div>
    </div>

    <!-- Fighter Stats Side by Side -->
    <div class="grid md:grid-cols-2 gap-4 mb-6">
      <FighterStats :fighter="fight.fighter_a" />
      <FighterStats :fighter="fight.fighter_b" />
    </div>

    <!-- Prediction -->
    <PredictionPanel v-if="prediction" :prediction="prediction" class="mb-4" />

    <!-- Vulnerability Alert -->
    <div v-if="prediction?.vulnerability_note" class="card border-red-800/40 bg-red-950/20 p-5 mb-4">
      <div class="flex items-start gap-3">
        <div class="shrink-0 w-8 h-8 rounded-lg bg-red-900/40 flex items-center justify-center">
          <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-red-400 font-semibold text-sm mb-1">{{ $t('betting.vulnerability') }}</h3>
          <p class="text-gray-300 text-sm leading-relaxed">{{ prediction.vulnerability_note }}</p>
        </div>
      </div>
    </div>

    <!-- Betting Insight -->
    <div v-if="prediction?.betting_insight" class="card p-5">
      <div class="flex items-start gap-3">
        <div class="shrink-0 w-8 h-8 rounded-lg bg-ufc-gold/10 flex items-center justify-center">
          <svg class="w-4 h-4 text-ufc-gold" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
          </svg>
        </div>
        <div>
          <h3 class="text-ufc-gold font-semibold text-sm mb-1">{{ $t('betting.insight') }}</h3>
          <p class="text-gray-300 text-sm leading-relaxed">{{ prediction.betting_insight }}</p>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="flex items-center justify-center py-16">
    <div class="w-6 h-6 border-2 border-ufc-red/30 border-t-ufc-red rounded-full animate-spin"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEventsStore } from '../stores/events'
import { usePredictionsStore } from '../stores/predictions'
import FighterStats from '../components/FighterStats.vue'
import PredictionPanel from '../components/PredictionPanel.vue'

const props = defineProps({ id: [String, Number] })
const eventsStore = useEventsStore()
const predictionsStore = usePredictionsStore()
const fight = ref(null)
const prediction = ref(null)

const isWinnerA = computed(() =>
  prediction.value?.predicted_winner?.id === fight.value?.fighter_a?.id
)

const isWinnerB = computed(() =>
  prediction.value?.predicted_winner?.id === fight.value?.fighter_b?.id
)

onMounted(async () => {
  await eventsStore.fetchFight(props.id)
  fight.value = eventsStore.currentFight

  await predictionsStore.fetchPrediction(props.id)
  prediction.value = predictionsStore.currentPrediction
})
</script>
