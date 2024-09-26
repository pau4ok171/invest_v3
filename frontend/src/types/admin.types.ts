import type {ValidationRule} from "@vuelidate/core";

export interface IAdminCompany {
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

export interface IFetchedDetailCompany {
  ticker: string,
  slug: string,
  uid: string,
  title: string,
  short_title: string,
  short_title_genitive: string,
  description: string,
  short_description: string,
  city: string,
  country: IFetchedCountry,
  market: IFetchedMarket,
  sector: IFetchedSector,
  industry: IFetchedIndustry,
  created: string,
  updated: string,
  created_by: IFetchedUser,
  updated_by: IFetchedUser,
  is_visible: boolean,
  logo: string,
  is_fund: boolean,
  website: string,
  year_founded: string,
}

export interface IFetchedCountry {
  id: number,
  name: string,
  name_iso: string,
  currency: IFetchedCurrency,
  flag_url: string,
}

export interface IFetchedMarket {
  title: string,
  slug: string,
  country: number,
}

export interface IFetchedSector {
  id: number,
  title: string,
  slug: string,
}

export interface IFetchedIndustry {
  title: string,
  slug: string,
  sector: number,
}

export interface IFetchedCurrency {
  name: string,
  symbol: string,
}

export interface IFetchedUser {
  first_name: string,
  last_name: string,
}

export interface IFormattedDetailCompany {
  ticker: string,
  slug: string,
  uid: string,
  companyName: string,
  shortCompanyName: string,
  shortCompanyNameGenitive: string,
  description: string,
  shortDescription: string,
  city: string,
  country: IFormattedCountry,
  market: IFormattedMarket,
  sector: IFormattedSector,
  industry: IFormattedIndustry,
  created: string,
  updated: string,
  createdBy: IFormattedUser,
  updatedBy: IFormattedUser,
  isVisible: boolean,
  logo: File,
  isFund: boolean,
  website: string,
  founded: string,
}
export type toPrevious<T> = {
	[P in keyof T]: {value: T[P], wasModified: boolean}
}
export type PreviousFormattedDetailCompany = toPrevious<IFormattedDetailCompany>

export interface IFormattedSelector {
  key: number,
  name: string,
  slug: string,
}

export interface IFormattedCountry extends IFormattedSelector{
  flagURL: string,
  currency: IFormattedCurrency,
}

export interface IFormattedMarket extends IFormattedSelector{

}

export interface IFormattedSector extends IFormattedSelector{
}

export interface IFormattedIndustry extends IFormattedSelector{
}

export interface IFormattedCurrency {
  name: string,
  symbol: string,
}

export interface IFormattedUser {
  firstName: string,
  lastName: string,
}

export interface ICompanyDataToRequest {
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

export type AdminModelValue = string | number | boolean | File | IFormattedSelector

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
  options?: string | IFormattedSelector[],
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
  options: string | IFormattedSelector[] | null,
}

export interface IAdminField {
  field: AdminFieldType,
  modelValue: keyof IFormattedDetailCompany,
  isRequired: boolean,
  isDisabled: boolean | string,
  label: string,
  helpText: string,
  validators: AdminValidatorType | {},
  wasModifiedIsNeeded: boolean,
  hasSearch: boolean | undefined,
  options: IFormattedSelector[] | undefined,
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

export const isKeyOfFormattedDetailCompany = (obj: IFormattedDetailCompany, key: string): key is keyof IFormattedDetailCompany => {
  return Object.hasOwn(obj, key)
}

export const isKeyOfPreviousFormattedDetailCompany = (obj: PreviousFormattedDetailCompany,  key: string): key is keyof PreviousFormattedDetailCompany => {
  return Object.hasOwn(obj, key)
}
