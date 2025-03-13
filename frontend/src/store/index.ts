import { createStore } from 'vuex'
import { companyDetailModule } from '@/store/modules/companyDetailModule'

const store = createStore({
  state: () => ({
    isLoading: false,
    lateralMenuIsOpen: false,
  }),
  mutations: {
    setIsLoading(state, status: boolean) {
      state.isLoading = status
    },
    setLateralMenuIsOpen(state, status: boolean) {
      state.lateralMenuIsOpen = status
    },
  },
  modules: {
    companyDetail: companyDetailModule,
  },
})

export default store
