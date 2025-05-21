// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { ref, watch } from 'vue'

interface TitleParams {
  [key: string]: string | number
}

export function useTitle() {
  const { t, locale } = useI18n()
  const currentTitle = ref<string>('')

  const currentParams = ref<TitleParams>({})

  const setTitle = (titleKey: string, params: TitleParams = {}) => {
    currentTitle.value = titleKey
    currentParams.value = params
    document.title = t(titleKey, params)
  }

  watch([locale, currentTitle, currentParams], () => {
    if (currentTitle.value) {
      document.title = t(currentTitle.value, currentParams.value)
    }
  })

  return { setTitle }
}
