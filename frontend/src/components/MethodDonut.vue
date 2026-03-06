<template>
  <div class="flex flex-col items-center">
    <div class="relative" :style="{ width: size + 'px', height: size + 'px' }">
      <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`">
        <circle
          :cx="center" :cy="center" :r="radius"
          fill="none" :stroke-width="strokeWidth"
          class="stroke-gray-800"
        />
        <circle
          v-for="(seg, i) in segments"
          :key="i"
          :cx="center" :cy="center" :r="radius"
          fill="none" :stroke-width="strokeWidth"
          :stroke="seg.color"
          :stroke-dasharray="seg.dashArray"
          :stroke-dashoffset="seg.dashOffset"
          stroke-linecap="round"
          class="transition-all duration-500"
          :style="{ transform: 'rotate(-90deg)', transformOrigin: 'center' }"
        />
      </svg>
      <div class="absolute inset-0 flex items-center justify-center">
        <span class="text-xs font-bold text-gray-300">{{ total }}</span>
      </div>
    </div>
    <div class="mt-3 space-y-1 w-full">
      <div v-for="item in items" :key="item.label" class="flex items-center justify-between text-xs">
        <div class="flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full" :style="{ background: item.color }"></span>
          <span class="text-gray-400">{{ item.label }}</span>
        </div>
        <span class="font-medium text-gray-300">{{ item.value }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: { type: Array, required: true },
  size: { type: Number, default: 100 },
  strokeWidth: { type: Number, default: 8 },
})

const center = computed(() => props.size / 2)
const radius = computed(() => (props.size - props.strokeWidth) / 2)
const circumference = computed(() => 2 * Math.PI * radius.value)
const total = computed(() => props.items.reduce((sum, item) => sum + item.value, 0))

const segments = computed(() => {
  if (total.value === 0) return []
  let offset = 0
  return props.items.map(item => {
    const pct = item.value / total.value
    const seg = {
      color: item.color,
      dashArray: `${pct * circumference.value} ${circumference.value}`,
      dashOffset: -offset * circumference.value,
    }
    offset += pct
    return seg
  })
})
</script>
