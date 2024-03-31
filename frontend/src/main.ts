import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from "axios"
import Vintersection from "@/directives/Vintersection";

axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)

app.directive('intersection', Vintersection)

app
    .use(router)
    .use(store)
    .use(axios)
    .mount('#app')
