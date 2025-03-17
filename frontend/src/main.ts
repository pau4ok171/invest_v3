import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from '@/axios'
import VueAxios from 'vue-axios'

import Vue3Toastify, { toast, type ToastContainerOptions } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import VueTippy, { directive } from 'vue-tippy'
import 'tippy.js/dist/tippy.css'

import Vintersection from '@/directives/Vintersection'
import Vdebounce from '@/directives/Vdebounce'

import { createPinia } from 'pinia'

import HighchartsVue from 'highcharts-vue'
import Highcharts from 'highcharts'
import 'highcharts/modules/stock'
import 'highcharts/highcharts-more'
import 'highcharts/modules/solid-gauge'
import { defaultChartOpts } from '@/components/charts/DefaultChartOpts'
import visagiste from '@/plugins/visagiste'

const app = createApp(App)
const pinia = createPinia()
const hc = Highcharts as any

app.directive('intersection', Vintersection)
app.directive('debounce', Vdebounce)
app.directive('tippy', directive)

hc.Templating.helpers.abs = (value: number) => Math.abs(value)

Highcharts.setOptions({
  ...defaultChartOpts,
})

app
  .use(router)
  .use(store)
  .use(pinia)
  .use(VueAxios, axios)
  .use(HighchartsVue, { tagName: 'charts' })
  .use(Vue3Toastify, {
    autoClose: 3000,
    position: toast.POSITION.BOTTOM_RIGHT,
    limit: 5,
    closeButton: false,
    transition: toast.TRANSITIONS.BOUNCE,
    style: {
      fontSize: '1rem',
    },
    theme: 'colored',
  } as ToastContainerOptions)
  .use(VueTippy, {
    directive: 'tippy',
    component: 'tippy',
    componentSingleton: 'tippy-singleton',
    defaultProps: {
      placement: 'top',
      allowHTML: false,
      followCursor: 'horizontal',
    },
  })
  .use(visagiste)
  .mount('#app')
