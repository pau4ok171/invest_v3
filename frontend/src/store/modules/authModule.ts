import type {Module} from "vuex";

export const authModule = {
  state: () => ({
    isAuthenticated: false,
    token: '',
  }),
  getters: {
    getIsAuthenticated(state) {
      return state.isAuthenticated
    },
    getToken(state) {
      return state.token
    },
  },
  mutations: {
    initializeAuth(state) {
      const token: String | null = localStorage.getItem('token')
      if (token) {
        state.token = token
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    setToken(state, token: String) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
    },
  },
  actions: {

  },
  namespaced: true,
} as Module<any, any>