<template>
  <router-link
    :to="`/fight/${fight.id}`"
    class="block bg-ufc-dark rounded-lg p-4 border border-gray-800 hover:border-ufc-red/40 transition-colors"
  >
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <p class="font-semibold">{{ fight.fighter_a.name }}</p>
        <p class="text-gray-500 text-xs">{{ fight.fighter_a.record }}</p>
      </div>

      <div class="px-4 text-center">
        <span class="text-gray-500 text-sm">{{ $t('fight.vs') }}</span>
        <p class="text-gray-600 text-xs mt-1">{{ fight.weight_class }}</p>
      </div>

      <div class="flex-1 text-right">
        <p class="font-semibold">{{ fight.fighter_b.name }}</p>
        <p class="text-gray-500 text-xs">{{ fight.fighter_b.record }}</p>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  fight: { type: Object, required: true },
})
</script>
