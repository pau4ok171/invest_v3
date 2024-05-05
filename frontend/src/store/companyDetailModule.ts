import axios from "axios";
import {toast} from "vue3-toastify";

export const companyDetailModule = {
  state: () => ({
    companyPriceData: [],
    company: {},
    portfolios: [],
    notes: [],
    note: {},
    priceChartDataisLoading: true,
    // NotesModalMenu
    notesModalMenuIsOpen: false,
    notesModalMenuIsLateral: true,
    watchlistIsLoading: false,
    portfolioIsLoading: false,
    // NotesModalMenu
    noteSavedContent: '',
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
    getCompany(state) {
      return state.company
    },
    getPortfolios(state) {
      return state.portfolios
    },
    getNotes(state) {
      return state.notes
    },
    getNote(state) {
      return state.note
    },
    getNoteSavedContent(state) {
      return state.noteSavedContent
    },
    getWatchlistIsLoading(state) {
      return state.watchlistIsLoading
    },
    getPortfolioIsLoading(state) {
      return state.portfolioIsLoading
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
    setNotes(state, notes) {
      state.notes = notes
    },
    setNote(state, note) {
      state.note = note
    },
    addNewPortfolio(state, portfolio) {
      state.portfolios.push(portfolio)
    },
    addNewNote(state, note) {
      state.notes.push(note)
    },
    setNoteSavedContent(state, savedContent) {
      state.noteSavedContent = savedContent
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
    setWatchlistIsLoading(state, status: Boolean) {
      state.watchlistIsLoading = status
    },
    setPortfolioIsLoading(state, status: Boolean) {
      state.portfolioIsLoading = status
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
    updateNotesWithNewNote({state, commit}, note) {
      let notes: Array<Object> = []
      state.notes.forEach((n: {id: Number}) => {
        if (n.id === note.id) {
          notes.push(note)
        } else {
          notes.push(n)
        }
      })
      commit('setNotes', notes)
    },
    async fetchPriceData({state, commit}, slug) {
      await axios
        .get(`api/v1/invest/price_data/${slug}`)
        .then(response => {
          commit("getCompanyPriceData", response.data)
          commit("setPriceChartDataIsLoading", false)
        })
    },
    async toggleToWatchlist({state, commit}) {
      commit('setWatchlistIsLoading', true)

      const formData = new FormData()
      Object.entries({uid: state.company.uid}).forEach(([key, val]) => {
        formData.append(key, val)
      })

      if (state.company.is_watchlisted) {
        await axios
          .delete('/api/v1/invest/toggle_to_watchlist/', {data: formData})
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
          .patch('/api/v1/invest/toggle_to_watchlist/', formData)
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
    async deleteNote({state, commit}, note) {
      await axios
        .delete(`/api/v1/notes/${note.id}`)
        .then(response => {
          commit('setNotes', [...state.notes].filter(n => n.id !== note.id))
        })
        .catch(error => {
          console.log(error)
          toast.error('Something was wrong...')
          })
    },
  },
  namespaced: true,
}