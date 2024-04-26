import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from "axios";

import Vue3Toastify, {toast, type ToastContainerOptions} from "vue3-toastify";
import 'vue3-toastify/dist/index.css';

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
  },
  accessibility: {
    enabled: false
  },
});

app
  .use(router)
  .use(store)
  .use(axios)
  .use(HighchartsVue, {tagName: 'charts'})
  .use(
    Vue3Toastify,
    {
      autoClose: 3000,
      position: toast.POSITION.BOTTOM_RIGHT,
      limit: 5,
      closeButton: false,
      transition: toast.TRANSITIONS.BOUNCE,
      style: {
        fontSize: '1.6rem',
      },
      theme: 'colored',
    } as ToastContainerOptions
  )
  .mount('#app')
