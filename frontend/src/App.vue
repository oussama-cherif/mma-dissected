<template>
  <div class="min-h-screen bg-ufc-darker text-white">
    <nav class="bg-ufc-dark/95 backdrop-blur-sm border-b border-gray-800/50 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-14">
          <router-link to="/" class="flex items-center gap-2 group">
            <span class="text-ufc-red text-2xl font-extrabold tracking-tight group-hover:text-ufc-red-light transition-colors">MMA</span>
            <span class="text-gray-400 text-sm font-medium hidden sm:inline">Dissected</span>
          </router-link>

          <div class="hidden sm:flex items-center gap-1">
            <router-link
              v-for="link in navLinks"
              :key="link.to"
              :to="link.to"
              :class="[
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                $route.path === link.to || (link.to !== '/' && $route.path.startsWith(link.to))
                  ? 'bg-ufc-red/15 text-ufc-red'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              ]"
            >
              {{ $t(link.label) }}
            </router-link>
          </div>

          <div class="flex items-center gap-3">
            <LanguageSwitcher />
            <button
              @click="mobileOpen = !mobileOpen"
              class="sm:hidden p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/5"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div v-if="mobileOpen" class="sm:hidden border-t border-gray-800/50 px-4 py-2 space-y-1">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          @click="mobileOpen = false"
          :class="[
            'block px-3 py-2 rounded-lg text-sm font-medium transition-colors',
            $route.path === link.to
              ? 'bg-ufc-red/15 text-ufc-red'
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          ]"
        >
          {{ $t(link.label) }}
        </router-link>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="border-t border-gray-800/30 mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 py-6 text-center">
        <p class="text-gray-600 text-xs">MMA Dissected &middot; Stats-based fight predictions</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

const mobileOpen = ref(false)

const navLinks = [
  { to: '/', label: 'nav.home' },
  { to: '/events', label: 'nav.events' },
]
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
