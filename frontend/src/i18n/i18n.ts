// Utilities
import { createI18n } from 'vue-i18n'
import { messages } from '@/i18n/locales'

// Types
import type { PluralizationRule } from 'vue-i18n'

const ruRule: PluralizationRule = (choice) => {
  if (choice === 0) return 0 // 'Нет аналитиков'

  const teen = choice > 10 && choice < 20
  const endsWithOne = choice % 10 === 1

  if (!teen && endsWithOne) return 1 // '1 аналитик'
  if (!teen && choice % 10 >= 2 && choice % 10 <= 4) return 2 // '2 аналитика'

  return 3 // '5 аналитиков'
}

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  pluralRules: {
    ru: ruRule,
  },
  fallbackLocale: 'en',
  messages: messages,
})
