<template>
  <div class="bg-ufc-dark rounded-lg p-5 border border-gray-800">
    <h2 class="text-lg font-bold mb-1">{{ fighter.name }}</h2>
    <p v-if="fighter.nickname" class="text-ufc-gold text-sm mb-3">"{{ fighter.nickname }}"</p>
    <p class="text-gray-400 text-sm mb-4">{{ fighter.record }} &middot; {{ fighter.weight_class }}</p>

    <div class="space-y-2 text-sm">
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.wins') }}</span>
        <span class="text-green-400">{{ fighter.record_wins }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.losses') }}</span>
        <span class="text-red-400">{{ fighter.record_losses }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.draws') }}</span>
        <span>{{ fighter.record_draws }}</span>
      </div>

      <hr class="border-gray-700 my-3" />

      <p class="text-gray-400 text-xs uppercase tracking-wide mb-2">{{ $t('stats.winMethod') }}</p>
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.ko') }}</span>
        <span>{{ fighter.wins_ko_tko }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.sub') }}</span>
        <span>{{ fighter.wins_submission }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.dec') }}</span>
        <span>{{ fighter.wins_decision }}</span>
      </div>

      <hr class="border-gray-700 my-3" />

      <p class="text-red-400 text-xs uppercase tracking-wide mb-2">{{ $t('stats.vulnerabilities') }}</p>
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.ko') }} {{ $t('stats.losses') }}</span>
        <span class="text-red-400">{{ fighter.losses_ko_tko }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.sub') }} {{ $t('stats.losses') }}</span>
        <span class="text-red-400">{{ fighter.losses_submission }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-500">{{ $t('stats.dec') }} {{ $t('stats.losses') }}</span>
        <span class="text-red-400">{{ fighter.losses_decision }}</span>
      </div>

      <template v-if="fighter.sig_strikes_per_min">
        <hr class="border-gray-700 my-3" />
        <p class="text-gray-400 text-xs uppercase tracking-wide mb-2">{{ $t('stats.advanced') }}</p>
        <div class="flex justify-between">
          <span class="text-gray-500">{{ $t('stats.sigStrikes') }}</span>
          <span>{{ fighter.sig_strikes_per_min }}/min</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-500">{{ $t('stats.strikeAcc') }}</span>
          <span>{{ fighter.strike_accuracy }}%</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-500">{{ $t('stats.tdAvg') }}</span>
          <span>{{ fighter.takedown_avg }}/15min</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-500">{{ $t('stats.tdDef') }}</span>
          <span>{{ fighter.takedown_defense }}%</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
defineProps({
  fighter: { type: Object, required: true },
})
</script>
