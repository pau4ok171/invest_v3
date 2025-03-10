export interface DetailCompany {
    analyst_ideas: Array<AnalystIdea>,
    reports: Array<Report>,
    country: Country,
    formatting: Formatting,
    market: Market,
    sector_market: SectorMarket,
    price_data: PriceData,
    sector: Sector,
    id: number,
    year_founded: number,
    is_watchlisted: boolean,
    absolute_url: string,
    logo_url: string,
    title: string,
    ticker: string,
    uid: string,
    slug: string,
    description: string,
    short_description: string,
    website: string,
    company_news: Array<News>,
    next_dividend: Dividend,
    last_reported_earnings: string,
    next_earnings: string,
    return_7d: number,
    return_30d: number,
    return_90d: number,
    return_1y: number,
    return_3y: number,
    return_5y: number,
    average_weekly_mouvement: number,
}

export interface ListCompany {
    absolute_url: string,
    country: Country,
    formatting: Formatting,
    is_watchlisted: boolean,
    logo_url: string,
    market: Market,
    price_data: PriceData,
    sector: Sector,
    ticker: string,
    title: string,
    uid: string,
    updated: string,
}

export interface SearchCompany {
    uid: string,
    title: string,
    ticker: string,
    logo_url: string,
    country: Country,
    sector: Sector,
    market: Market,
    absolute_url: string,
}

export interface SearchCompanyItems extends Array<SearchCompany>{}

export interface AnalystIdea {
    analyst: Analyst,
    company: number,
    currency: Currency,
    date_target: string,
    description: string,
    id: number,
    idea_created: string,
    price_target: number,
}

export interface Analyst {
    description: string,
    id: number,
    name: string,
    score: number,
}

export interface Currency {
    id: number,
    name: string,
    name_iso: string,
    symbol: string,
}

export interface Report {
    total_employees_figure: number,
    updated: string,
    scale: string,
    scale_unit: number,
    income_net: number,
    sales: number,
    cost_of_sales: number,
    equity: number,
    debt: number,
    gross_margin: number,
    operation_expenses: number,
    operation_income: number,
    other_income_net: number,
    taxes: number,
    share_outstanding: number,
    assets: number,
}

export interface Country {
    currency: Currency,
    id: number,
    markets: Array<Market>
    slug: string,
    title: string,
}

export interface Market {
    country: number,
    id: number,
    slug: string,
    title: string,
    return_7d: number,
    return_30d: number,
    return_90d: number,
    return_1y: number,
    return_3y: number,
    return_5y: number,
    average_weekly_mouvement: number,
    volatility_10p: number,
    volatility_90p: number,
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
    capitalisation: number,
    last_price: number,
}

export interface Sector {
    main_header: string,
    slug: string,
    title: string,
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
    value: number,
    future: number,
    past: number,
    health: number,
    dividends: number,
}

export interface Candle {
    close: number,
    time: number,
}

export interface News {
    id: number,
    type: string,
    date: string,
    title: string,
    content: string,
}

export interface  Dividend {
    scale: string,
    scale_unit: number,
    dividend_yield: number,
    dividend_amount: number,
    declared_date: string,
    ex_dividend_date: string,
    pay_date: string,
    currency: Currency,
}

export interface SectorMarket {
    return_7d: number,
    return_30d: number,
    return_90d: number,
    return_1y: number,
    return_3y: number,
    return_5y: number,
    average_weekly_mouvement: number,
}