<template>
  <div class="bg-ufc-dark rounded-lg p-5 border border-gray-800">
    <h3 class="text-sm uppercase tracking-wide text-ufc-gold mb-4">{{ $t('fight.prediction') }}</h3>

    <div class="flex items-center justify-between mb-4">
      <div>
        <p class="text-lg font-bold">{{ prediction.predicted_winner.name }}</p>
        <p class="text-gray-500 text-xs">{{ $t('fight.winner') }}</p>
      </div>
      <div
        :class="[
          'text-2xl font-bold px-4 py-2 rounded-lg',
          prediction.confidence > 70 ? 'bg-green-900/50 text-green-400' :
          prediction.confidence > 50 ? 'bg-yellow-900/50 text-yellow-400' :
          'bg-gray-700 text-gray-400'
        ]"
      >
        {{ prediction.confidence }}%
      </div>
    </div>

    <div class="space-y-2 text-sm">
      <p class="text-gray-400 text-xs uppercase mb-2">{{ $t('fight.method') }}</p>
      <MethodBar :label="$t('stats.ko')" :value="prediction.prob_ko_tko" color="bg-red-500" />
      <MethodBar :label="$t('stats.sub')" :value="prediction.prob_submission" color="bg-blue-500" />
      <MethodBar :label="$t('stats.dec')" :value="prediction.prob_dec_unanimous + prediction.prob_dec_split + prediction.prob_dec_majority" color="bg-yellow-500" />
    </div>

    <div v-if="prediction.predicted_round" class="mt-4 flex gap-4 text-sm text-gray-400">
      <span>{{ $t('fight.round') }}: {{ prediction.predicted_round }}</span>
      <span v-if="prediction.predicted_time">{{ $t('fight.time') }}: {{ prediction.predicted_time }}</span>
    </div>

    <div v-if="prediction.key_factors?.length" class="mt-4">
      <p class="text-gray-400 text-xs uppercase mb-2">{{ $t('fight.keyFactors') }}</p>
      <ul class="space-y-1">
        <li v-for="(factor, i) in prediction.key_factors" :key="i" class="text-gray-300 text-sm">
          &bull; {{ factor }}
        </li>
      </ul>
    </div>

    <p class="text-gray-600 text-xs mt-4">
      {{ $t('fight.generatedAt') }}: {{ formatDate(prediction.created_at) }}
    </p>
  </div>
</template>

<script setup>
import MethodBar from './MethodBar.vue'

defineProps({
  prediction: { type: Object, required: true },
})

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString()
}
</script>
