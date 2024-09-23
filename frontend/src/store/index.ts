import {createStore} from "vuex";
import {companyDetailModule} from "@/store/modules/companyDetailModule";
import {companyListModule} from "@/store/modules/companyListModule";
import {authModule} from "@/store/modules/authModule";

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
    authModule: authModule,
    companyList: companyListModule,
    companyDetail: companyDetailModule,
  },
})

export default store
