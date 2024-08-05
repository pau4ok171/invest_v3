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
  createdBy: FetchedUser,
  updatedBy: FetchedUser,
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
