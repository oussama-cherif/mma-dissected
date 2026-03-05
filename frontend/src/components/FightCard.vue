<template>
  <router-link
    :to="`/fight/${fight.id}`"
    class="block bg-ufc-dark rounded-lg p-4 border border-gray-800 hover:border-ufc-red/40 transition-colors"
  >
    <div class="flex items-center">
      <div class="flex-1">
        <p :class="['font-semibold', isWinnerA ? 'text-green-400' : 'text-white']">
          {{ fight.fighter_a.name }}
          <span v-if="isWinnerA" class="text-[10px] ml-1">&#9668;</span>
        </p>
        <p class="text-gray-500 text-xs">{{ fight.fighter_a.record }}</p>
      </div>

      <div class="px-4 text-center shrink-0">
        <span class="text-gray-500 text-sm">{{ $t('fight.vs') }}</span>
        <p class="text-gray-600 text-xs mt-1">{{ fight.weight_class }}</p>
      </div>

      <div class="flex-1 text-right">
        <p :class="['font-semibold', isWinnerB ? 'text-green-400' : 'text-white']">
          <span v-if="isWinnerB" class="text-[10px] mr-1">&#9658;</span>
          {{ fight.fighter_b.name }}
        </p>
        <p class="text-gray-500 text-xs">{{ fight.fighter_b.record }}</p>
      </div>
    </div>

    <div v-if="fight.prediction" class="mt-3 pt-3 border-t border-gray-700/50">
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2">
          <span
            :class="[
              'text-xs font-bold px-2 py-0.5 rounded',
              fight.prediction.confidence > 70 ? 'bg-green-900/60 text-green-400' :
              fight.prediction.confidence > 50 ? 'bg-yellow-900/60 text-yellow-400' :
              'bg-gray-700 text-gray-400'
            ]"
          >
            {{ fight.prediction.confidence }}%
          </span>
          <span class="text-xs text-gray-400">
            {{ fight.prediction.predicted_winner.name }} {{ $t('fight.wins') }}
          </span>
        </div>
        <span class="text-[10px] text-gray-600">{{ topMethod }}</span>
      </div>

      <div class="flex gap-3 text-[10px]">
        <div class="flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-red-500 inline-block"></span>
          <span class="text-gray-500">{{ $t('stats.ko') }} {{ fight.prediction.prob_ko_tko }}%</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-blue-500 inline-block"></span>
          <span class="text-gray-500">{{ $t('stats.sub') }} {{ fight.prediction.prob_submission }}%</span>
        </div>
        <div class="flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-yellow-500 inline-block"></span>
          <span class="text-gray-500">{{ $t('stats.dec') }} {{ decisionPct }}%</span>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  fight: { type: Object, required: true },
})

const isWinnerA = computed(() =>
  props.fight.prediction?.predicted_winner?.id === props.fight.fighter_a.id
)

const isWinnerB = computed(() =>
  props.fight.prediction?.predicted_winner?.id === props.fight.fighter_b.id
)

const decisionPct = computed(() => {
  const p = props.fight.prediction
  if (!p) return 0
  return p.prob_dec_unanimous + p.prob_dec_split + p.prob_dec_majority
})

const topMethod = computed(() => {
  const p = props.fight.prediction
  if (!p) return ''
  const methods = [
    { label: t('stats.ko'), pct: p.prob_ko_tko },
    { label: t('stats.sub'), pct: p.prob_submission },
    { label: t('stats.dec'), pct: decisionPct.value },
  ]
  const top = methods.reduce((a, b) => a.pct > b.pct ? a : b)
  return `${top.label} ${top.pct}%`
})
</script>
