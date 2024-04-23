import axios from "axios";
import {toast} from "vue3-toastify";

export const companyDetailModule = {
  state: () => ({
    companyPriceData: [],
    company: {},
    portfolios: [],
    priceChartDataisLoading: true,
    // NotesModalMenu
    notesModalMenuIsOpen: false,
    notesModalMenuIsLateral: true,
    // PortfolioModalMenu
    portfolioModalMenuIsOpen: false,
    watchlistIsLoading: false,
    portfolioIsLoading: false,
    // AnalystsModalMenu
    analystsModalMenuIsOpen: false,
  }),
  getters: {
    companyPriceData(state) {
      return state.companyPriceData.map((F: {time: string, close: string}) => [F['time'], F['close']])
    },
    getNotesModalMenuIsActive(state) {
      return state.notesModalMenuIsOpen
    },
    getNotesModalMenuIsLateral(state) {
      return state.notesModalMenuIsLateral
    },
    getPortfolioModalMenuIsOpen(state) {
      return state.portfolioModalMenuIsOpen
    },
    getCompany(state) {
      return state.company
    },
    getPortfolios(state) {
      return state.portfolios
    },
    getWatchlistIsLoading(state) {
      return state.watchlistIsLoading
    },
    getPortfolioIsLoading(state) {
      return state.portfolioIsLoading
    },
    getAnalystsModalMenuIsOpen(state) {
      return state.analystsModalMenuIsOpen
    },
  },
  mutations: {
    getCompanyPriceData(state, priceData) {
      state.companyPriceData = priceData
    },
    setPriceChartDataIsLoading(state, status: Boolean) {
      state.priceChartDataisLoading = status
    },
    setCompany(state, company) {
      state.company = company
    },
    setPortfolios(state, portfolios) {
      state.portfolios = portfolios
    },
    addNewPortfolio(state, portfolio) {
      state.portfolios.push(portfolio)
    },
    setIsWatchlisted(state, status: Boolean) {
      state.company.is_watchlisted = status
    },
    setNotesModalMenuIsOpen(state, status: Boolean) {
      state.notesModalMenuIsOpen = status
    },
    setNotesModalMenuIsLateral(state, status: Boolean) {
      state.notesModalMenuIsLateral = status
    },
    setPortfolioModalMenuIsOpen(state, status: Boolean) {
      state.portfolioModalMenuIsOpen = status
    },
    setWatchlistIsLoading(state, status: Boolean) {
      state.watchlistIsLoading = status
    },
    setPortfolioIsLoading(state, status: Boolean) {
      state.portfolioIsLoading = status
    },
    setAnalystsModalMenuIsOpen(state, status: Boolean) {
      state.analystsModalMenuIsOpen = status
    },
  },
  actions: {
    updatePortfoliosWithNewPortfolio({state, commit}, portfolio) {
      let portfolios: Array<Object> = []
      state.portfolios.forEach((p: {id: Number}) => {
        if (p.id === portfolio.id) {
          portfolios.push(portfolio)
        } else {
          portfolios.push(p)
        }
      })
      commit('setPortfolios', portfolios)
    },
    async fetchPriceData({state, commit}, slug) {
      await axios
        .get(`invest/api/v1/price_chart/${slug}`)
        .then(response => {
          commit("getCompanyPriceData", response.data)
          commit("setPriceChartDataIsLoading", false)
        })
    },
    async toggleToWatchlist({state, commit}) {
      commit('setWatchlistIsLoading', true)
      const formData = {
        uid: state.company.uid
      }
      if (state.company.is_watchlisted) {
        await axios
          .delete('/invest/api/v1/toggle_to_watchlist/', {
            data: formData
          })
          .then(() => {
            commit('setIsWatchlisted', false)
            toast.success(`Company ${state.company.slug.toUpperCase()} was remove from watchlist`)
          })
          .catch(error => {
            console.log(error)
            toast.error('Something was wrong...')
          })
      } else {
        await axios
          .patch('/invest/api/v1/toggle_to_watchlist/', formData)
          .then(() => {
            commit('setIsWatchlisted', true)
            toast.success(`Company ${state.company.slug.toUpperCase()} was added to watchlist`)
          })
          .catch(error => {
            console.log(error)
            toast.error('Something was wrong...')
          })
      }
      commit('setWatchlistIsLoading', false)
    },
  },
  namespaced: true,
}