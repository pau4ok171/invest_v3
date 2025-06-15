// Utilities
import * as validators from '@vuelidate/validators'
import { i18n } from '@/i18n/i18n'

const { createI18nMessage } = validators

const formatPropertyName = (property: string) => {
  if (!property) return ''
  return property.replace(/[-_]/g, ' ').replace(/^\S/, (a) => a.toUpperCase())
}

const withI18nMessage = createI18nMessage({
  t: i18n.global.t.bind(i18n),
  messageParams: ($params) => {
    if ($params.property) {
      return {
        ...$params,
        property: i18n.global.t(`labels.${$params.property}`),
      }
    }
    return $params
  },
})

export const required = withI18nMessage(validators.required)
export const minLength = withI18nMessage(validators.minLength, {
  withArguments: true,
})
export const emailField = withI18nMessage(validators.email)
