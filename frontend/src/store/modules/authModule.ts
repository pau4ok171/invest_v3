import type {Module} from "vuex";
import axios from "axios";

export const authModule = {
  state: () => ({
    isAuthenticated: false,
    userInfo: {},
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
    setUserInfo(state, payload: Object) {
      state.userInfo = payload
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
    },
  },
  actions: {
    async fetchUserInfo({state, commit}) {
      await axios
          .get('api/v1/admin/users/')
          .then(r => commit('setUserInfo', r.data))
          .catch(e => console.log(e))
    },
  },
  namespaced: true,
} as Module<any, any>