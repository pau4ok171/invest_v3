// Types
import type {
  CountryTranslations,
  CurrencyTranslations,
  ListCompany,
  Market,
  SectorTranslations,
  Snowflake,
} from '@/types/invest'

export interface BaseState {
  id: number
  key: string
}

export interface CountryState extends BaseState {
  translations: CountryTranslations
  markets: Market[]
}

export interface SectorState extends BaseState {
  translations: SectorTranslations
  parentKeys: number[]
}

export interface CurrencyState extends BaseState {
  translations: CurrencyTranslations
  symbol: string
}

export interface CompaniesOptions {
  side?: InfiniteScrollSide
  done: (status: InfiniteScrollStatus) => void
}

export interface CompaniesResponse {
  results: ListCompany[]
  next: string | null
  count: number
}

export type InfiniteScrollSide = 'start' | 'end' | 'both'
export type InfiniteScrollStatus = 'ok' | 'empty' | 'loading' | 'error'

export interface CompanyItem {
  companyLogo: string
  companyName: string
  lastPrice: string
  return7D: string
  return1Y: string
  marketCap: string
  consensus: string
  fairValue: string
  growth: string
  dividendYield: string
  sector: string
  watchlisted: boolean
  ticker: string
  to: string
  uid: string
  snowflake: Snowflake
  description: string
}
