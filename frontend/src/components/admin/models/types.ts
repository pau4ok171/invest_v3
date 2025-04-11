// Types
import type {
  NestedValidations,
  ValidationRule,
  ValidationRuleWithoutParams,
} from '@vuelidate/core'
import type { IFormattedDetailCompany } from '@/types/admin.types'

type FieldType = 'checkbox' | 'text' | 'textarea' | 'selector' | 'image'

export interface BaseField {
  key: keyof IFormattedDetailCompany
  type: FieldType
  label?: string
  helpText?: string
  hasReset?: boolean
  validators?: Record<
    string,
    ValidationRule | ValidationRuleWithoutParams | NestedValidations
  >
}
export interface EnrichedBaseField extends BaseField {
  label: string
  helpText: string
  hasReset: boolean
  validators: Record<
    string,
    ValidationRule | ValidationRuleWithoutParams | NestedValidations
  >
}

interface CheckboxField extends BaseField {
  type: 'checkbox'
  helpText?: undefined
}
interface EnrichedCheckboxField extends EnrichedBaseField {
  type: 'checkbox'
}
interface TextField extends BaseField {
  type: 'text'
}
interface EnrichedTextField extends BaseField {
  type: 'text'
}
interface TextareaField extends BaseField {
  type: 'textarea'
}
interface EnrichedTextareaField extends BaseField {
  type: 'textarea'
}
export interface SelectorItem {
  name: string
  slug: string
}
interface SelectorField extends BaseField {
  type: 'selector'
  items: SelectorItem[]
}
interface EnrichedSelectorField extends BaseField {
  type: 'selector'
  items: SelectorItem[]
}
interface ImageField extends BaseField {
  type: 'image'
}
interface EnrichedImageField extends BaseField {
  type: 'image'
}

export type FormField =
  | CheckboxField
  | TextField
  | TextareaField
  | SelectorField
  | ImageField
export type EnrichedFormField =
  | EnrichedCheckboxField
  | EnrichedTextField
  | EnrichedTextareaField
  | EnrichedSelectorField
  | EnrichedImageField
