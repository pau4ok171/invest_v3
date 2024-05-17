import axios from "axios";
import store from "@/store";
import {toast} from "vue3-toastify";
import type {Module} from "vuex";
import type {Country, Currency, ListCompany, Sector} from "@/types/invest";

const defaultCurrency: Currency = {
    id: 0,
    name: '',
    name_iso: '',
    symbol: '',
}
const defaultCountry: Country = {
    id: 0,
    title: '',
    slug: '',
    currency: defaultCurrency,
    markets: [],
}
const defaultSector: Sector = {
    main_header: '',
    slug: '',
    title: '',
}

export const companyListModule = {
  state: () => ({
    pageIsReady: false,
    companies: [] as Array<ListCompany>,
    filters: {
        country: [] as Array<Country>,
        sector: [] as Array<Sector>,
      },
    active_filters: {
        country: defaultCountry,
        sector: defaultSector,
      },
    next_url: '/api/v1/invest/companies',
    totalCompaniesLength: 0,
  }),
  getters: {
    getPageIsReady(state) {
      return state.pageIsReady
    },
    getCompanies(state) {
      return state.companies
    },
    getActiveFilters(state) {
      return state.active_filters
    },
    getFilters(state) {
      return state.filters
    },
    getListUpdated(state) {
      return state.companies.reduce((prev: ListCompany, cur: ListCompany) => prev.updated > cur.updated ? prev : cur, 0).updated
    },
    getTotalCompaniesLength(state) {
      return state.totalCompaniesLength
    },
    getNextURL(state) {
      return state.next_url
    },
  },
  mutations: {
    setPageIsReady(state, status) {
      state.pageIsReady = status
    },
  },
  actions: {
    changeFilter: async function ({state, commit, dispatch}, args) {
      if (args.filter_name === 'country') {
        state.active_filters.sector = state.filters.sector[0]
      }
      state.active_filters[`${args.filter_name}`] = args.object
      await dispatch('fetchNewCompanies')
    },
    fetchCompanies: async function ({state}) {
      store.commit('setIsLoading', true)

      await axios
          .get(state.next_url)
          .then(response => {
            state.companies = [...state.companies, ...response.data.results]
            state.next_url = response.data.next
            state.totalCompaniesLength = response.data.count
          })
          .catch(error => console.log(error))

      store.commit('setIsLoading', false)
    },
    fetchFilters: async function ({state}) {
      await axios
          .get('/api/v1/invest/filters')
          .then(response => {
            state.filters.country = [{
              title: 'Global',
              slug: 'global',
              required: true
            }, ...response.data.filters.country]
            state.filters.sector = [{title: 'Any', slug: 'any', required: true}, ...response.data.filters.sector]
            state.active_filters.country = state.filters.country[0]
            state.active_filters.sector = state.filters.sector[0]
          })
          .catch(error => console.log(error))
    },
    fetchFiltersByCountry: async function ({state}) {
      await axios
          .get(`api/v1/invest/filters/sector/${state.active_filters.country.slug}`)
          .then(response => {
            state.filters.sector = [{title: 'Any', slug: 'any', required: true}, ...response.data.filters.sector]
          })
          .catch(error => console.log(error))
    },
    fetchNewCompanies: async function ({state, dispatch}) {
      state.next_url = `/api/v1/invest/companies/?country=${state.active_filters.country.slug}&sector=${state.active_filters.sector.slug}`
      state.companies = []
      await dispatch('fetchCompanies')
      await dispatch('fetchFiltersByCountry')
    },
    toggleToWatchlist: async function ({state, commit, dispatch}, company: ListCompany) {
      const formData = new FormData()
      const formDataPayload: Object = {
        uid: company.uid
      }
      Object.entries(formDataPayload).forEach(([key, val]) => formData.append(key, val))

      if (company.is_watchlisted) {
        await axios
            .delete('/api/v1/invest/toggle_to_watchlist/', {data: formData})
            .then(() => toast.success(`Company ${company.ticker.toUpperCase()} was removed from watchlist`))
            .catch(error => {
              console.log(error)
              toast.error('Something was wrong...')
            })
      } else {
        await axios
            .patch('/api/v1/invest/toggle_to_watchlist/', formData)
            .then(() => toast.success(`Company ${company.ticker.toUpperCase()} was added to watchlist`))
            .catch(error => {
              console.log(error)
              toast.error('Something was wrong...')
            })
      }
      state.companies.forEach((c: ListCompany) => {
        if (c.uid === company.uid) {
          company.is_watchlisted = !company.is_watchlisted
        }
      })
    }
  },
  namespaced: true,
} as Module<any, any>