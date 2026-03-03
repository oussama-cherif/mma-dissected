<template>
  <div class="flex items-center gap-2">
    <span class="w-12 text-gray-500 text-xs">{{ label }}</span>
    <div class="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
      <div :class="[color, 'h-full rounded-full transition-all']" :style="{ width: value + '%' }" />
    </div>
    <span class="w-10 text-right text-xs text-gray-400">{{ value }}%</span>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: Number, required: true },
  color: { type: String, default: 'bg-ufc-red' },
})
</script>
