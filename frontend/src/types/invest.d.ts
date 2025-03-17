export interface DetailCompany {
  absolute_url: string | undefined
  analyst_ideas: Array<AnalystIdea>
  average_weekly_mouvement: number | undefined
  company_news: Array<News>
  country: Country
  description: string | undefined
  formatting: Formatting
  id: number | undefined
  is_watchlisted: boolean | undefined
  last_reported_earnings: string | undefined
  logo_url: string | undefined
  market: Market
  next_dividend: Dividend
  next_earnings: string | undefined
  price_data: PriceData
  reports: Array<Report>
  return_1y: number | undefined
  return_30d: number | undefined
  return_3y: number | undefined
  return_5y: number | undefined
  return_7d: number | undefined
  return_90d: number | undefined
  sector: Sector
  sector_market: SectorMarket
  short_description: string | undefined
  slug: string | undefined
  ticker: string | undefined
  title: string | undefined
  uid: string | undefined
  website: string | undefined
  year_founded: number | undefined
}

export interface ListCompany {
  absolute_url: string
  average_weekly_mouvement: number
  country: Country
  formatting: Formatting
  is_watchlisted: boolean
  logo_url: string
  market: Market
  price_data: PriceData
  return_1y: number
  return_30d: number
  return_3y: number
  return_5y: number
  return_7d: number
  return_90d: number
  sector: Sector
  ticker: string
  title: string
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
  title: string
  uid: string
}

export interface AnalystIdea {
    analyst: Analyst,
    company: number | undefined,
    currency: Currency,
    date_target: string | undefined,
    description: string | undefined,
    id: number | undefined,
    idea_created: string | undefined,
    price_target: number | undefined,
}

export interface Analyst {
    description: string | undefined,
    id: number | undefined,
    name: string | undefined,
    score: number | undefined,
}

export interface Currency {
    id: number | undefined,
    name: string | undefined,
    name_iso: string | undefined,
    symbol: string | undefined,
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
  id: number | undefined
  markets: Array<Market>
  slug: string | undefined
  title: string | undefined
}

export interface Market {
    country: number | undefined
    id: number | undefined
    slug: string | undefined
    title: string | undefined
    return_7d: number | undefined
    return_30d: number | undefined
    return_90d: number | undefined
    return_1y: number | undefined
    return_3y: number | undefined
    return_5y: number | undefined
    average_weekly_mouvement: number | undefined
    volatility_10p: number | undefined
    volatility_90p: number | undefined
}

export interface Formatting {
    primaryCurrencyISO: string | undefined
    primaryCurrencySymbol: string | undefined
    reportCurrencyISO: string | undefined
    reportCurrencySymbol: string | undefined
    tradingCurrencyISO: string | undefined
    tradingCurrencySymbol: string | undefined
}

export interface PriceData {
    capitalisation: number | undefined
    last_price: number | undefined
}

export interface Sector {
    main_header: string | undefined,
    slug: string | undefined,
    title: string | undefined,
}

export interface Competitor {
    absolute_url: string,
    country: Country,
    formatting: Formatting,
    id: number,
    market: Market,
    price_data: PriceData,
    sector: Sector,
    slug: string,
    snowflake: Snowflake,
    ticker: string,
    title: string,
    uid: string,
}

export interface Snowflake {
  dividends: number
  future: number
  health: number
  past: number
  value: number
}

export interface Candle {
  close: number
  time: number
}

export interface News {
    id: number,
    type: string,
    date: string,
    title: string,
    content: string,
}

export interface Dividend {
  currency: Currency
  declared_date: string | undefined
  dividend_amount: number | undefined
  dividend_yield: number | undefined
  ex_dividend_date: string | undefined
  pay_date: string | undefined
  scale: string | undefined
  scale_unit: number | undefined
}

export interface SectorMarket {
  average_weekly_mouvement: number | undefined
  return_1y: number | undefined
  return_30d: number | undefined
  return_3y: number | undefined
  return_5y: number | undefined
  return_7d: number | undefined
  return_90d: number | undefined
}