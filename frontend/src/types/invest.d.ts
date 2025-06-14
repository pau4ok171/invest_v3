import { Statement } from '@/types/statements'

export interface CompanyTranslations {
  [languageCode: string]: {
    title: string
    short_title: string
    short_title_genitive: string
    description: string
    short_description: string
    city: string
  }
}

export interface CountryTranslations {
  [languageCode: string]: {
    name: string
    name_genitive: string
  }
}

export interface SectorTranslations {
  [languageCode: string]: {
    title: string
    description: string
  }
}

export interface CurrencyTranslations {
  [languageCode: string]: {
    name: string
  }
}

export interface CompanyPerformance {
  return_7d: number
  return_30d: number
  return_90d: number
  return_1y: number
  return_3y: number
  return_5y: number
  average_weekly_movement: number
  last_reported_earnings: number | null
  next_earnings: number | null
}

export interface DetailCompany {
  absolute_url: string
  analyst_ideas: Array<AnalystIdea>
  company_news: Array<News>
  country: Country
  translations: CompanyTranslations
  formatting: Formatting
  id: number
  logo_url: string
  market: Market
  next_dividend: Dividend
  price_data: PriceData
  reports: Array<Report>
  performance: CompanyPerformance
  sector: Sector
  sector_market: SectorMarket
  slug: string
  ticker: string
  uid: string
  website: string
  year_founded: number
}

export interface ListCompany {
  absolute_url: string
  country: Country
  translations: CompanyTranslations
  formatting: Formatting
  logo_url: string
  market: Market
  price_data: PriceData
  performance: CompanyPerformance
  sector: Sector
  statements: Statement[]
  ticker: string
  uid: string
  updated: string
}

export interface SearchCompany {
  absolute_url: string
  country: Country
  logo_url: string
  market: Market
  sector: Sector
  ticker: string
  translations: CompanyTranslations
  uid: string
}

export interface AnalystIdea {
  analyst: Analyst
  company: number
  currency: Currency
  date_target: string
  description: string
  id: number
  idea_created: string
  price_target: number
}

export interface Analyst {
  description: string
  id: number
  name: string
  score: number
}

export interface Currency {
  id: number
  translations: CurrencyTranslations
  iso_code: string
  symbol: string
}

export interface Report {
  assets: number
  cost_of_sales: number
  debt: number
  equity: number
  gross_margin: number
  income_net: number
  operation_expenses: number
  operation_income: number
  other_income_net: number
  sales: number
  scale: string
  scale_unit: number
  share_outstanding: number
  taxes: number
  total_employees_figure: number
  updated: string
}

export interface Country {
  currency: Currency
  id: number
  markets: Market[]
  slug: string
  translations: CountryTranslations
}

export interface Market {
  country: number
  id: number
  slug: string
  title: string
  return_7d: number
  return_30d: number
  return_90d: number
  return_1y: number
  return_3y: number
  return_5y: number
  average_weekly_mouvement: number
  volatility_10p: number
  volatility_90p: number
}

export interface Formatting {
  primaryCurrencyISO: string
  primaryCurrencySymbol: string
  reportCurrencyISO: string
  reportCurrencySymbol: string
  tradingCurrencyISO: string
  tradingCurrencySymbol: string
}

export interface PriceData {
  capitalisation: number
  last_price: number
}

export interface Sector {
  id: number
  main_header: string
  slug: string
  translations: SectorTranslations
  countries: Country[]
}

export interface Competitor {
  absolute_url: string
  country: Country
  formatting: Formatting
  id: number
  market: Market
  price_data: PriceData
  sector: Sector
  slug: string
  snowflake: Snowflake
  ticker: string
  translations: CompanyTranslations
  uid: string
}

export type SnowflakeKey = 'value' | 'future' | 'past' | 'health' | 'dividends'
export type Snowflake = Record<SnowflakeKey, Statement[]>

export interface Candle {
  close: number
  time: number
}

export interface News {
  id: number
  type: string
  date: string
  title: string
  content: string
}

export interface Dividend {
  currency: Currency
  declared_date: string
  dividend_amount: number
  dividend_yield: number
  ex_dividend_date: string
  pay_date: string
  scale: string
  scale_unit: number
}

export interface SectorMarket {
  average_weekly_mouvement: number
  return_1y: number
  return_30d: number
  return_3y: number
  return_5y: number
  return_7d: number
  return_90d: number
}
