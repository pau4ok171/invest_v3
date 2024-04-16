import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from "axios";
import Vintersection from "@/directives/Vintersection";
import HighchartsVue from 'highcharts-vue';
import Highcharts from 'highcharts'
import StockChart from 'highcharts/modules/stock';
import highchartsMore from 'highcharts/highcharts-more'
import loadSolidGauge from 'highcharts/modules/solid-gauge'

axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)

app.directive('intersection', Vintersection)

highchartsMore(Highcharts)
loadSolidGauge(Highcharts)
StockChart(Highcharts)

Highcharts.Templating.helpers.abs = value => Math.abs(value);

Highcharts.setOptions({
    lang: {
        rangeSelectorZoom: ''
    }
});

app
    .use(router)
    .use(store)
    .use(axios)
    .use(HighchartsVue, {tagName: 'charts'})
    .mount('#app')
