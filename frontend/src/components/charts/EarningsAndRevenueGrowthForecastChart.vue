<script setup lang="ts">
// Composables

// Utilities
import { computed, ref } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type { Options } from 'highcharts'

// Constants
const CHART_HEIGHT = 356
const TOOLTIP_WIDTH = 340
const EARNINGS_COLOR = 'rgb(35, 148, 223)'
const REVENU_COLOR = 'rgb(113, 231, 214)'
const FCF_COLOR = 'rgb(187, 71, 134)'
const CFO_COLOR = 'rgb(229, 176, 97)'
const MAIN_TEXT_COLOR = 'rgb(var(--v-theme-on-surface))'

// Interfaces
interface FinancialData {
  date: number
  revenue: number
  earnings: number
  freeCashFlow: number
  cashFromOp: number
  analysts: number
}
interface ChartData {
  currency: string
  financialUnit: '' | 't' | 'm' | 'b' | 'T'
  financialData: FinancialData[]
}

// Reactive states
const currentDate = DateTime.now()
const activeLegends = ref<string[]>(['revenue', 'earnings'])
const legends = [
  { text: 'Revenue', value: 'revenue' },
  { text: 'Earnings', value: 'earnings' },
  { text: 'Free Cash Flow', value: 'fcf' },
  { text: 'Cash From Op', value: 'cfo' },
]

// TODO: REPLACE WITH NEEDED DATA
const tooltipData = {
  tooltipStyle: undefined,
  date: undefined,
  analysts: undefined,
  sharePrice: undefined,
  analyticsPrice: undefined,
  margeColorClass: undefined,
  marge: undefined,
  agrColorClass: undefined,
  agrStatus: undefined,
  agrText: undefined,
}

// Data
const data: ChartData = {
  currency: 'US$',
  financialUnit: 'm',
  financialData: [
    {
      date: 1835568000000,
      revenue: 287928,
      earnings: 158511,
      freeCashFlow: 144364,
      cashFromOp: 155550,
      analysts: 21,
    },
    {
      date: 1803830400000,
      revenue: 248214,
      earnings: 133079,
      freeCashFlow: 126857,
      cashFromOp: 131939,
      analysts: 50,
    },
    {
      date: 1772006400000,
      revenue: 201633,
      earnings: 104904,
      freeCashFlow: 95759,
      cashFromOp: 101337,
      analysts: 55,
    },
    {
      date: 1737763200000,
      revenue: 130497,
      earnings: 72880,
      freeCashFlow: 60853,
      cashFromOp: 64089,
      analysts: null,
    },
    {
      date: 1729987200000,
      revenue: 113269,
      earnings: 63074,
      freeCashFlow: 56546,
      cashFromOp: 58959,
      analysts: null,
    },
    {
      date: 1722124800000,
      revenue: 96307,
      earnings: 53008,
      freeCashFlow: 46786,
      cashFromOp: 48664,
      analysts: null,
    },
    {
      date: 1714262400000,
      revenue: 79774,
      earnings: 42598,
      freeCashFlow: 39334,
      cashFromOp: 40524,
      analysts: null,
    },
    {
      date: 1706400000000,
      revenue: 60922,
      earnings: 29760,
      freeCashFlow: 27021,
      cashFromOp: 28090,
      analysts: null,
    },
    {
      date: 1698537600000,
      revenue: 44870,
      earnings: 18889,
      freeCashFlow: 17515,
      cashFromOp: 18839,
      analysts: null,
    },
    {
      date: 1690675200000,
      revenue: 32681,
      earnings: 10326,
      freeCashFlow: 10323,
      cashFromOp: 11899,
      analysts: null,
    },
    {
      date: 1682812800000,
      revenue: 25878,
      earnings: 4793,
      freeCashFlow: 5101,
      cashFromOp: 6821,
      analysts: null,
    },
    {
      date: 1674950400000,
      revenue: 26974,
      earnings: 4368,
      freeCashFlow: 3808,
      cashFromOp: 5641,
      analysts: null,
    },
    {
      date: 1667088000000,
      revenue: 28566,
      earnings: 5957,
      freeCashFlow: 4829,
      cashFromOp: 6426,
      analysts: null,
    },
    {
      date: 1659225600000,
      revenue: 29738,
      earnings: 7741,
      freeCashFlow: 6264,
      cashFromOp: 7553,
      analysts: null,
    },
    {
      date: 1651363200000,
      revenue: 29541,
      earnings: 9458,
      freeCashFlow: 7926,
      cashFromOp: 8965,
      analysts: null,
    },
    {
      date: 1643500800000,
      revenue: 26914,
      earnings: 9752,
      freeCashFlow: 8132,
      cashFromOp: 9108,
      analysts: null,
    },
    {
      date: 1635638400000,
      revenue: 24274,
      earnings: 8206,
      freeCashFlow: 7156,
      cashFromOp: 8142,
      analysts: null,
    },
    {
      date: 1627776000000,
      revenue: 21897,
      earnings: 7078,
      freeCashFlow: 6665,
      cashFromOp: 7902,
      analysts: null,
    },
    {
      date: 1619913600000,
      revenue: 19256,
      earnings: 5327,
      freeCashFlow: 5516,
      cashFromOp: 6787,
      analysts: null,
    },
    {
      date: 1612051200000,
      revenue: 16675,
      earnings: 4332,
      freeCashFlow: 4694,
      cashFromOp: 5822,
      analysts: null,
    },
    {
      date: 1604188800000,
      revenue: 14777,
      earnings: 3826,
      freeCashFlow: 4230,
      cashFromOp: 5220,
      analysts: null,
    },
    {
      date: 1596326400000,
      revenue: 13065,
      earnings: 3388,
      freeCashFlow: 4961,
      cashFromOp: 5581,
      analysts: null,
    },
    {
      date: 1588464000000,
      revenue: 11778,
      earnings: 3319,
      freeCashFlow: 4434,
      cashFromOp: 4950,
      analysts: null,
    },
    {
      date: 1580601600000,
      revenue: 10918,
      earnings: 2796,
      freeCashFlow: 4272,
      cashFromOp: 4761,
      analysts: null,
    },
    {
      date: 1572739200000,
      revenue: 10018,
      earnings: 2411,
      freeCashFlow: 3647,
      cashFromOp: 4194,
      analysts: null,
    },
    {
      date: 1564876800000,
      revenue: 10185,
      earnings: 2743,
      freeCashFlow: 2447,
      cashFromOp: 3041,
      analysts: null,
    },
    {
      date: 1557014400000,
      revenue: 10729,
      earnings: 3291,
      freeCashFlow: 2408,
      cashFromOp: 3018,
      analysts: null,
    },
    {
      date: 1549152000000,
      revenue: 11716,
      earnings: 4141,
      freeCashFlow: 3143,
      cashFromOp: 3743,
      analysts: null,
    },
    {
      date: 1541289600000,
      revenue: 12422,
      earnings: 4694,
      freeCashFlow: null,
      cashFromOp: 4203,
      analysts: null,
    },
    {
      date: 1533427200000,
      revenue: 11877,
      earnings: 4301,
      freeCashFlow: null,
      cashFromOp: 4873,
      analysts: null,
    },
    {
      date: 1525564800000,
      revenue: 10984,
      earnings: 3784,
      freeCashFlow: null,
      cashFromOp: 4665,
      analysts: null,
    },
    {
      date: 1517702400000,
      revenue: 9714,
      earnings: 3047,
      freeCashFlow: null,
      cashFromOp: 3502,
      analysts: null,
    },
    {
      date: 1509840000000,
      revenue: 8976,
      earnings: 2582,
      freeCashFlow: null,
      cashFromOp: 2865,
      analysts: null,
    },
    {
      date: 1501977600000,
      revenue: 8344,
      earnings: 2288,
      freeCashFlow: null,
      cashFromOp: 2140,
      analysts: null,
    },
    {
      date: 1494115200000,
      revenue: 7542,
      earnings: 1965,
      freeCashFlow: null,
      cashFromOp: 1635,
      analysts: null,
    },
    {
      date: 1486252800000,
      revenue: 6910,
      earnings: 1666,
      freeCashFlow: null,
      cashFromOp: 1672,
      analysts: null,
    },
    {
      date: 1478390400000,
      revenue: 6138,
      earnings: 1220,
      freeCashFlow: null,
      cashFromOp: 1462,
      analysts: null,
    },
    {
      date: 1470528000000,
      revenue: 5439,
      earnings: 923,
      freeCashFlow: null,
      cashFromOp: 1285,
      analysts: null,
    },
    {
      date: 1462665600000,
      revenue: 5164,
      earnings: 688,
      freeCashFlow: null,
      cashFromOp: 1248,
      analysts: null,
    },
    {
      date: 1454803200000,
      revenue: 5010,
      earnings: 614,
      freeCashFlow: null,
      cashFromOp: 1175,
      analysts: null,
    },
    {
      date: 1446940800000,
      revenue: 4860,
      earnings: 600,
      freeCashFlow: null,
      cashFromOp: 1107,
      analysts: null,
    },
    {
      date: 1439078400000,
      revenue: 4780,
      earnings: 526,
      freeCashFlow: null,
      cashFromOp: 1068,
      analysts: null,
    },
    {
      date: 1431216000000,
      revenue: 4730,
      earnings: 628,
      freeCashFlow: null,
      cashFromOp: 1001,
      analysts: null,
    },
    {
      date: 1423353600000,
      revenue: 4682,
      earnings: 631,
      freeCashFlow: null,
      cashFromOp: 906,
      analysts: null,
    },
    {
      date: 1415491200000,
      revenue: 4575,
      earnings: 584,
      freeCashFlow: null,
      cashFromOp: 864,
      analysts: null,
    },
    {
      date: 1407628800000,
      revenue: 4404,
      earnings: 531,
      freeCashFlow: null,
      cashFromOp: 810,
      analysts: null,
    },
    {
      date: 1399766400000,
      revenue: 4278,
      earnings: 499,
      freeCashFlow: null,
      cashFromOp: 810,
      analysts: null,
    },
  ] as FinancialData[],
}

const [date, revenue, earnings, fcf, cfo] = [
  data.financialData
    .map((p) => p.date)
    .slice(0, 16)
    .reverse(),
  data.financialData
    .map((p) => [p.date, p.revenue])
    .slice(0, 16)
    .reverse(),
  data.financialData
    .map((p) => [p.date, p.earnings])
    .slice(0, 16)
    .reverse(),
  data.financialData
    .map((p) => [p.date, p.freeCashFlow])
    .slice(0, 16)
    .reverse(),
  data.financialData
    .map((p) => [p.date, p.cashFromOp])
    .slice(0, 16)
    .reverse(),
]

const options = computed<Options>(
  () =>
    ({
      chart: {
        type: 'areaspline',
        height: CHART_HEIGHT,
        backgroundColor: 'transparent',
      },
      accessibility: {
        enabled: false,
      },
      title: {
        text: undefined,
      },
      credits: {
        enabled: false,
      },
      legend: {
        enabled: false,
      },
      tooltip: {
        enabled: false,
      },
      plotOptions: {
        series: {
          marker: {
            enabled: false,
          },
          states: {
            inactive: {
              opacity: 1,
            },
            hover: {
              enabled: false,
            },
          },
        },
      },
      xAxis: {
        type: 'datetime',
        tickInterval: 365.25 * 24 * 3600 * 1000,
        tickColor: 'rgb(70, 82, 96)',
        lineColor: 'rgb(70, 82, 96)',
        gridLineWidth: 0,
        ordinal: false,
        labels: {
          format: '{value:%Y}',
          align: 'center',
          step: 1,
          style: {
            color: MAIN_TEXT_COLOR,
          },
        },
        plotBands: [
          {
            from: 0,
            to: currentDate.toMillis(),
            color: 'url(#Actual_Background_Gradient)',
            label: {
              text: 'Past',
              align: 'right',
              style: {
                color: MAIN_TEXT_COLOR,
                fontWeight: '400',
                fontSize: '0.75rem',
              },
              x: -10,
            },
            zIndex: -1,
          },
          {
            from: currentDate.toMillis(),
            to: currentDate.plus({ year: 3 }).toMillis(),
            color: 'transparent',
            label: {
              text: 'Analysts Forecasts',
              align: 'left',
              style: {
                color: '#606060',
                opacity: 1,
                fontWeight: '400',
                fontSize: '0.75rem',
              },
              x: 10,
            },
            zIndex: -1,
          },
        ],
      },
      yAxis: {
        title: { text: '' },
        gridLineWidth: 1,
        gridLineColor: 'rgba(var(--v-theme-on-surface), 0.1)',
        lineWidth: 0,
        labels: {
          formatter: function () {
            return this.isFirst ? `US$0` : this.isLast ? `US$$300b` : ''
          },
          style: {
            color: 'rgb(var(--v-theme-on-surface))',
          },
        },
        min: 0,
        max: 300000,
      },
      series: [
        {
          type: 'areaspline',
          name: 'revenue',
          data: revenue,
          color: EARNINGS_COLOR,
          fillColor: 'url(#Chart_01_Gradient_02)',
          lineWidth: 3,
          visible: activeLegends.value.includes('revenue'),
        },
        {
          type: 'areaspline',
          name: 'earnings',
          data: earnings,
          color: REVENU_COLOR,
          fillColor: 'url(#Chart_02_Gradient_02)',
          lineWidth: 3,
          visible: activeLegends.value.includes('earnings'),
        },
        {
          type: 'areaspline',
          name: 'fcf',
          data: fcf,
          color: FCF_COLOR,
          fillColor: 'url(#Chart_03_Gradient_02)',
          lineWidth: 3,
          visible: activeLegends.value.includes('fcf'),
        },
        {
          type: 'areaspline',
          name: 'cfo',
          data: cfo,
          color: CFO_COLOR,
          fillColor: 'url(#Chart_04_Gradient_02)',
          lineWidth: 3,
          visible: activeLegends.value.includes('cfo'),
        },
      ],
    }) satisfies Options
)
</script>

<template>
  <div class="earnings-and-revenue-growth-forecast-chart">
    <div class="earnings-and-revenue-growth-forecast-chart__tooltip-box">
      <v-card
        v-if="tooltipData"
        width="340"
        :style="tooltipData.tooltipStyle"
        class="text-caption text-disabled"
      >
        <v-card-item>
          <v-row no-gutters>
            <v-col class="text-high-emphasis">{{ tooltipData.date }}</v-col>
            <v-col
              ><div class="text-capitalize d-flex justify-end">
                {{ tooltipData.analysts }}
              </div></v-col
            >
          </v-row>
          <v-divider />
          <v-row no-gutters>
            <v-col cols="4">Share Price</v-col>
            <v-col offset="1"
              ><div class="text-info">
                {{ tooltipData.sharePrice }}
              </div></v-col
            >
          </v-row>
          <v-divider />
          <v-row no-gutters>
            <v-col cols="4">Average 1Y Price Target</v-col>
            <v-col offset="1"
              ><div class="text-hc-average-series-color">
                {{ tooltipData.analyticsPrice }}
              </div></v-col
            >
            <v-col :class="tooltipData.margeColorClass">{{
              tooltipData.marge
            }}</v-col>
          </v-row>
          <v-divider />
          <v-row no-gutters>
            <v-col cols="4">Agreement</v-col>
            <v-col offset="1">
              <div :class="tooltipData.agrColorClass">
                {{ tooltipData.agrStatus }}
              </div>
              <div>
                {{ tooltipData.agrText }}
              </div>
            </v-col>
          </v-row>
        </v-card-item>
      </v-card>
    </div>
    <charts
      class="earnings-and-revenue-growth-forecast-chart__chart"
      constructorType="chart"
      :options="options"
    />
    <v-btn-toggle multiple variant="outlined" v-model="activeLegends">
      <v-btn
        v-for="item in legends"
        :key="`legend-${item.value}`"
        class="earnings-and-revenue-growth-forecast-chart__legend-button"
        :value="item.value"
        size="small"
        :text="item.text"
      >
        <template #prepend>
          <span
            :class="[
              'earnings-and-revenue-growth-forecast-chart__circle-indicator',
              `earnings-and-revenue-growth-forecast-chart__circle-indicator--${item.value}`,
              {
                [`earnings-and-revenue-growth-forecast-chart__circle-indicator--${item.value}-active`]:
                  activeLegends.includes(item.value),
              },
            ]"
          />
        </template>
      </v-btn>
    </v-btn-toggle>
  </div>
</template>

<style scoped lang="scss">
.earnings-and-revenue-growth-forecast-chart {
  &__tooltip-box {
    height: 190px;
    position: relative;
    display: flex;
    align-items: end;
  }
  &__chart {
    position: relative;
    display: grid;
    justify-content: center;
  }
  &__legend-button {
    text-transform: none;
  }
  &__circle-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: 1px solid transparent;
    background-color: transparent;
    transition: background-color 0.3s;

    &--revenue {
      border-color: rgb(35, 148, 223);
      &-active {
        background-color: rgb(35, 148, 223);
      }
    }
    &--earnings {
      border-color: rgb(113, 231, 214);

      &-active {
        background-color: rgb(113, 231, 214);
      }
    }
    &--fcf {
      border-color: rgb(187, 71, 134);

      &-active {
        background-color: rgb(187, 71, 134);
      }
    }
    &--cfo {
      border-color: rgb(229, 176, 97);

      &-active {
        background-color: rgb(229, 176, 97);
      }
    }
  }
}
</style>
