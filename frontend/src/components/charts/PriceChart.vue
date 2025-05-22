<script setup lang="ts">
// Components
import FetchingData from '@/components/charts/FetchingData.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref, shallowRef, watch } from 'vue'
import Highcharts from 'highcharts'
import { debounce } from 'lodash'
import { DateTime } from 'ts-luxon'

// Types
import type { Options, StockChart } from 'highcharts'

type AllowedPeriod = '1M' | '3M' | '1Y' | '3Y' | '5Y' | 'Max'

interface Tab {
  value: AllowedPeriod
  title: string
  min: DateTime
}
type Tablist = Record<string, Tab>

const companyDetailStore = useCompanyDetailStore()
const company = computed(() => companyDetailStore.company)
const priceData = computed(() => companyDetailStore.chartPriceData)
const { t, locale } = useI18n()
const chartRef = ref<{ chart: StockChart }>()

const current = shallowRef<Array<AllowedPeriod>>(['1Y'])
const tablist = computed<Tablist>(() => ({
  M1: {
    value: '1M',
    title: t('date.shortMonths', 1),
    min: DateTime.now().minus({ months: 1 }),
  },
  M3: {
    value: '3M',
    title: t('date.shortMonths', 3),
    min: DateTime.now().minus({ months: 3 }),
  },
  Y1: {
    value: '1Y',
    title: t('date.shortYears', 1),
    min: DateTime.now().minus({ years: 1 }),
  },
  Y3: {
    value: '3Y',
    title: t('date.shortYears', 3),
    min: DateTime.now().minus({ years: 3 }),
  },
  Y5: {
    value: '5Y',
    title: t('date.shortYears', 5),
    min: DateTime.now().minus({ years: 5 }),
  },
  MAX: {
    value: 'Max',
    title: t('date.max'),
    min: DateTime.now().minus({ years: 50 }),
  },
}))

const tickInterval = computed(() => {
  switch (current.value[0]) {
    case '1M':
      return 7 * 24 * 3600 * 1000 // 1 неделя
    case '3M':
      // Точное количество дней для 3 месяцев (~91 день)
      return Math.floor((91 * 24 * 3600 * 1000) / 3) * 3 // Кратно 3 месяцам
    case '1Y':
      // Точное количество дней для квартала (~91 день)
      return 91 * 24 * 3600 * 1000
    case '3Y':
      return 365 * 24 * 3600 * 1000 // 1 год
    case '5Y':
      return 365 * 24 * 3600 * 1000 // 1 год
    case 'Max':
      // Для максимального диапазона вычисляем оптимальный интервал
      if (!priceData.value?.length) return 2 * 365 * 24 * 3600 * 1000

      const dataRange =
        priceData.value[priceData.value.length - 1][0] - priceData.value[0][0]
      return dataRange > 10 * 365 * 24 * 3600 * 1000
        ? 2 * 365 * 24 * 3600 * 1000
        : 365 * 24 * 3600 * 1000
    default:
      return 30 * 24 * 3600 * 1000
  }
})

const chartOptions = computed<Options>(() => {
  return {
    lang: {
      locale: locale.value,
    },
    series: [
      {
        type: 'line',
        data: priceData.value,
        threshold: null,
        tooltip: {
          valueDecimals: 2,
        },
        marker: {
          radius: 2,
          fillColor: 'rgb(var(--v-theme-on-surface-light))',
          states: {
            hover: {
              radius: 4,
            },
          },
        },
        lineWidth: 2,
        color: 'rgb(var(--v-theme-info))',
      },
    ],
    chart: {
      marginTop: 40,
      style: {
        fontFamily: 'inherit',
        fontSize: '1rem',
        fontWeight: 'normal',
      },
      zooming: {
        mouseWheel: {
          enabled: false,
        },
      },
      events: {
        load() {
          const chart = this
          // Устанавливаем начальный зум (1 год) с учетом полного диапазона
          current.value = ['1Y']
          const tab = tablist.value.Y1
          const minDate = tab.min.startOf('day').toMillis()
          const maxDate = DateTime.now().toMillis()

          chart.xAxis[0].setExtremes(minDate, maxDate)
        },
      },
      reflow: true,
    },
    xAxis: [
      {
        visible: true,
        crosshair: {
          color: '#5C6874',
          dashStyle: 'ShortDash',
        },
        type: 'datetime',
        tickInterval: tickInterval.value,
        labels: {
          style: {
            color: 'rgb(var(--v-theme-on-surface-light))',
            opacity: 1,
          },
        },
      },
    ],
    yAxis: [
      {
        visible: false,
        crosshair: {
          color: '#5C6874',
          dashStyle: 'ShortDash',
        },
      },
    ],
    scrollbar: {
      enabled: false,
    },
    rangeSelector: {
      enabled: false,
    },
    navigator: {
      height: 32,
      top: 4,
      outlineWidth: 0,
      maskFill: 'rgba(35, 148, 223, 0.2)',
      handles: {
        enabled: false,
      },
      xAxis: {
        visible: false,
        gridLineWidth: 0,
        labels: {
          overflow: 'allow',
          y: -10,
          align: 'center',
          style: {
            color: 'rgb(var(--v-theme-on-surface-light))',
            opacity: 1,
            fontSize: '.75rem',
          },
        },
      },
    },
    tooltip: {
      backgroundColor: 'rgb(var(--v-theme-surface-bright))',
      borderRadius: 3,
      padding: 8,
      borderWidth: 0,
      headerFormat: '',
      xDateFormat: '%a, %e %b %Y',
      useHTML: true,
      formatter: function () {
        return `
          <div class="custom-tooltip">
            <div class="date">${DateTime.fromMillis(this.x).toFormat('EEE, d MMM yyyy', { locale: locale.value })}</div>
            <div class="price">₽${this.y?.toFixed(2)}</div>
          </div>
        `
      },
      style: {
        fontSize: '.875rem',
      },
    },
    plotOptions: {
      series: {
        animation: {
          duration: 500,
        },
        states: {
          hover: {
            halo: {
              size: 5,
              opacity: 0.1,
            },
          },
        },
      },
    },
  } satisfies Options
})

function changeZoom(tab: Tab) {
  current.value = [tab.value]
  const chart = chartRef.value?.chart
  if (chart) {
    // Устанавливаем начало периода на 00:00:00
    const minDate = tab.min.startOf('day').toMillis()
    // Устанавливаем текущее время как максимальную границу
    const maxDate = DateTime.now().toMillis()

    // Для месячного диапазона добавляем небольшой буфер (2 дня)
    const buffer = tab.value === '1M' ? 2 * 24 * 3600 * 1000 : 0

    chart.xAxis[0].setExtremes(minDate, maxDate + buffer)

    // Обновляем интервал ticks после изменения масштаба
    chart.xAxis[0].update({
      tickInterval: tickInterval.value,
    })
  }
}

const reinitChart = () => {
  if (!chartRef.value?.chart) return

  const chart = chartRef.value.chart
  const renderTo = chart.renderTo

  chart.destroy()
  const newChart = new Highcharts.StockChart(renderTo, chartOptions.value)

  chartRef.value.chart = newChart
}

watch(locale, debounce(reinitChart, 100))
</script>

<template>
  <div class="detail-price-chart__wrapper">
    <fetching-data v-if="companyDetailStore.fetchingCompany" />

    <template v-else>
      <v-btn-toggle
        mandatory
        density="compact"
        variant="text"
        selected-class="text-info"
        v-model="current"
        style="display: grid; grid-template-columns: repeat(6, 1fr)"
      >
        <v-btn
          v-for="tab in tablist"
          :key="tab.value"
          :value="tab.value"
          :text="tab.title"
          @click="changeZoom(tab)"
        />
      </v-btn-toggle>

      <charts
        ref="chartRef"
        class="detail-price-chart"
        constructorType="stockChart"
        :options="chartOptions"
      />
    </template>
  </div>
</template>

<style lang="scss">
.detail-price-chart__wrapper {
  height: 430px;

  @media (max-width: 600px) {
    height: 350px;
  }
}
.detail-price-chart {
  svg {
    width: 100%;
    height: 100%;
    fill: none;
  }
  .highcharts-background {
    fill: rgb(var(--v-theme-surface-light));
  }
  .custom-tooltip {
    width: 200px;

    .date {
      color: rgba(var(--v-theme-on-surface-light), 0.7);
      font-size: 0.875rem;
    }
    .price {
      color: rgb(var(--v-theme-on-surface-light));
      font-weight: 900;
      font-size: 1rem;
    }
  }
  .highcharts-navigator-mask-inside {
    cursor: grab !important;
    rx: 4;
    ry: 4;
    stroke-width: 1;
    stroke: rgb(var(--v-theme-info));
  }
  .highcharts-navigator-mask-outside {
    cursor: pointer;
    fill: rgba(var(--v-theme-surface-light), 0.3);
    rx: 4;
    ry: 4;
  }
  @media (max-width: 600px) {
    .highcharts-tooltip {
      font-size: 0.75rem !important;
    }
  }
}
</style>
