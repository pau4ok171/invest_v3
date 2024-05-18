export interface DetailCompany {
    analyst_ideas: Array<AnalystIdea>,
    reports: Array<Report>,
    country: Country,
    formatting: Formatting,
    market: Market,
    price_data: PriceData,
    sector: Sector,
    id: Number,
    year_founded: Number,
    is_watchlisted: Boolean,
    absolute_url: String,
    logo_url: String,
    title: String,
    ticker: String,
    uid: String,
    slug: String,
    description: String,
    short_description: String,
    website: String,
}

export interface ListCompany {
    absolute_url: string,
    country: Country,
    formatting: Formatting,
    is_watchlisted: Boolean,
    logo_url: string,
    market: Market,
    price_data: PriceData,
    sector: Sector,
    ticker: String,
    title: string,
    uid: String,
    updated: String,
}

export interface SearchCompany {
    uid: string,
    title: String,
    logo_url: string,
    country: Country,
    sector: Sector,
    market: Market,
    absolute_url: string,
}

export interface SearchCompanyItems extends Array<SearchCompany>{}

export interface AnalystIdea {
    analyst: Analyst,
    company: Number,
    currency: Currency,
    date_target: String,
    description: String,
    id: Number,
    idea_created: String,
    price_target: Number,
}

export interface Analyst {
    description: String,
    id: Number,
    name: String,
    score: Number,
}

export interface Currency {
    id: Number,
    name: String,
    name_iso: String,
    symbol: String,
}

export interface Report {
    total_employees_figure: Number,
    updated: String,
}

export interface Country {
    currency: Currency,
    id: Number,
    markets: Array<Market>
    slug: String,
    title: String,
}

export interface Market {
    country: Number,
    id: Number,
    slug: String,
    title: String,
}

export interface Formatting {
    primaryCurrencyISO: String
    primaryCurrencySymbol: string
    reportCurrencyISO: String
    reportCurrencySymbol: String
    tradingCurrencyISO: String
    tradingCurrencySymbol: String
}

export interface PriceData {
    capitalisation: number,
    last_price: number,
    return_1y: number,
    return_7d: number,
}

export interface Sector {
    main_header: String,
    slug: String,
    title: string,
}

export interface Competitor {
    absolute_url: string,
    country: Country,
    formatting: Formatting,
    id: Number,
    market: Market,
    price_data: PriceData,
    sector: Sector,
    slug: String,
    snowflake: Snowflake,
    ticker: String,
    title: String,
    uid: String,
}

export interface Snowflake {
    value: Number,
    future: Number,
    past: Number,
    health: Number,
    dividends: Number,
}

export interface Candle {
    close: Number,
    time: Number,
}