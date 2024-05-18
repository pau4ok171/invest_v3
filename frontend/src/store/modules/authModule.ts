import type {Module} from "vuex";

export const authModule = {
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
      const token: String | null = localStorage.getItem('token')
      if (token) {
        state.token = token
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    setIsLoading(state, status: Boolean) {
      state.isLoading = status
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
  actions: {},
} as Module<any, any>