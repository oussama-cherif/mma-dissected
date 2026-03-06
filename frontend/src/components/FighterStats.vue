<template>
  <div class="card p-5">
    <!-- Name + Record -->
    <div class="mb-4">
      <h2 class="text-lg font-bold">{{ fighter.name }}</h2>
      <p v-if="fighter.nickname" class="text-ufc-gold text-sm">"{{ fighter.nickname }}"</p>
      <div class="flex items-center gap-3 mt-2">
        <span class="text-sm text-gray-300 font-medium">
          {{ fighter.record_wins }}-{{ fighter.record_losses }}-{{ fighter.record_draws }}
        </span>
        <span class="text-xs text-gray-600">&middot;</span>
        <span class="text-xs text-gray-500">{{ fighter.weight_class }}</span>
      </div>
    </div>

    <!-- Win/Loss Donuts -->
    <div class="grid grid-cols-2 gap-4 mb-5">
      <div>
        <p class="text-[10px] text-gray-500 uppercase tracking-wider text-center mb-2">{{ $t('stats.winMethod') }}</p>
        <MethodDonut :items="winMethods" :size="90" :stroke-width="7" />
      </div>
      <div>
        <p class="text-[10px] text-red-400/70 uppercase tracking-wider text-center mb-2">{{ $t('stats.lossMethod') }}</p>
        <MethodDonut :items="lossMethods" :size="90" :stroke-width="7" />
      </div>
    </div>

    <!-- Advanced Stats -->
    <template v-if="fighter.sig_strikes_per_min">
      <div class="border-t border-gray-800/40 pt-4">
        <p class="text-[10px] text-gray-500 uppercase tracking-wider mb-3">{{ $t('stats.advanced') }}</p>
        <div class="space-y-2.5">
          <StatRow :label="$t('stats.sigStrikes')" :value="fighter.sig_strikes_per_min" suffix="/min" />
          <StatRow :label="$t('stats.strikeAcc')" :value="fighter.strike_accuracy" suffix="%" :bar="true" />
          <StatRow :label="$t('stats.tdAvg')" :value="fighter.takedown_avg" suffix="/15min" />
          <StatRow :label="$t('stats.tdDef')" :value="fighter.takedown_defense" suffix="%" :bar="true" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import MethodDonut from './MethodDonut.vue'
import StatRow from './StatRow.vue'

const { t } = useI18n()

const props = defineProps({
  fighter: { type: Object, required: true },
})

const winMethods = computed(() => [
  { label: t('stats.ko'), value: props.fighter.wins_ko_tko || 0, color: '#EF4444' },
  { label: t('stats.sub'), value: props.fighter.wins_submission || 0, color: '#3B82F6' },
  { label: t('stats.dec'), value: props.fighter.wins_decision || 0, color: '#EAB308' },
])

const lossMethods = computed(() => [
  { label: t('stats.ko'), value: props.fighter.losses_ko_tko || 0, color: '#EF4444' },
  { label: t('stats.sub'), value: props.fighter.losses_submission || 0, color: '#3B82F6' },
  { label: t('stats.dec'), value: props.fighter.losses_decision || 0, color: '#EAB308' },
])
</script>
