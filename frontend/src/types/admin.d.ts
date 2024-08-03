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

export interface AdminDetailCompany {
  id: number | null,
  ticker: string | null,
  slug: string | null,
  uid: string | null,
  title: string | null,
  shortTitle: string | null,
  isVisible: boolean | null,
  logo: File | null,
  isFund: boolean | null,
  marketName: string | null,
  sectorName: string | null,
  industryName: string | null,
  absoluteURL: string | null,
  country_flag: string | null,
  currencySymbol: string | null,
  created: string | null,
  updated: string | null,
}

export interface SelectorOption {
  name: string,
  slug: string,
}