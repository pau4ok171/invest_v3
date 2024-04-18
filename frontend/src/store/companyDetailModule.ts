import axios from "axios";

export const companyDetailModule = {
  state: () => ({
    companyPriceData: [],
    company: {},
    priceChartDataisLoading: true,
    notesModalMenuIsOpen: false,
    notesModalMenuIsLateral: true,
  }),
  getters: {
    companyPriceData(state) {
      return state.companyPriceData.map(F => [F['time'], F['close']])
    },
    getNotesModalMenuIsActive(state) {
      return state.notesModalMenuIsOpen
    },
    getNotesModalMenuIsLateral(state) {
      return state.notesModalMenuIsLateral
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
    setIsWatchlisted(state, status: Boolean) {
      state.company.is_watchlisted = status
    },
    setNotesModalMenuIsOpen(state, status: Boolean) {
      state.notesModalMenuIsOpen = status
    },
    setNotesModalMenuIsLateral(state, status: Boolean) {
      state.notesModalMenuIsLateral = status
    },
  },
  actions: {
    async fetchPriceData({state, commit}, slug) {
      await axios
        .get(`invest/api/v1/price_chart/${slug}`)
        .then(response => {
          commit("getCompanyPriceData", response.data)
          commit("setPriceChartDataIsLoading", false)
        })
    },
    async toggleToWatchlist({state, commit}) {
      const formData = {
        uid: state.company.uid
      }
      if (state.company.is_watchlisted) {
        await axios
          .delete('/invest/api/v1/toggle_to_watchlist/', {
            data: formData
          })
          .then(response => commit('setIsWatchlisted', false))
          .catch(error => console.log(error))
      } else {
        await axios
          .patch('/invest/api/v1/toggle_to_watchlist/', formData)
          .then(response => commit('setIsWatchlisted', true))
          .catch(error => console.log(error))
      }
    },
  },
  namespaced: true,
}