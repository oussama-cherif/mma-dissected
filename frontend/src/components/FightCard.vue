<template>
  <router-link
    :to="`/fight/${fight.id}`"
    class="block card card-hover p-4 sm:p-5 group"
  >
    <!-- Fighters Row -->
    <div class="flex items-center">
      <div class="flex-1 min-w-0">
        <p :class="['font-bold text-sm sm:text-base truncate', isWinnerA ? 'text-green-400' : 'text-white']">
          {{ fight.fighter_a.name }}
          <span v-if="isWinnerA" class="text-green-500 text-xs ml-1">&#9664;</span>
        </p>
        <p class="text-gray-500 text-xs mt-0.5">{{ fight.fighter_a.record }}</p>
      </div>

      <div class="px-3 sm:px-5 text-center shrink-0">
        <div class="w-9 h-9 rounded-full bg-ufc-red/10 border border-ufc-red/20 flex items-center justify-center">
          <span class="text-ufc-red text-[10px] font-bold">{{ $t('fight.vs') }}</span>
        </div>
        <p class="text-gray-600 text-[10px] mt-1.5">{{ fight.weight_class }}</p>
      </div>

      <div class="flex-1 min-w-0 text-right">
        <p :class="['font-bold text-sm sm:text-base truncate', isWinnerB ? 'text-green-400' : 'text-white']">
          <span v-if="isWinnerB" class="text-green-500 text-xs mr-1">&#9654;</span>
          {{ fight.fighter_b.name }}
        </p>
        <p class="text-gray-500 text-xs mt-0.5">{{ fight.fighter_b.record }}</p>
      </div>
    </div>

    <!-- Prediction: gradient bar + centered info -->
    <div v-if="fight.prediction" class="mt-3 pt-3 border-t border-gray-800/40">
      <!-- Green-to-red gradient bar -->
      <div
        class="relative h-8 rounded-lg overflow-hidden"
        :style="{
          background: isWinnerA
            ? 'linear-gradient(to right, rgba(34,197,94,0.25), rgba(34,197,94,0.05) 50%, rgba(239,68,68,0.05) 50%, rgba(239,68,68,0.25))'
            : 'linear-gradient(to right, rgba(239,68,68,0.25), rgba(239,68,68,0.05) 50%, rgba(34,197,94,0.05) 50%, rgba(34,197,94,0.25))'
        }"
      >
        <div class="absolute inset-0 flex items-center justify-center">
          <span
            :class="[
              'text-lg font-extrabold tabular-nums',
              fight.prediction.confidence > 70 ? 'text-green-400' :
              fight.prediction.confidence > 50 ? 'text-yellow-400' :
              'text-gray-400'
            ]"
          >
            {{ fight.prediction.confidence }}%
          </span>
        </div>
      </div>

      <!-- Winner centered below -->
      <p class="text-center mt-2 text-sm font-bold text-green-400">
        {{ fight.prediction.predicted_winner.name }} {{ $t('fight.wins') }}
      </p>

      <!-- Vulnerability badge -->
      <div v-if="fight.prediction.vulnerability_note" class="flex items-center justify-center gap-1.5 mt-2">
        <svg class="w-3.5 h-3.5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
        </svg>
        <span class="text-red-400 text-xs font-medium">{{ $t('betting.vulnerability') }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  fight: { type: Object, required: true },
})

const isWinnerA = computed(() =>
  props.fight.prediction?.predicted_winner?.id === props.fight.fighter_a.id
)

const isWinnerB = computed(() =>
  props.fight.prediction?.predicted_winner?.id === props.fight.fighter_b.id
)

</script>
