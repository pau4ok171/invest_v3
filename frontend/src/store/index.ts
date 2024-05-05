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
            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
            } else {
                state.token = ''
                state.isAuthenticated = false
            }
        },
        setIsLoading(state, status: Boolean) {
          state.isLoading = status
        },
        setToken(state, token) {
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
    namespaced: true,
})

export default store
