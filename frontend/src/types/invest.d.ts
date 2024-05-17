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
    absolute_url: String,
    country: Country,
    formatting: Formatting,
    is_watchlisted: Boolean,
    logo_url: String,
    market: Market,
    price_data: PriceData,
    sector: Sector,
    ticker: String,
    title: String,
    uid: String,
    updated: String,
}

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
    primaryCurrencySymbol: String
    reportCurrencyISO: String
    reportCurrencySymbol: String
    tradingCurrencyISO: String
    tradingCurrencySymbol: String
}

export interface PriceData {
    capitalisation: Number,
    last_price: Number,
    return_1y: Number,
    return_7d: Number,
}

export interface Sector {
    main_header: String,
    slug: String,
    title: String,
}

export interface Competitor {
    analyst_ideas: Array<AnalystIdea>,
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