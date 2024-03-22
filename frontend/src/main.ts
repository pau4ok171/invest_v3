import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from "axios"

axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)

app.use(router, store, axios)

app.mount('#app')
