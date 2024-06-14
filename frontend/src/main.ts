import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from "axios";
import VueAxios from "vue-axios";

import Vue3Toastify, {toast, type ToastContainerOptions} from "vue3-toastify";
import 'vue3-toastify/dist/index.css';

import VueTippy from 'vue-tippy';
import 'tippy.js/dist/tippy.css';

import Vintersection from "@/directives/Vintersection";

import HighchartsVue from 'highcharts-vue';
import Highcharts from 'highcharts'
import StockChart from 'highcharts/modules/stock';
import highchartsMore from 'highcharts/highcharts-more'
import loadSolidGauge from 'highcharts/modules/solid-gauge'
import {defaultChartOpts} from "@/components/charts/DefaultChartOpts";

axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)
const hc = Highcharts as any

app.directive('intersection', Vintersection)

highchartsMore(hc)
loadSolidGauge(hc)
StockChart(hc)

hc.Templating.helpers.abs = (value: number) => Math.abs(value);

Highcharts.setOptions({
  ...defaultChartOpts
});

app
  .use(router)
  .use(store)
  .use(VueAxios, axios)
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
  .use(
    VueTippy,
    {
      directive: 'tippy',
      component: 'tippy',
      componentSingleton: 'tippy-singleton',
      defaultProps: {
        placement: 'top',
        allowHTML: false,
        followCursor: 'horizontal',
      }
    }
  )
  .mount('#app')
