import {defineStore} from "pinia";
import type {
  CompanyDataToRequest,
  FetchedDetailCompany,
  FormattedCountry,
  FormattedDetailCompany,
  FormattedIndustry,
  FormattedMarket,
  FormattedSector,
  FormattedUser,
  PreviousFormattedDetailCompany
} from "@/types/admin.types";
import {AdminComponentName, isKeyOfFormattedDetailCompany} from "@/types/admin.types";
import axios, {AxiosError} from "axios";
import {toast} from "vue3-toastify";

export const useAdminStore = defineStore({
  id: 'admin',
  state: () => ({
    activeComponent: AdminComponentName.DASHBOARD,
    previousComponent: AdminComponentName.EMPTY,
    companyUID: '',
    companyFormData: getEmptyCompanyFormData(),
    previousCompanyFormData: getPreviousCompanyFormData(),
    // Model
    modelIsSaving: false,
    editModeActivated: false,
    isNewModel: false,
    modelWasModified: false,
  }),
  getters: {
    getModelWasModified: ((state) => Object.values(state.previousCompanyFormData).some(v => v.wasModified)),
  },
  actions: {
    async initAdminStore() {
      this.companyFormData = getEmptyCompanyFormData()
      this.previousCompanyFormData = getPreviousCompanyFormData()
    },
    async deleteModelData() {
      this.companyUID = ''
      this.companyFormData = getEmptyCompanyFormData()
      this.previousCompanyFormData = getPreviousCompanyFormData()
      this.isNewModel = false
    },
    async fetchCompany() {
      const companyUID = this.companyUID
      const company: FetchedDetailCompany = await axios
        .get(`api/v1/admin/companies/${companyUID}/`)
        .then(response => response.data)
        .catch(error => console.log(error))

      this.companyFormData = await getFormattedCompanyData(company)
    },
    async saveModelForm() {
      let company: FetchedDetailCompany
      // Set ModelIsSaving
      this.modelIsSaving = true
      // PrepareData
      const companyData: FormattedDetailCompany = this.companyFormData
      const preparedCompanyData = await getCompanyDataToRequest(companyData, this.previousCompanyFormData)
      // CreateDataObject
      const formData = getFormDataFromRequestData(preparedCompanyData)
      // If NewModel => POST Request
      try {
        if (this.isNewModel) {
          company = await axios
            .post('api/v1/admin/companies/', formData)
            .then(response => {
              this.companyUID = response.data.uid
              toast.success('Company is successfully created')
              return response.data
            })
            .catch(this.catchAxiosError)
        }
        // If OldModel => PATCH Request
        else {
          const companyUID = this.companyUID
          company = await axios
            .patch(`api/v1/admin/companies/${companyUID}/`, formData)
            .then(response => {
              this.companyUID = response.data.uid
              toast.success('Company is successfully saved')
              return response.data
            })
            .catch(this.catchAxiosError)
        }
        const companyFormData = await getFormattedCompanyData(company)

        this.editModeActivated = false
        this.companyFormData = companyFormData
        this.previousCompanyFormData = getPreviousCompanyFormData()
        this.isNewModel = false
        window.scrollTo({top: 0, behavior: 'smooth'})
      } finally {
        // Reset ModelIsSaving
        this.modelIsSaving = false
      }
    },
    async deleteModel() {
      // Send DELETE Request
      try {
        await axios
            .delete(`api/v1/admin/companies/${this.companyUID}/`)
            .then(async () => {
              // Open Models Component
              this.activeComponent = AdminComponentName.MODELS
              // Notify Client
              toast.success('Company is successfully deleted')
            })
            .catch(e => console.log(e))
      }
      catch (e) {
        console.log(e)
      }
    },
    async catchAxiosError(error: AxiosError) {
      // client received an error response (5xx, 4xx)
      if (error.response) {
        console.log(error)
        toast.error('Something was wrong...')
        // client never received a response, or request never left
      } else if (error.request) {
        console.log(error)
        toast.error('Something was wrong...')
        // anything else
      } else {
        console.log(error)
        toast.error('Something was wrong...')
      }
    },
    async activateEditMode() {
      this.previousCompanyFormData = getPreviousCompanyFormData(this.companyFormData)
      this.editModeActivated = true
    },
    async deactivateEditMode() {
      await this.resetField('__all__')
      this.editModeActivated = false
      if (this.isNewModel) {
        await this.deleteModelData()
        this.activeComponent = AdminComponentName.MODELS
      }
    },
    async resetField(key: '__all__' | string) {
      let companyFormData: FormattedDetailCompany = {...this.companyFormData}
      const previousCompanyFormData: PreviousFormattedDetailCompany = {...this.previousCompanyFormData}

      if (key === '__all__') {
        companyFormData = Object.keys(companyFormData).reduce((obj, k) => {
          return {...obj, [k]: previousCompanyFormData[k as keyof PreviousFormattedDetailCompany].value}
        }, {} as FormattedDetailCompany)
        this.companyFormData = companyFormData
        return
      }

      if (isKeyOfFormattedDetailCompany(companyFormData, key)) {
        companyFormData = {...companyFormData, [key]: previousCompanyFormData[key].value}
      }

      if (key === 'country' || key === 'market') {
        companyFormData['country'] = this.previousCompanyFormData['country'].value
        companyFormData['market'] = this.previousCompanyFormData['market'].value
      }
      if (key === 'sector' || key === 'industry') {
        companyFormData['sector'] = this.previousCompanyFormData['sector'].value
        companyFormData['industry'] = this.previousCompanyFormData['industry'].value
      }
      if (key === 'ticker') {
        companyFormData['slug'] = this.previousCompanyFormData['slug'].value
      }
      this.companyFormData = companyFormData
    },
  },
})

const getEmptyCompanyFormData = (): FormattedDetailCompany => {
  return {
    ticker: '',
    slug: '',
    uid: '',
    companyName: '',
    shortCompanyName: '',
    shortCompanyNameGenitive: '',
    description: '',
    shortDescription: '',
    city: '',
    country: {name: '', slug: '', key: 0} as FormattedCountry,
    market: {name: '', slug: '', key: 0} as FormattedMarket,
    sector: {name: '', slug: '', key: 0} as FormattedSector,
    industry: {name: '', slug: '', key: 0} as FormattedIndustry,
    created: '',
    updated: '',
    createdBy: {firstName: '', lastName: ''} as FormattedUser,
    updatedBy: {firstName: '', lastName: ''} as FormattedUser,
    isVisible: false,
    logo: {} as File,
    isFund: false,
    website: '',
    founded: '',
  }
}

const getPreviousCompanyFormData = (company: FormattedDetailCompany|undefined = undefined): PreviousFormattedDetailCompany => {
  return Object.entries(company || getEmptyCompanyFormData()).reduce((obj, [k, v]) => {
    return {...obj, [k]: {value: v, wasModified: false}}
  }, {} as PreviousFormattedDetailCompany)
}

const getFormDataFromRequestData = (object: CompanyDataToRequest) => Object.keys(object).reduce((formData, key) => {
  const obj = object[key as keyof CompanyDataToRequest]
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

const getFormattedCompanyData = async (company: FetchedDetailCompany): Promise<FormattedDetailCompany> => {
  let file = await fetch(company.logo).then(r => r.blob()).then(blobFile => new File([blobFile], "CompanyLogo", {type: "image/png"}))
  return {
    ticker: company.ticker  || '',
    slug: company.slug  || '',
    uid: company.uid  || '',
    companyName: company.title  || '',
    shortCompanyName: company.short_title  || '',
    shortCompanyNameGenitive: company.short_title_genitive  || '',
    description: company.description  || '',
    shortDescription: company.short_description  || '',
    city: company.city  || '',
    country: {
      name: company.country.name  || '',
      slug: company.country.name_iso  || '',
      key: company.country.id  || '',
      currency: {
        name: company.country.currency.name  || '',
        symbol: company.country.currency.symbol  || '',
      },
      flagURL: company.country.flag_url
    },
    market: {
      name: company.market.title || '',
      slug: company.market.slug || '',
      key: company.market.country || '',
    },
    sector: {
      name: company.sector.title || '',
      slug: company.sector.slug || '',
      key: company.sector.id  || '',
    },
    industry: {
      name: company.industry.title  || '',
      slug: company.industry.slug  || '',
      key: company.industry.sector  || '',
    },
    created: company.created  || '',
    updated: company.updated  || '',
    createdBy: {
      firstName: company.created_by.first_name  || '',
      lastName: company.created_by.last_name  || '',
    },
    updatedBy: {
      firstName: company.updated_by.first_name  || '',
      lastName: company.updated_by.last_name  || '',
    },
    isVisible: company.is_visible  || false,
    logo: file,
    isFund: company.is_fund || false,
    website: company.website || '',
    founded: company.year_founded !== null ? String(company.year_founded) : '',
  } as FormattedDetailCompany
}

const getCompanyDataToRequest = async (companyData: FormattedDetailCompany, previousCompanyData: PreviousFormattedDetailCompany): Promise<CompanyDataToRequest> => {
  const companyDataToRequest = {
    ticker: previousCompanyData['ticker'].wasModified?companyData.ticker.trim().toUpperCase():null,
    slug: previousCompanyData['slug'].wasModified?companyData.slug.trim():null,
    uid: previousCompanyData['uid'].wasModified?companyData.uid.trim():null,
    title: previousCompanyData['companyName'].wasModified?companyData.companyName.trim():null,
    short_title: previousCompanyData['shortCompanyName'].wasModified?companyData.shortCompanyName.trim():null,
    short_title_genitive: previousCompanyData['shortCompanyNameGenitive'].wasModified?companyData.shortCompanyNameGenitive.trim():null,
    description: previousCompanyData['description'].wasModified?companyData.description.trim():null,
    short_description: previousCompanyData['shortDescription'].wasModified?companyData.shortDescription.trim():null,
    city: previousCompanyData['city'].wasModified?companyData.city.trim():null,
    country_name_iso: previousCompanyData['country'].wasModified?companyData.country.slug:null,
    market_slug: previousCompanyData['market'].wasModified?companyData.market.slug:null,
    sector_slug: previousCompanyData['sector'].wasModified?companyData.sector.slug:null,
    industry_slug: previousCompanyData['industry'].wasModified?companyData.industry.slug:null,
    is_visible: previousCompanyData['isVisible'].wasModified?companyData.isVisible:null,
    logo: previousCompanyData['logo'].wasModified?companyData.logo:null,
    is_fund: previousCompanyData['isFund'].wasModified?companyData.isFund:null,
    website: previousCompanyData['website'].wasModified?companyData.website.trim():null,
    year_founded: previousCompanyData['founded'].wasModified?companyData.founded.trim():null,
  }
  return Object.keys(companyDataToRequest)
      .filter(k => companyDataToRequest[k as keyof CompanyDataToRequest] !== null)
      .reduce((a, k) => ({...a, [k]: companyDataToRequest[k as keyof CompanyDataToRequest]}), {})
}