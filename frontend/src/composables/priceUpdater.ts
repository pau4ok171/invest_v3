// Utilities
import { ref } from 'vue'

export type ActiveAnimations = Record<string, 'up' | 'down'>
export type PriceChanges = Record<string, number>

export const usePriceUpdater = () => {
  const priceChanges = ref<PriceChanges>({})
  const activeAnimations = ref<ActiveAnimations>({})

  const updatePrice = (key: string, newPrice: number, oldPrice: number) => {
    const change = newPrice - oldPrice

    if (change !== 0) {
      priceChanges.value[key] = change
      activeAnimations.value[key] = change > 0 ? 'up' : 'down'
    }

    setTimeout(() => {
      delete priceChanges.value[key]
      delete activeAnimations.value[key]
    }, 1200)
  }

  return {
    priceChanges,
    activeAnimations,
    updatePrice,
  }
}
