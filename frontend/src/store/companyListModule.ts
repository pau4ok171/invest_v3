import axios from "axios";
import store from "@/store";
import {toast} from "vue3-toastify";

export const companyListModule = {
  state: () => ({
    pageIsReady: false,
    companies: [],
    filters: {
        country: [],
        sector: [],
      },
    active_filters: {
        country: {title: '', slug: ''},
        sector: {title: '', slug: ''},
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
      return state.companies.reduce((prev, cur) => prev.updated > cur.updated ? prev : cur).updated
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
    async fetchCompanies({state, commit}) {
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
    async fetchFilters({state, commit}) {
      await axios
        .get('/api/v1/invest/filters')
        .then(response => {
          state.filters.country = [{title: 'Global', slug: 'global', required: true}, ...response.data.filters.country]
          state.filters.sector = [{title: 'Any', slug: 'any', required: true}, ...response.data.filters.sector]
          state.active_filters.country = state.filters.country[0]
          state.active_filters.sector = state.filters.sector[0]
        })
        .catch(error => console.log(error))
    },
    async fetchFiltersByCountry({state, commit}) {
      await axios
        .get(`api/v1/invest/filters/sector/${state.active_filters.country.slug}`)
        .then(response => {
          state.filters.sector = [{title: 'Any', slug: 'any', required: true}, ...response.data.filters.sector]
        })
        .catch(error => console.log(error))
    },
    async fetchNewCompanies({state, commit, dispatch}) {
      state.next_url = `/api/v1/invest/companies/?country=${state.active_filters.country.slug}&sector=${state.active_filters.sector.slug}`
      state.companies = []
      dispatch('fetchCompanies')
      dispatch('fetchFiltersByCountry')
    },
    async changeFilter({state, commit, dispatch}, args) {
      if (args.filter_name === 'country') {
        state.active_filters.sector = state.filters.sector[0]
      }
      state.active_filters[`${args.filter_name}`] = args.object
      dispatch('fetchNewCompanies')
    },
    async toggleToWatchlist({state, commit, dispatch}, object) {
      const formData = new FormData()
      Object.entries({
          uid: object.uid,
      }).forEach(([key, val]) => formData.append(key, val))

      if (object.is_watchlisted) {
        await axios
          .delete('/api/v1/invest/toggle_to_watchlist/', {data: formData})
          .then(() => toast.success(`Company ${object.ticker.toUpperCase()} was removed from watchlist`))
          .catch(error => {
            console.log(error)
            toast.error('Something was wrong...')
          })
      } else {
        await axios
          .patch('/api/v1/invest/toggle_to_watchlist/', formData)
          .then(() => toast.success(`Company ${object.ticker.toUpperCase()} was added to watchlist`))
          .catch(error=> {
            console.log(error)
            toast.error('Something was wrong...')
          })
      }
      state.companies.forEach((c: Object) => {
        if (c.uid === object.uid) {
          object.is_watchlisted = !object.is_watchlisted
        }
      })
    }
  },
  namespaced: true,
}