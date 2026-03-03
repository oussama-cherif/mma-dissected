import { defineStore } from 'pinia'
import api from '../api'

export const usePredictionsStore = defineStore('predictions', {
  state: () => ({
    currentPrediction: null,
  }),

  actions: {
    async fetchPrediction(fightId) {
      try {
        const { data } = await api.get(`/predictions/fights/${fightId}/prediction/`)
        this.currentPrediction = data
      } catch {
        this.currentPrediction = null
      }
    },

    async generatePrediction(fightId, lang = 'en') {
      const { data } = await api.post(`/predictions/fights/${fightId}/predict/?lang=${lang}`)
      this.currentPrediction = data
      return data
    },
  },
})
