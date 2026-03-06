<template>
  <div>
    <div class="flex items-center justify-between text-sm">
      <span class="text-gray-500 text-xs">{{ label }}</span>
      <span class="text-gray-300 font-medium text-xs">{{ value }}{{ suffix }}</span>
    </div>
    <div v-if="bar" class="mt-1 h-1 rounded-full bg-gray-800 overflow-hidden">
      <div class="h-full rounded-full bg-ufc-gold/70 transition-all duration-500" :style="{ width: Math.min(value, 100) + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: [Number, String], required: true },
  suffix: { type: String, default: '' },
  bar: { type: Boolean, default: false },
})
</script>
