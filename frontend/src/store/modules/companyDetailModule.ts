import axios from "axios";
import type {Module} from "vuex";
import {toast} from "vue3-toastify";
import type {
  Candle,
  Competitor,
  DetailCompany,
} from "@/types/invest";
import type {Statement} from "@/types/statements";
import type {Portfolio} from "@/types/portfolios"
import type {Note} from "@/types/notes";
import store from "@/store";

export const companyDetailModule = {
  state: () => ({
    pageIsReady: false,
    companyPriceData: [] as Array<Candle>,
    company: {} as DetailCompany,
    portfolios: [] as Array<Portfolio>,
    notes: [] as Array<Note>,
    statements: [] as Array<Statement>,
    snowflake: [] as Array<Number>,
    competitors: [] as Array<Competitor>,
    note: {} as Note,
    priceChartDataisLoading: true,
    // NotesModalMenu
    notesModalMenuIsOpen: false,
    notesModalMenuIsLateral: true,
    watchlistIsLoading: false,
    portfolioIsLoading: false,
    // NotesModalMenu
    noteSavedContent: '',
    // PageNotFound
    pageNotFound: false,
  }),
  getters: {
    getPageIsReady(state): boolean {
      return state.pageIsReady
    },
    companyPriceData(state): Array<Candle> {
      return state.companyPriceData.map((F: {time: string, close: string}) => [F['time'], F['close']])
    },
    getNotesModalMenuIsActive(state): boolean {
      return state.notesModalMenuIsOpen
    },
    getNotesModalMenuIsLateral(state) {
      return state.notesModalMenuIsLateral
    },
    getCompany(state): DetailCompany {
      return state.company
    },
    getSnowflake(stake) {
      return stake.snowflake
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
    getStatements(state) {
      return state.statements
    },
    getCompetitors(state) {
      return state.competitors
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
    getPageNotFound(state) {
      return state.pageNotFound
    },
  },
  mutations: {
    setPageIsReady(state, status: Boolean) {
      state.pageIsReady = status
    },
    getCompanyPriceData(state, priceData: Array<Candle>) {
      state.companyPriceData = priceData
    },
    setPriceChartDataIsLoading(state, status: Boolean) {
      state.priceChartDataisLoading = status
    },
    setCompany(state, company) {
      state.company = company
    },
    setPortfolios(state, portfolios: Array<Portfolio>) {
      state.portfolios = portfolios
    },
    setNotes(state, notes: Array<Note>) {
      state.notes = notes
    },
    setNote(state, note: Note) {
      state.note = note
    },
    setStatements(state, statements: Array<Statement>) {
      state.statements = statements
    },
    setSnowflake(state, snowflake: Array<Number>) {
      state.snowflake = snowflake
    },
    setCompetitors(state, competitors: Array<Competitor>) {
      state.competitors = competitors
    },
    addNewPortfolio(state, portfolio: Portfolio) {
      state.portfolios.push(portfolio)
    },
    addNewNote(state, note: Note) {
      state.notes.push(note)
    },
    setNoteSavedContent(state, savedContent: String) {
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
    updatePortfoliosWithNewPortfolio({state, commit}, portfolio: Portfolio) {
      let portfolios: Array<Portfolio> = []
      state.portfolios.forEach((p: Portfolio) => {
        if (p.id === portfolio.id) {
          portfolios.push(portfolio)
        } else {
          portfolios.push(p)
        }
      })
      commit('setPortfolios', portfolios)
    },
    updateNotesWithNewNote({state, commit}, note: Note) {
      let notes: Array<Note> = []
      state.notes.forEach((n: Note) => {
        if (n.id === note.id) {
          notes.push(note)
        } else {
          notes.push(n)
        }
      })
      commit('setNotes', notes)
    },
    async fetchPriceData({state, commit, dispatch}, company_slug: String) {
      await axios
        .get(`api/v1/invest/price_data/${company_slug}`)
        .then(response => {
          commit("getCompanyPriceData", response.data)
          commit("setPriceChartDataIsLoading", false)
        })
        .catch(error => dispatch('catchAxiosError', error))
    },
    async fetchCompany({state, commit, dispatch}, company_slug: String) {
      store.commit('setIsLoading', true)

      await axios
        .get(`api/v1/invest/companies/${company_slug}`)
        .then(response => {
          const company: DetailCompany = response.data.company
          const portfolios: Array<Portfolio> = response.data.portfolios
          const notes: Array<Note> = response.data.notes
          const statements: Array<Statement> = response.data.statements
          const snowflake: Array<Number> = Object.values(response.data.snowflake as Array<Number>)
          const competitors: Array<Competitor> = response.data.peers

          commit('setCompany', company)
          commit('setPortfolios', portfolios)
          commit('setNotes', notes)
          commit('setStatements', statements)
          commit('setSnowflake', snowflake)
          commit('setCompetitors', competitors)
        })
        .catch(error => dispatch('catchAxiosError', error))

        store.commit('setIsLoading', false)
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
    async deleteNote({state, commit}, note: Note) {
      await axios
        .delete(`/api/v1/notes/${note.id}`)
        .then(() => {
          commit('setNotes', [...state.notes].filter(n => n.id !== note.id))
        })
        .catch(error => {
          console.log(error)
          toast.error('Something was wrong...')
          })
    },
    async catchAxiosError({state, commit}, error) {
      // client received an error response (5xx, 4xx)
      if (error.response) {
        if (error.response.status === 404) {
          state.pageNotFound = true
        }
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