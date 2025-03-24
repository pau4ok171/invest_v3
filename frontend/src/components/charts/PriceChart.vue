<script setup lang="ts">
// Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import FetchingData from '@/components/charts/FetchingData.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useRoute } from 'vue-router'

// Utilities
import { computed, onUnmounted, ref, shallowRef, watch } from 'vue'
import { chartOpts as _chartOpts } from '@/components/charts/priceChartOpts'
import { DateTime } from 'ts-luxon'

// Types
import type { Chart } from 'highcharts-vue'

type AllowedPeriod = '1M' | '3M' | '1Y' | '3Y' | '5Y' | 'Max'

interface Tab {
  value: AllowedPeriod
  min: Readonly<DateTime>
}
type Tablist = { [value: string]: Tab }

const companyDetailStore = useCompanyDetailStore()
const company = computed(() => companyDetailStore.company)
const priceData = computed(() => companyDetailStore.chartPriceData)

const route = useRoute()

const chartEl = ref<typeof Chart>()
const chartOpts = ref(_chartOpts)

const current = shallowRef('1Y')
const intervalId = shallowRef(-1)
const tablist = ref<Tablist>({
  M1: { value: '1M', min: DateTime.now().minus({ months: 1 }) },
  M3: { value: '3M', min: DateTime.now().minus({ months: 3 }) },
  Y1: { value: '1Y', min: DateTime.now().minus({ years: 1 }) },
  Y3: { value: '3Y', min: DateTime.now().minus({ years: 3 }) },
  Y5: { value: '5Y', min: DateTime.now().minus({ years: 5 }) },
  MAX: { value: 'Max', min: DateTime.now().minus({ years: 50 }) },
})

function changeZoom(tab: Tab) {
  current.value = tab.value
  const chart = chartEl?.value?.chart
  const chartMax = chart.xAxis[1].max || DateTime.now().ts
  chart.xAxis[0].setExtremes(tab.min.ts, chartMax)
}

function afterCreate(chart: any) {
  chartOpts.value.series[0].data = priceData.value as []
  const chartMax = chart.xAxis[1].max || DateTime.now().ts
  chart.xAxis[0].setExtremes(tablist.value['Y1'].min.ts, chartMax)
  setChartDataUpdateInterval()
}

function setChartDataUpdateInterval() {
  const companySlug = route.params.companySlug as string
  intervalId.value = setInterval(
    async () => await companyDetailStore.fetchPriceData(companySlug),
    1000 * 60 * 5
  ) // 5min
}

onUnmounted(() => {
  if (intervalId.value) {
    window.clearInterval(intervalId.value)
  }
})

watch(
  () => priceData.value,
  () => {
    chartOpts.value.series[0].data = priceData.value as []
  },
  { deep: true }
)
</script>

<template>
  <div class="detail-price-chart__wrapper">
    <FetchingData v-if="companyDetailStore.fetchingCompany" />

    <template v-else>
      <div role="tablist" class="detail-price-chart__tablist">
        <base-button
          v-for="tab in tablist"
          :key="tab.value"
          :text="tab.value"
          variant="text"
          :disabled="tab.value === current"
          @click="changeZoom(tab)"
        />
      </div>
      <div class="detail-price-chart">
        <charts
          ref="chartEl"
          :constructorType="'stockChart'"
          :options="chartOpts"
          :callback="afterCreate"
        />
      </div>
    </template>
  </div>
</template>

<style lang="scss">
.detail-price-chart__wrapper {
  height: 430px;
}
.detail-price-chart__tablist {
  display: grid;
  grid-template-columns: repeat(6, auto);
}
.detail-price-chart svg {
  width: 100%;
  height: 100%;
  fill: none;
}
.detail-price-chart .highcharts-button-box {
  overflow: visible;
  font: inherit;
  -webkit-font-smoothing: inherit;
  letter-spacing: inherit;
  background-color: transparent;
  cursor: pointer;
  position: relative;
  display: block;
  width: 100%;
  height: auto;
  border-top: 1px solid transparent;
  border-left: 1px solid transparent;
  border-right: 1px solid transparent;
  padding: 4px;

  border-radius: 4px;
}
.detail-price-chart .highcharts-button > text,
#price-history-chart .highcharts-label > text,
#price-history-chart .highcharts-tooltip-box > text {
  font-size: 1.3rem !important;
  line-height: 1.5 !important;
  font-weight: 500 !important;
  fill: rgba(255, 255, 255, 0.3) !important;
}
.detail-price-chart .highcharts-button-pressed > text {
  fill: var(--blue) !important;
}
.detail-price-chart .highcharts-button-hover > text {
  fill: var(--blue) !important;
}
.detail-price-chart .price-history-chart-point-box__date {
  fill: rgba(255, 255, 255, 0.7);
  line-height: 1.4;
}
.detail-price-chart .price-history-chart-point-box__price {
  fill: #fff;
  font-weight: 900;
}
.detail-price-chart .highcharts-navigator-mask-inside {
  cursor: grab !important;
  rx: 4;
  ry: 4;
  stroke-width: 1;
  stroke: rgb(35, 148, 223);
}
.detail-price-chart .highcharts-navigator-mask-outside {
  fill: rgba(21, 27, 36, 0.3);
  rx: 4;
  ry: 4;
}
</style>
