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

const plRule: PluralizationRule = (choice) => {
  if (choice === 0) return 0 // '0 firm'

  const isOne = choice === 1
  const endsWithTwoToFourButNotTeen =
    choice % 10 >= 2 &&
    choice % 10 <= 4 &&
    !(choice % 100 >= 12 && choice % 100 <= 14)

  if (isOne) return 1 // '1 firma'
  if (endsWithTwoToFourButNotTeen) return 2 // '2 firmy'

  return 3 // '5 firm'
}

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  pluralRules: {
    ru: ruRule,
    pl: plRule,
  },
  fallbackLocale: 'en',
  messages: messages,
})
