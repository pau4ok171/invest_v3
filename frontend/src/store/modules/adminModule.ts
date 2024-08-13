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

export const adminModule = {
  state: () => ({
      companyUID: '',
      companyFormData: getEmptyCompanyFormData(),
  }),
  getters: {
    getCompanyUID(state) {
      return state.companyUID
    },
  },
  mutations: {
      setCompanyUID(state, payload: string) {
        state.companyUID = payload
      },
      setCompanyFormData(state, payload: FormattedDetailCompany) {
        state.companyFormData = payload
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
      let file = await fetch(company.logo).then(r => r.blob()).then(blobFile => new File([blobFile], "CompanyLogo", { type: "image/png" }))
      const companyFormData: FormattedDetailCompany = {
        ticker: company.ticker,
        slug: company.slug,
        uid: company.uid,
        companyName: company.title,
        shortCompanyName: company.short_title,
        shortCompanyNameGenitive: company.short_title_genitive,
        description: company.description,
        shortDescription: company.short_description,
        city: company.city,
        country: {
          name: company.country.name,
          slug: company.country.name_iso,
          key: company.country.id,
          currency: {
            name: company.country.currency.name,
            symbol: company.country.currency.symbol
          },
          flagURL: company.country.flag_url
        },
        market: {
          name: company.market.title,
          slug: company.market.slug,
          key: company.market.country
        },
        sector: {
          name: company.sector.title,
          slug: company.sector.slug,
          key: company.sector.id
        },
        industry: {
          name: company.industry.title,
          slug: company.industry.slug,
          key: company.industry.sector
        },
        created: company.created,
        updated: company.updated,
        createdBy: {
          firstName: company.created_by.first_name,
          lastName: company.created_by.last_name,
        },
        updatedBy: {
          firstName: company.updated_by.first_name,
          lastName: company.updated_by.last_name,
        },
        isVisible: company.is_visible,
        logo: file,
        isFund: company.is_fund,
        website: company.website,
        founded: String(company.year_founded),
      }
      commit('setCompanyFormData', companyFormData)
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