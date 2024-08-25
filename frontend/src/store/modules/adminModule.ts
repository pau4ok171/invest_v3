import type {Module} from "vuex";
import type {
  FetchedDetailCompany,
  FormattedCountry,
  FormattedDetailCompany,
  FormattedIndustry,
  FormattedMarket,
  FormattedSector,
  FormattedUser,
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
    previousCompanyFormData: getPreviousCompanyFormData(),
    // MODEL
    modelIsSaving: false,
    editModeActivated: false,
    isNewModel: false,
    modelWasModified: false,
  }),
  getters: {
    getCompanyUID(state) {
      return state.companyUID
    },
    getEditModeActivated(state) {
      return state.editModeActivated
    },
    getModelWasModified(state) {
      return Object.values({...state.previousCompanyFormData}).some((v: any) => v.wasModified)
    },
    getPreviousCompanyFormData(state) {
      return state.previousCompanyFormData
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
    setPreviousCompanyFormData(state, payload: FormattedDetailCompany) {
      state.previousCompanyFormData = payload
    },
    setModelIsSaving(state, payload: boolean) {
      state.modelIsSaving = payload
    },
    setModelWasModified(state, payload: boolean) {
      state.modelWasModified = payload
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
      state.companyFormData.shortDescription = payload
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
    async initAdminStore({commit}) {
      commit('setCompanyFormData', getEmptyCompanyFormData())
      commit('setPreviousCompanyFormData', getPreviousCompanyFormData())
    },
    async deleteModelData({commit}) {
      commit('setCompanyUID', '')
      commit('setCompanyFormData', getEmptyCompanyFormData())
      commit('setPreviousCompanyFormData', getPreviousCompanyFormData())
      commit('setIsNewModel', false)
    },
    async fetchCompany({state, commit}) {
      const companyUID = state.companyUID
      const company: FetchedDetailCompany = await axios
        .get(`api/v1/admin/companies/${companyUID}/`)
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
      const preparedCompanyData = await getCompanyDataToRequest(companyData, state.previousCompanyFormData)
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
        commit('setPreviousCompanyFormData', getPreviousCompanyFormData())
        commit('setIsNewModel', false)
        window.scrollTo({top: 0, behavior: 'smooth'})
      } finally {
        // Reset ModelIsSaving
        commit('setModelIsSaving', false)
      }
    },
    async deleteModel({state, commit, dispatch}) {
      // Get Company UID
      const companyUID = state.companyUID
      // Send DELETE Request
      try {
        await axios
            .delete(`api/v1/admin/companies/${companyUID}/`)
            .then(async r => {
              // Open Models Component
              commit('setActiveComponent', 'AdminModels')
              // Notify Client
              toast.success('Company is successfully deleted')
            })
            .catch(e => console.log(e))
      }
      catch (e) {
        console.log(e)
      }
    },
    async catchAxiosError({state, commit}, error) {
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

const getPreviousCompanyFormData = (company: FormattedDetailCompany|undefined = undefined) => {
  return Object.entries(company || getEmptyCompanyFormData()).reduce((obj: {[name: string]: Object}, [k, v]) => {
    obj[k] = {value: v, wasModified: false}
    return obj
  }, {})
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

const getCompanyDataToRequest = async (companyData: FormattedDetailCompany, previousCompanyData: any): Promise<{ [p: string]: any }> => {
  const companyDataToRequest: { [name: string]: any } = {
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
      .filter(k => companyDataToRequest[k] !== null)
      .reduce((a, k) => ({...a, [k]: companyDataToRequest[k]}), {})
}
