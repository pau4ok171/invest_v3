import type {Module} from "vuex";

export const adminModule = {
  state: () => ({
      companyUID: '',
  }),
  getters: {},
  mutations: {
      setCompanyUID(state, payload: string) {
        state.companyUID = payload
      },
  },
  actions: {},
  namespaced: true,
} as Module<any, any>