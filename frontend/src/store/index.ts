import {createStore} from "vuex";
import {companyDetailModule} from "@/store/modules/companyDetailModule";
import {companyListModule} from "@/store/modules/companyListModule";
import {authModule} from "@/store/modules/authModule";
import {adminModule} from "@/store/modules/adminModule";

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
    adminModule: adminModule,
    authModule: authModule,
    companyList: companyListModule,
    companyDetail: companyDetailModule,
  },
})

export default store
