import { defineStore } from 'pinia'
import api from '../api'

export const useEventsStore = defineStore('events', {
  state: () => ({
    events: [],
    nextEvent: null,
    currentEvent: null,
    currentFight: null,
  }),

  actions: {
    async fetchEvents() {
      const { data } = await api.get('/events/')
      this.events = data.results || data
      this.nextEvent = this.events.find(e => e.status === 'upcoming') || null
    },

    async fetchEvent(id) {
      const { data } = await api.get(`/events/${id}/`)
      this.currentEvent = data
    },

    async fetchFight(id) {
      const { data } = await api.get(`/fights/${id}/`)
      this.currentFight = data
    },
  },
})
