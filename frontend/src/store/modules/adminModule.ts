import type {Module} from "vuex";
import type {
  FetchedDetailCompany,
  FormattedCountry,
  FormattedDetailCompany,
  FormattedIndustry,
  FormattedMarket,
  FormattedSector,
  FormattedUser,
  CompanyDataToRequest,
} from "@/types/admin";
import axios from "axios";
import getSlug from "speakingurl";
import _ from "lodash";
import {toast} from "vue3-toastify";


export const adminModule = {
  state: () => ({
    activeComponent: 'AdminDashboard',
    companyUID: '',
    companyFormData: getEmptyCompanyFormData(),
    // MODEL
    modelIsSaving: false,
    editModeActivated: false,
    isNewModel: false,
  }),
  getters: {
    getCompanyUID(state) {
      return state.companyUID
    },
    getEditModeActivated(state) {
      return state.editModeActivated
    },
  },
  mutations: {
    setActiveComponent(state, payload: string) {
      state.activeComponent = payload
    },
    setCompanyUID(state, payload: string) {
      state.companyUID = payload
    },
    setCompanyFormData(state, payload: FormattedDetailCompany) {
      state.companyFormData = payload
    },
    setModelIsSaving(state, payload: boolean) {
      state.modelIsSaving = payload
    },
    setIsNewModel(state, payload: boolean) {
      state.isNewModel = payload
    },
    setEditModeActivated(state, payload: boolean) {
      state.editModeActivated = payload
    },
    setCompanyModelIsVisible(state, payload: boolean) {
      state.companyFormData.isVisible = payload
    },
    setCompanyModelCompanyName(state, payload: string) {
      state.companyFormData.companyName = payload
    },
    setCompanyModelShortCompanyName(state, payload: string) {
      state.companyFormData.shortCompanyName = payload
    },
    setCompanyModelShortCompanyNameGenitive(state, payload: string) {
      state.companyFormData.shortCompanyNameGenitive = payload
    },
    setCompanyModelTicker(state, payload: string) {
      state.companyFormData.ticker = payload
      state.companyFormData.slug = getSlug(_.kebabCase(payload))
    },
    setCompanyModelSlug(state, payload: string) {
      state.companyFormData.slug = payload
    },
    setCompanyModelUID(state, payload: string) {
      state.companyFormData.uid = payload
    },
    setCompanyModelCountry(state, payload: FormattedCountry) {
      state.companyFormData.market = {name: '', slug: '', key: ''}
      state.companyFormData.country = payload
    },
    setCompanyModelMarket(state, payload: FormattedMarket) {
      state.companyFormData.market = payload
    },
    setCompanyModelSector(state, payload: FormattedSector) {
      state.companyFormData.industry = {name: '', slug: '', key: ''}
      state.companyFormData.sector = payload
    },
    setCompanyModelIndustry(state, payload: FormattedIndustry) {
      state.companyFormData.industry = payload
    },
    setCompanyModelLogo(state, payload: File) {
      state.companyFormData.logo = payload
    },
    setCompanyModelDescription(state, payload: string) {
      state.companyFormData.description = payload
    },
    setCompanyModelShortDescription(state, payload: string) {
      state.companyFormData.shorDescription = payload
    },
    setCompanyModelIsFund(state, payload: boolean) {
      state.companyFormData.isFund = payload
    },
    setCompanyModelCity(state, payload: string) {
      state.companyFormData.city = payload
    },
    setCompanyModelWebsite(state, payload: string) {
      state.companyFormData.website = payload
    },
    setCompanyModelFounded(state, payload: number) {
      state.companyFormData.founded = payload
    },
  },
  actions: {
    initAdminStore({commit}) {
      commit('setCompanyFormData', getEmptyCompanyFormData())
    },
    async fetchCompany({state, commit}) {
      const companyUID = state.companyUID
      const company: FetchedDetailCompany = await axios
        .get(`api/v1/admin/companies/${companyUID}`)
        .then(response => response.data)
        .catch(error => console.log(error))

      const companyFormData = await getFormattedCompanyData(company)

      commit('setCompanyFormData', companyFormData)
    },
    async saveModelForm({state, commit, dispatch}) {
      let company: FetchedDetailCompany
      // Set ModelIsSaving
      commit('setModelIsSaving', true)
      // PrepareData
      const companyData: FormattedDetailCompany = state.companyFormData
      const preparedCompanyData = await getCompanyDataToRequest(companyData)
      // CreateDataObject
      const formData = getCompanyFormData(preparedCompanyData)
      // If NewModel => POST Request
      try {
        if (state.isNewModel) {
          company = await axios
            .post('api/v1/admin/companies/', formData)
            .then(response => {
              commit('setCompanyUID', response.data.uid)
              toast.success('Company is successfully created')
              return response.data
            })
            .catch(error => dispatch('catchAxiosError', error))
        }
        // If OldModel => PATCH Request
        else {
          const companyUID = state.companyUID
          company = await axios
            .patch(`api/v1/admin/companies/${companyUID}/`, formData)
            .then(response => {
              commit('setCompanyUID', response.data.uid)
              toast.success('Company is successfully saved')
              return response.data
            })
            .catch(error => dispatch('catchAxiosError', error))
        }
        const companyFormData = await getFormattedCompanyData(company)

        commit('setEditModeActivated', false)
        commit('setCompanyFormData', companyFormData)
        commit('setIsNewModel', false)

      } finally {
        // Reset ModelIsSaving
        commit('setModelIsSaving', false)
      }

      // Reset ModelIsSaving
      commit('setModelIsSaving', false)
    },
    async catchAxiosError({state, commit}, error) {
      // client received an error response (5xx, 4xx)
      if (error.response) {
        console.log(error)
        toast.error('Something was wrong... Please reload page')
        // client never received a response, or request never left
      } else if (error.request) {
        console.log(error)
        toast.error('Something was wrong... Please reload page')
        // anything else
      } else {
        console.log(error)
        toast.error('Something was wrong... Please reload page')
      }
    },
  },
  namespaced: true,
} as Module<any, any>


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

const getCompanyFormData = (object: any) => Object.keys(object).reduce((formData, key) => {
  if (key === 'logo' && typeof object[key] === 'object') {
    // https://stackoverflow.com/questions/63230458/django-rest-framework-doesnt-accept-blob-picture-file-file-extension-is-not
    formData.append(key, object[key], 'logo.png')
    return formData
  }

  formData.append(key, object[key])
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
    founded: company.year_founded || '',
  } as FormattedDetailCompany
}

const getCompanyDataToRequest = async (companyData: FormattedDetailCompany): Promise<CompanyDataToRequest> => {
  return {
    ticker: companyData.ticker.trim().toUpperCase(),
    slug: companyData.slug.trim(),
    uid: companyData.uid.trim(),
    title: companyData.companyName.trim(),
    short_title: companyData.shortCompanyName.trim(),
    short_title_genitive: companyData.shortCompanyNameGenitive.trim(),
    description: companyData.description.trim(),
    short_description: companyData.shortDescription.trim(),
    city: companyData.city.trim(),
    country_name_iso: companyData.country.slug,
    market_slug: companyData.market.slug,
    sector_slug: companyData.sector.slug,
    industry_slug: companyData.industry.slug,
    is_visible: companyData.isVisible,
    logo: companyData.logo,
    is_fund: companyData.isFund,
    website: companyData.website.trim(),
    year_founded: companyData.founded.trim(),
  }
}
