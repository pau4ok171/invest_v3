import {createStore} from "vuex";
import {companyDetailModule} from "@/store/modules/companyDetailModule";
import {companyListModule} from "@/store/modules/companyListModule";
import {authModule} from "@/store/modules/authModule";

const store = createStore({
  state: () => ({
    isLoading: false,
  }),
  mutations: {
    setIsLoading(state, status: Boolean) {
      state.isLoading = status
    },
  },
  modules: {
    authModule: authModule,
    companyList: companyListModule,
    companyDetail: companyDetailModule,
  },
})

export default store
