import { createApp } from "vue";
import {createStore, Store} from "vuex";

const store = createStore({
    state: {
        authModalMenuIsActive: false,
        isAuthenticated: false,
        isLoading: false,
        token: '',
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
        setAuthModalMenuIsActive(state, status: Boolean) {
            state.authModalMenuIsActive = status
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
    actions: {
    },
    modules: {
    }
})

export default store
