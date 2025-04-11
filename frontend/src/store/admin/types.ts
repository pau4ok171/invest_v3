// Types
import type {IFormattedDetailCompany} from "@/types/admin.types";

export type FormState = {
  [K in keyof IFormattedDetailCompany]: IFormattedDetailCompany[K]
}

export type PreviousFormState = {
  [K in keyof IFormattedDetailCompany]: {
    value: FormState[K]
    isDirty: boolean
  }
}

export type DependentFieldMap = {
  [K in keyof IFormattedDetailCompany]?: Array<keyof IFormattedDetailCompany>
}