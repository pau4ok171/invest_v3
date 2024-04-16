import axios from "axios";

export const companyDetailModule = {
  state: () => ({
    companyPriceData: [],
    priceChartDataisLoading: true
  }),
  getters: {
    companyPriceData(state) {
      return state.companyPriceData.map(F => [F['time'], F['close']])
    }
  },
  mutations: {
    getCompanyPriceData(state, priceData) {
      state.companyPriceData = priceData
    },
    setPriceChartDataIsLoading(state, status: Boolean) {
      state.priceChartDataisLoading = status
    }
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
  },
  namespaced: true,
}