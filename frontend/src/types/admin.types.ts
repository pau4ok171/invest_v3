import type {ValidationRule} from "@vuelidate/core";

export interface AdminCompany {
  id: number,
  ticker: string,
  slug: string,
  uid: string,
  title: string,
  short_title: string,
  is_visible: boolean,
  logo: string,
  is_fund: boolean,
  market_name: string,
  sector_name: string,
}

export interface FetchedDetailCompany {
  ticker: string,
  slug: string,
  uid: string,
  title: string,
  short_title: string,
  short_title_genitive: string,
  description: string,
  short_description: string,
  city: string,
  country: FetchedCountry,
  market: FetchedMarket,
  sector: FetchedSector,
  industry: FetchedIndustry,
  created: string,
  updated: string,
  created_by: FetchedUser,
  updated_by: FetchedUser,
  is_visible: boolean,
  logo: string,
  is_fund: boolean,
  website: string,
  year_founded: string,
}

export interface FetchedCountry {
  id: number,
  name: string,
  name_iso: string,
  currency: FetchedCurrency,
  flag_url: string,
}

export interface FetchedMarket {
  title: string,
  slug: string,
  country: number,
}

export interface FetchedSector {
  id: number,
  title: string,
  slug: string,
}

export interface FetchedIndustry {
  title: string,
  slug: string,
  sector: number,
}

export interface FetchedCurrency {
  name: string,
  symbol: string,
}

export interface FetchedUser {
  first_name: string,
  last_name: string,
}

export interface FormattedDetailCompany {
  ticker: string,
  slug: string,
  uid: string,
  companyName: string,
  shortCompanyName: string,
  shortCompanyNameGenitive: string,
  description: string,
  shortDescription: string,
  city: string,
  country: FormattedCountry,
  market: FormattedMarket,
  sector: FormattedSector,
  industry: FormattedIndustry,
  created: string,
  updated: string,
  createdBy: FormattedUser,
  updatedBy: FormattedUser,
  isVisible: boolean,
  logo: File,
  isFund: boolean,
  website: string,
  founded: string,
}
export type toPrevious<T> = {
	[P in keyof T]: {value: T[P], wasModified: boolean}
}
export type PreviousFormattedDetailCompany = toPrevious<FormattedDetailCompany>

export interface FormattedSelector {
  key: number,
  name: string,
  slug: string,
}

export interface FormattedCountry extends FormattedSelector{
  flagURL: string,
  currency: FormattedCurrency,
}

export interface FormattedMarket extends FormattedSelector{

}

export interface FormattedSector extends FormattedSelector{
}

export interface FormattedIndustry extends FormattedSelector{
}

export interface FormattedCurrency {
  name: string,
  symbol: string,
}

export interface FormattedUser {
  firstName: string,
  lastName: string,
}

export interface CompanyDataToRequest {
  ticker?: string,
  slug?: string,
  uid?: string,
  title?: string,
  short_title?: string,
  short_title_genitive?: string,
  description?: string,
  short_description?: string,
  city?: string,
  country_name_iso?: string,
  market_slug?: string,
  sector_slug?: string,
  industry_slug?: string,
  is_visible?: boolean,
  logo?: File,
  is_fund?: boolean,
  website?: string,
  year_founded?: string,
}

export enum FieldStatusEnum {
  DISABLED = 'disabled',
  INVALID = 'invalid',
  VALID = 'valid',
  VIRGIN = 'virgin',
}

export enum AdminComponentName {
  EMPTY = '',
  DASHBOARD = 'AdminDashboard',
  MODELS = 'AdminModels',
  MODEL = 'AdminModel',
  STAFF = 'AdminStaff',
  SETTINGS = 'AdminSettings',
}

export type AdminModelValue = string | number | boolean | File | FormattedSelector

export enum AdminFieldType {
  CHECKBOX='AdminCheckBoxField',
  CHAR='AdminCharField',
  IMAGE='AdminImageField',
  SELECTOR='AdminSelectorField',
  TEXT='AdminTextField',
  YEAR='AdminYearField',
}
export type AdminBaseValidatorType = { [p: string]: ValidationRule }
export type AdminDeepValidatorType = { [p: string]: { [p: string]: ValidationRule } }
export type AdminValidatorType = AdminBaseValidatorType | AdminDeepValidatorType


export interface IAdminFieldDeclared {
  field: AdminFieldType,
  modelValue?: string,
  isRequired?: boolean,
  isDisabled?: string | boolean,
  label?: string,
  helpText?: string,
  validators?: AdminValidatorType,
  wasModifiedIsNeeded?: boolean,
  hasSearch?: boolean,
  options?: string | FormattedSelector[],
}

export interface IDefaultField {
  modelValue: undefined,
  isDisabled: boolean,
  isRequired: boolean,
  label: string,
  helpText: string,
  validators: object,
  options: undefined,
  hasSearch: undefined,
  wasModifiedIsNeeded: boolean,
}

export interface IAdminUnitedField {
  field: AdminFieldType,
  modelValue: string | null,
  isRequired: boolean,
  isDisabled: string | boolean,
  label: string,
  helpText: string,
  validators: AdminValidatorType | {},
  wasModifiedIsNeeded: boolean,
  hasSearch: boolean | null,
  options: string | FormattedSelector[] | null,
}

export interface IAdminField {
  field: AdminFieldType,
  modelValue: keyof FormattedDetailCompany,
  isRequired: boolean,
  isDisabled: boolean | string,
  label: string,
  helpText: string,
  validators: AdminValidatorType | {},
  wasModifiedIsNeeded: boolean,
  hasSearch: boolean | undefined,
  options: FormattedSelector[] | undefined,
}
export const isAdminValidatorType = (validators: AdminValidatorType | {}): validators is AdminValidatorType => {
  return !!Object.keys(validators).length
}
export const isBaseValidators = (validators: AdminValidatorType): validators is AdminBaseValidatorType => {
  return !Object.hasOwn(validators, 'slug')
}


export interface IAdminModelDeclared {
  [p: string]: IAdminFieldDeclared
}

export interface IAdminModel {
  [p: string]: IAdminField
}

export const isAdminModel = (model: IAdminModelDeclared | IAdminModel): model is IAdminModel => {
  return Object.values(model).every(field => {
    return typeof field.isDisabled == 'boolean' && typeof field.options != 'string'
  })
}

export const isKeyOfFormattedDetailCompany = (obj: FormattedDetailCompany,  key: string): key is keyof FormattedDetailCompany => {
  return Object.hasOwn(obj, key)
}

export const isKeyOfPreviousFormattedDetailCompany = (obj: PreviousFormattedDetailCompany,  key: string): key is keyof PreviousFormattedDetailCompany => {
  return Object.hasOwn(obj, key)
}
