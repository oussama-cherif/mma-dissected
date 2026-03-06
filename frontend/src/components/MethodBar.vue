<template>
  <div class="flex items-center gap-2">
    <span class="w-16 text-gray-500 text-xs truncate">{{ label }}</span>
    <div class="flex-1 bg-gray-800 rounded-full h-2 overflow-hidden">
      <div
        :class="[color, 'h-full rounded-full transition-all duration-500']"
        :style="{ width: value + '%' }"
      />
    </div>
    <span class="w-10 text-right text-xs font-medium text-gray-400 tabular-nums">{{ value }}%</span>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: Number, required: true },
  color: { type: String, default: 'bg-ufc-red' },
})
</script>
