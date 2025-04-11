export interface IAdminCompany {
  id: number
  ticker: string
  slug: string
  uid: string
  title: string
  short_title: string
  is_visible: boolean
  logo: string
  is_fund: boolean
  market_name: string
  sector_name: string
}

export interface IFetchedDetailCompany {
  ticker: string
  slug: string
  uid: string
  title: string
  short_title: string
  short_title_genitive: string
  description: string
  short_description: string
  city: string
  country: IFetchedCountry
  market: IFetchedMarket
  sector: IFetchedSector
  industry: IFetchedIndustry
  created: string
  updated: string
  created_by: IFetchedUser
  updated_by: IFetchedUser
  is_visible: boolean
  logo: string
  is_fund: boolean
  website: string
  year_founded: string
}

export interface IFetchedCountry {
  id: number
  name: string
  name_iso: string
  currency: IFetchedCurrency
  flag_url: string
}

export interface IFetchedMarket {
  title: string
  slug: string
  country: number
}

export interface IFetchedSector {
  id: number
  title: string
  slug: string
}

export interface IFetchedIndustry {
  title: string
  slug: string
  sector: number
}

export interface IFetchedCurrency {
  name: string
  symbol: string
}

export interface IFetchedUser {
  first_name: string
  last_name: string
}

export interface IFormattedDetailCompany {
  ticker: string
  slug: string
  uid: string
  companyName: string
  shortCompanyName: string
  shortCompanyNameGenitive: string
  description: string
  shortDescription: string
  city: string
  country: IFormattedCountry
  market: IFormattedMarket
  sector: IFormattedSector
  industry: IFormattedIndustry
  created: string
  updated: string
  createdBy: IFormattedUser
  updatedBy: IFormattedUser
  isVisible: boolean
  logo: File | null
  isFund: boolean
  website: string
  founded: string
}
export type toPrevious<T> = {
  [P in keyof T]: { value: T[P]; isDirty: boolean }
}
export type PreviousFormattedDetailCompany = toPrevious<IFormattedDetailCompany>

export interface IFormattedSelector {
  name: string
  slug: string
}

export interface IFormattedCountry extends IFormattedSelector {
  key: number
  flagURL: string
  currency: IFormattedCurrency
}

export interface IFormattedMarket extends IFormattedSelector {
  parentKey: number
}

export interface IFormattedSector extends IFormattedSelector {
  key: number
}

export interface IFormattedIndustry extends IFormattedSelector {
  parentKey: number
}

export interface IFormattedCurrency {
  name: string
  symbol: string
}

export interface IFormattedUser {
  firstName: string
  lastName: string
}

export interface ICompanyDataToRequest {
  ticker?: string
  slug?: string
  uid?: string
  title?: string
  short_title?: string
  short_title_genitive?: string
  description?: string
  short_description?: string
  city?: string
  country_name_iso?: string
  market_slug?: string
  sector_slug?: string
  industry_slug?: string
  is_visible?: boolean
  logo?: File
  is_fund?: boolean
  website?: string
  year_founded?: string
}
