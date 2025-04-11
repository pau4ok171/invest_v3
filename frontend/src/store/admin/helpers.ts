import type {
  ICompanyDataToRequest,
  IFetchedDetailCompany,
  IFormattedDetailCompany,
  PreviousFormattedDetailCompany,
} from '@/types/admin.types'

export const getInitFormState = (): IFormattedDetailCompany => ({
  ticker: '',
  slug: '',
  uid: '',
  companyName: '',
  shortCompanyName: '',
  shortCompanyNameGenitive: '',
  description: '',
  shortDescription: '',
  city: '',
  country: {
    name: '',
    slug: '',
    key: -1,
    currency: { name: '', symbol: '' },
    flagURL: '',
  },
  market: { name: '', slug: '', parentKey: -1 },
  sector: { name: '', slug: '', key: -1 },
  industry: { name: '', slug: '', parentKey: -1 },
  created: '',
  updated: '',
  createdBy: { firstName: '', lastName: '' },
  updatedBy: { firstName: '', lastName: '' },
  isVisible: false,
  logo: null,
  isFund: false,
  website: '',
  founded: '',
})

export const formatCompanyData = async (
  company: IFetchedDetailCompany
): Promise<IFormattedDetailCompany> => {
  let logoFile: File | null = null

  if (company.logo) {
    try {
      const response = await fetch(company.logo)
      if (response.ok) {
        const blob = await response.blob()
        logoFile = new File([blob], 'logo.png', { type: blob.type })
      }
    } catch (e) {
      console.warn('Failed to load logo:', e)
    }
  }
  return {
    ticker: company.ticker || '',
    slug: company.slug || '',
    uid: company.uid || '',
    companyName: company.title || '',
    shortCompanyName: company.short_title || '',
    shortCompanyNameGenitive: company.short_title_genitive || '',
    description: company.description || '',
    shortDescription: company.short_description || '',
    city: company.city || '',
    country: {
      name: company.country.name || '',
      slug: company.country.name_iso || '',
      key: company.country.id || -1,
      currency: {
        name: company.country.currency.name || '',
        symbol: company.country.currency.symbol || '',
      },
      flagURL: company.country.flag_url,
    },
    market: {
      name: company.market.title || '',
      slug: company.market.slug || '',
      parentKey: company.market.country || -1,
    },
    sector: {
      name: company.sector.title || '',
      slug: company.sector.slug || '',
      key: company.sector.id || -1,
    },
    industry: {
      name: company.industry.title || '',
      slug: company.industry.slug || '',
      parentKey: company.industry.sector || -1,
    },
    created: company.created || '',
    updated: company.updated || '',
    createdBy: {
      firstName: company.created_by.first_name || '',
      lastName: company.created_by.last_name || '',
    },
    updatedBy: {
      firstName: company.updated_by.first_name || '',
      lastName: company.updated_by.last_name || '',
    },
    isVisible: company.is_visible || false,
    logo: logoFile,
    isFund: company.is_fund || false,
    website: company.website || '',
    founded: company.year_founded !== null ? String(company.year_founded) : '',
  }
}

export const prepareRequestData = async (
  companyData: IFormattedDetailCompany,
  previousCompanyData: PreviousFormattedDetailCompany
): Promise<ICompanyDataToRequest> => {
  const companyDataToRequest = {
    ticker: previousCompanyData['ticker'].isDirty
      ? companyData.ticker.trim().toUpperCase()
      : null,
    slug: previousCompanyData['slug'].isDirty ? companyData.slug.trim() : null,
    uid: previousCompanyData['uid'].isDirty ? companyData.uid.trim() : null,
    title: previousCompanyData['companyName'].isDirty
      ? companyData.companyName.trim()
      : null,
    short_title: previousCompanyData['shortCompanyName'].isDirty
      ? companyData.shortCompanyName.trim()
      : null,
    short_title_genitive: previousCompanyData['shortCompanyNameGenitive']
      .isDirty
      ? companyData.shortCompanyNameGenitive.trim()
      : null,
    description: previousCompanyData['description'].isDirty
      ? companyData.description.trim()
      : null,
    short_description: previousCompanyData['shortDescription'].isDirty
      ? companyData.shortDescription.trim()
      : null,
    city: previousCompanyData['city'].isDirty ? companyData.city.trim() : null,
    country_name_iso: previousCompanyData['country'].isDirty
      ? companyData.country.slug
      : null,
    market_slug: previousCompanyData['market'].isDirty
      ? companyData.market.slug
      : null,
    sector_slug: previousCompanyData['sector'].isDirty
      ? companyData.sector.slug
      : null,
    industry_slug: previousCompanyData['industry'].isDirty
      ? companyData.industry.slug
      : null,
    is_visible: previousCompanyData['isVisible'].isDirty
      ? companyData.isVisible
      : null,
    logo: previousCompanyData['logo'].isDirty ? companyData.logo : null,
    is_fund: previousCompanyData['isFund'].isDirty ? companyData.isFund : null,
    website: previousCompanyData['website'].isDirty
      ? companyData.website.trim()
      : null,
    year_founded: previousCompanyData['founded'].isDirty
      ? companyData.founded.trim()
      : null,
  }
  const filtered = Object.keys(companyDataToRequest)
    .filter(
      (k) => companyDataToRequest[k as keyof ICompanyDataToRequest] !== null
    )
    .reduce(
      (a, k) => ({
        ...a,
        [k]: companyDataToRequest[k as keyof ICompanyDataToRequest],
      }),
      {}
    )
  return getFormDataFromRequestData(filtered) as ICompanyDataToRequest
}

const getFormDataFromRequestData = (object: ICompanyDataToRequest) =>
  Object.keys(object).reduce((formData, key) => {
    const obj = object[key as keyof ICompanyDataToRequest]
    if (key === 'logo') {
      if (obj != undefined && obj instanceof File) {
        // https://stackoverflow.com/questions/63230458/django-rest-framework-doesnt-accept-blob-picture-file-file-extension-is-not
        formData.append(key, obj, 'logo.png')
      } else {
        formData.append(key, '__delete__')
      }
      return formData
    }
    if (key === 'year_founded' && typeof obj == 'string' && !obj.length) {
      formData.append(key, '__delete__')
      return formData
    }
    if (typeof obj == 'string') {
      formData.append(key, obj)
      return formData
    }
    if (typeof obj == 'boolean') {
      formData.append(key, obj.toString())
      return formData
    }
    return formData
  }, new FormData())
