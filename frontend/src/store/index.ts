import {createStore} from "vuex";
import {companyDetailModule} from "@/store/companyDetailModule";
import {companyListModule} from "@/store/companyListModule";

const store = createStore({
  state: () => ({
    isAuthenticated: false,
    isLoading: false,
    token: '',
  }),
  getters: {
    getIsAuthenticated(state) {
      return state.isAuthenticated
    },
  },
  mutations: {
    initializeStore(state) {
      const token: string | null = localStorage.getItem('token')
      if (token) {
        state.token = token
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    setIsLoading(state, status: boolean) {
      state.isLoading = status
    },
    setToken(state, token: string) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
    },
  },
  actions: {},
  modules: {
    companyList: companyListModule,
    companyDetail: companyDetailModule,
  },
})

export default store
