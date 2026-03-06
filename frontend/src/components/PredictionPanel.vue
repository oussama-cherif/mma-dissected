<template>
  <div class="card p-5">
    <h3 class="text-[10px] uppercase tracking-[0.15em] text-ufc-gold font-semibold mb-5">{{ $t('fight.prediction') }}</h3>

    <!-- Winner + Confidence -->
    <div class="flex items-center justify-between mb-5">
      <div>
        <p class="text-xl font-extrabold tracking-tight">{{ prediction.predicted_winner.name }}</p>
        <p class="text-gray-500 text-xs mt-0.5">{{ $t('fight.winner') }}</p>
      </div>
      <div class="text-center">
        <div
          :class="[
            'text-3xl font-extrabold tabular-nums',
            prediction.confidence > 70 ? 'text-green-400' :
            prediction.confidence > 50 ? 'text-yellow-400' :
            'text-gray-400'
          ]"
        >
          {{ prediction.confidence }}%
        </div>
        <p class="text-gray-600 text-[10px] uppercase tracking-wider">{{ $t('fight.confidence') }}</p>
      </div>
    </div>

    <!-- Confidence Bar -->
    <div class="mb-6">
      <div class="h-2 rounded-full bg-gray-800 overflow-hidden">
        <div
          :class="[
            'h-full rounded-full transition-all duration-700',
            prediction.confidence > 70 ? 'bg-gradient-to-r from-green-600 to-green-400' :
            prediction.confidence > 50 ? 'bg-gradient-to-r from-yellow-600 to-yellow-400' :
            'bg-gray-500'
          ]"
          :style="{ width: prediction.confidence + '%' }"
        ></div>
      </div>
    </div>

    <!-- Method Probabilities -->
    <div class="space-y-3 mb-5">
      <p class="text-[10px] text-gray-500 uppercase tracking-wider">{{ $t('fight.method') }}</p>
      <MethodBar :label="$t('stats.ko')" :value="prediction.prob_ko_tko" color="bg-red-500" />
      <MethodBar :label="$t('stats.sub')" :value="prediction.prob_submission" color="bg-blue-500" />
      <MethodBar :label="$t('stats.dec')" :value="totalDecision" color="bg-yellow-500" />
    </div>

    <!-- Round + Time -->
    <div v-if="prediction.predicted_round" class="flex gap-4 mb-5 text-sm">
      <div class="card px-3 py-2 flex-1 text-center">
        <p class="text-gray-500 text-[10px] uppercase">{{ $t('fight.round') }}</p>
        <p class="font-bold text-lg mt-0.5">{{ prediction.predicted_round }}</p>
      </div>
      <div v-if="prediction.predicted_time" class="card px-3 py-2 flex-1 text-center">
        <p class="text-gray-500 text-[10px] uppercase">{{ $t('fight.time') }}</p>
        <p class="font-bold text-lg mt-0.5">{{ prediction.predicted_time }}</p>
      </div>
    </div>

    <!-- Key Factors -->
    <div v-if="prediction.key_factors?.length" class="border-t border-gray-800/40 pt-4">
      <p class="text-[10px] text-gray-500 uppercase tracking-wider mb-3">{{ $t('fight.keyFactors') }}</p>
      <ul class="space-y-2">
        <li v-for="(factor, i) in prediction.key_factors" :key="i" class="flex items-start gap-2 text-sm text-gray-300">
          <span class="text-ufc-gold mt-0.5 shrink-0">&#8226;</span>
          {{ factor }}
        </li>
      </ul>
    </div>

    <p class="text-gray-700 text-[10px] mt-4 pt-3 border-t border-gray-800/30">
      {{ $t('fight.generatedAt') }}: {{ formatDate(prediction.created_at) }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import MethodBar from './MethodBar.vue'

const props = defineProps({
  prediction: { type: Object, required: true },
})

const totalDecision = computed(() =>
  props.prediction.prob_dec_unanimous + props.prediction.prob_dec_split + props.prediction.prob_dec_majority
)

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString()
}
</script>
