import { useI18n } from 'vue-i18n'

type TranslationObject = Record<string, Record<string, string> | undefined>

export function useTranslations() {
  const { locale, fallbackLocale } = useI18n()

  const getFallbackLocale = (): string => {
    if (typeof fallbackLocale.value === 'string') {
      return fallbackLocale.value
    }
    if (Array.isArray(fallbackLocale.value)) {
      return fallbackLocale.value[0]
    }
    return 'en'
  }

  const getTranslation = (
    translations: TranslationObject,
    field: string
  ): string => {
    const currentLocale = locale.value
    const fallback = getFallbackLocale()

    return (
      translations?.[currentLocale]?.[field] ||
      translations?.[fallback]?.[field] ||
      translations?.en?.[field] ||
      ''
    )
  }

  return {
    getTranslation,
    getCurrentLocale: () => locale.value,
    getFallbackLocale,
  }
}
