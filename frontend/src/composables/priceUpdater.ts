// Utilities
import { ref } from 'vue'

export type ActiveAnimations = Record<string, 'up' | 'down'>
export type PriceChanges = Record<string, number>

export const usePriceUpdater = () => {
  const priceChanges = ref<PriceChanges>({})
  const activeAnimations = ref<ActiveAnimations>({})

  const updatePrice = (uid: string, newPrice: number, oldPrice: number) => {
    const change = newPrice - oldPrice

    if (change !== 0) {
      priceChanges.value[uid] = change
      activeAnimations.value[uid] = change > 0 ? 'up' : 'down'
    }

    setTimeout(() => {
      delete priceChanges.value[uid]
      delete activeAnimations.value[uid]
    }, 1200)
  }

  return {
    priceChanges,
    activeAnimations,
    updatePrice,
  }
}
