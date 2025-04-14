<script setup lang="ts">
// Utilities
import { computed } from 'vue'

// Types
import type { PropType } from 'vue'
import type { Options } from 'highcharts'
import type {Snowflake, SnowflakeKey} from "@/types/invest";

// Colors
const seriesColor5 = '#6bc51a'
const seriesBorderColor5 = '#79ee04'

const seriesColor4 = '#b2c319'
const seriesBorderColor4 = '#def30b'

const seriesColor3 = '#c7a028'
const seriesBorderColor3 = '#ffc413'

const seriesColor2 = '#c75633'
const seriesBorderColor2 = '#ff5a23'

const seriesColor1 = '#c74a35'
const seriesBorderColor1 = '#fb4a27'

const successIcon = '<svg class="snowflake-chart-tooltip__success-icon" width="24" height="24"><path d="M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM0 12C0 5.37258 5.37258 0 12 0C18.6274 0 24 5.37258 24 12C24 18.6274 18.6274 24 12 24C5.37258 24 0 18.6274 0 12ZM5.70711 13.7071L9.29289 17.2929C9.68342 17.6834 10.3166 17.6834 10.7071 17.2929L18.2929 9.70711C18.6834 9.31658 18.6834 8.68342 18.2929 8.29289L17.7071 7.70711C17.3166 7.31658 16.6834 7.31658 16.2929 7.70711L10 14L7.70711 11.7071C7.31658 11.3166 6.68342 11.3166 6.29289 11.7071L5.70711 12.2929C5.31658 12.6834 5.31658 13.3166 5.70711 13.7071Z"></path></svg>'
const errorIcon = '<svg class="snowflake-chart-tooltip__error-icon" width="24" height="24" viewBox="0 0 24 24"><path d="M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM0 12C0 5.37258 5.37258 0 12 0C18.6274 0 24 5.37258 24 12C24 18.6274 18.6274 24 12 24C5.37258 24 0 18.6274 0 12ZM12 10L8.70711 6.70711C8.31658 6.31658 7.68342 6.31658 7.29289 6.70711L6.70711 7.29289C6.31658 7.68342 6.31658 8.31658 6.70711 8.70711L10 12L6.70711 15.2929C6.31658 15.6834 6.31658 16.3166 6.70711 16.7071L7.29289 17.2929C7.68342 17.6834 8.31658 17.6834 8.70711 17.2929L12 14L15.2929 17.2929C15.6834 17.6834 16.3166 17.6834 16.7071 17.2929L17.2929 16.7071C17.6834 16.3166 17.6834 15.6834 17.2929 15.2929L14 12L17.2929 8.70711C17.6834 8.31658 17.6834 7.68342 17.2929 7.29289L16.7071 6.70711C16.3166 6.31658 15.6834 6.31658 15.2929 6.70711L12 10Z"></path></svg>'

const props = defineProps({
  data: {
    type: Object as PropType<Snowflake>,
    required: true,
  },
  size: {
    type: [Number, String],
    default: '280px',
  },
})

const tooltipItems = [
  {
    title: 'Valuation',
    desc: 'Is the company undervalued compared to its peers, industry and forecasted cash flows?',
  },
  {
    title: 'Future',
    desc: 'How is the company forecast to perform in the next 1-3 years?',
  },
  {
    title: 'Past',
    desc: 'How has the company performed over the past 5 years?',
  },
  {
    title: 'Health',
    desc: 'Does the company have strong financial health and manageable debt?',
  },
  {
    title: 'Dividend',
    desc: 'Does the company pay a good, reliable and sustainable dividend?',
  },
]
const order: SnowflakeKey[] = ['value', 'future', 'past', 'health', 'dividends']
const points = computed(() => order.map((key) =>
  props.data[key].reduce((acc, v) => acc + (v.status === 'PASS' ? 1: 0), 0)
))

const colors = computed(() => {
  const score =
    points.value.reduce((acc: number, val: number) => acc + val, 0) || 0

  let areaColor
  let borderColor

  switch (true) {
    case score <= 5:
      areaColor = seriesColor1
      borderColor = seriesBorderColor1
      break
    case score <= 10:
      areaColor = seriesColor2
      borderColor = seriesBorderColor2
      break
    case score <= 15:
      areaColor = seriesColor3
      borderColor = seriesBorderColor3
      break
    case score <= 20:
      areaColor = seriesColor4
      borderColor = seriesBorderColor4
      break
    default:
      areaColor = seriesColor5
      borderColor = seriesBorderColor5
  }

  return { areaColor, borderColor }
})

const options = computed<Options>(() => ({
  chart: {
    polar: true,
    type: 'column',
    backgroundColor: 'transparent',
    height: props.size,
  },
  accessibility: {
    enabled: false,
  },
  title: {
    text: undefined,
  },
  legend: {
    enabled: false,
  },
  credits: {
    enabled: false,
  },
  xAxis: {
    categories: ['Value', 'Future', 'Past', 'Health', 'Dividend'],
    tickmarkPlacement: 'on',
    gridLineColor: 'rgb(var(--v-theme-hc-snowflake-bg-light))',
    gridLineWidth: 3,
    lineWidth: 0,
    labels: {
      enabled: false,
    },
  },
  yAxis: {
    min: 0,
    max: 6,
    tickInterval: 1,
    labels: {
      enabled: false,
    },
    gridLineWidth: 0,
  },
  series: [
    {
      name: 'Tests',
      type: 'areaspline',
      clip: false, // Отключаем обрезание по границам
      data: points.value,
      pointPlacement: 'on',
      fillColor: colors.value.areaColor,
      lineColor: colors.value.borderColor,
      lineWidth: 2,
      opacity: 0.75,
      zIndex: 1,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
    {
      name: 'Hover',
      animation: {
        duration: 300,
      },
      data: [6, 6, 6, 6, 6], // Максимальное значение
      type: 'column',
      pointPlacement: 'on',
      color: 'transparent',
      enableMouseTracking: true,
      states: {
        hover: {
          color: 'rgba(255, 255, 255, 0.4)', // Подсветка сектора
          halo: {
            enabled: false,
          },
          lineWidth: 0,
        },
      },
      zIndex: 2,
    },
    // ---- Фоновые кольца (чередующиеся) ----
    {
      name: 'Background 1',
      type: 'areasplinerange',
      pointPlacement: 'on',
      data: [
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
      ],
      fillColor: 'rgb(var(--v-theme-hc-snowflake-bg-light))',
      fillOpacity: 1,
      lineWidth: 0,
      zIndex: -3,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
    {
      name: 'Background 3',
      type: 'areasplinerange',
      pointPlacement: 'on',
      data: [
        [2, 3],
        [2, 3],
        [2, 3],
        [2, 3],
        [2, 3],
      ],
      fillColor: 'rgb(var(--v-theme-hc-snowflake-bg-light))',
      fillOpacity: 1,
      lineWidth: 0,
      zIndex: 0,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
    {
      name: 'Background 5',
      type: 'areasplinerange',
      pointPlacement: 'on',
      data: [
        [4, 5],
        [4, 5],
        [4, 5],
        [4, 5],
        [4, 5],
      ],
      fillColor: 'rgb(var(--v-theme-hc-snowflake-bg-light))',
      fillOpacity: 1,
      lineWidth: 0,
      zIndex: 0,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
  ],
  tooltip: {
    shared: true,
    outside: true,
    useHTML: true,
    formatter() {
      const item = tooltipItems[this.index]
      const key = order[this.index]
      const statement = props.data[key]
      const icons = Object.values(statement).map(s => s.status === 'PASS' ? successIcon : errorIcon)
      return `
      <div class="snowflake-chart-tooltip">
        <div class="snowflake-chart-tooltip__title text-h6"><span class="text-disabled">${this.index + 1}</span><span class="snowflake-chart-tooltip__title-separator"></span><span>${item.title}</span></div>
        <div class="snowflake-chart-tooltip__desc text-subtitle-2 mb-4">${item.desc}</div>
        <div class="snowflake-chart-tooltip__checks text-subtitle-2">
            <div>Analysis Checks <span class="text-disabled">${this.options.y}/6</span></div>
            <div>${icons.join('')}</div>
        </div>
      </div>
      `
    },
  },
  plotOptions: {
    column: {
      // Убираем промежутки между столбцами
      grouping: false,
      pointPadding: 0,
      groupPadding: 0,
      borderWidth: 0,
    },
  },
  pane: [
    {
      background: [
        {
          backgroundColor: 'rgb(var(--v-theme-hc-snowflake-bg-dark))',
          borderWidth: 0,
          outerRadius: '100%',
        },
      ],
    },
  ],
}))
</script>

<template>
  <div class="snowflake-chart">
    <div class="snowflake-chart__labels">
      <svg :width="size" :height="size" viewBox="0 0 241 231">
        <g class="snowflake-chart__labels-value">
          <path
            d="M104.414 8.87181L105.614 1.95417L107.24 1.7169L105.391 10.6068L103.961 10.8126L99.7113 2.79367L101.322 2.55652L104.414 8.87181Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M114.142 7.74834L110.828 7.99804L110.286 10.0296L108.734 10.1312L111.337 1.37086L112.663 1.286L116.522 9.56314L114.986 9.67959L114.142 7.74834ZM111.151 6.7641L113.636 6.58058L112.134 3.13725L111.151 6.7641Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M119.665 8.26608L123.554 8.25125L123.562 9.4378L118.181 9.46635L118.151 0.91969L119.643 0.920982L119.665 8.26608Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M132.244 1.42657L131.894 7.12139C131.841 8.02293 131.499 8.73135 130.885 9.21649C130.271 9.71664 129.473 9.93278 128.508 9.8648C127.528 9.81195 126.772 9.50211 126.225 8.93542C125.679 8.38374 125.432 7.6346 125.5 6.71793L125.85 1.02311L127.328 1.11735L126.978 6.82719C126.937 7.39822 127.061 7.84788 127.335 8.16127C127.609 8.47465 128.032 8.65176 128.59 8.69271C129.736 8.75936 130.35 8.19913 130.416 6.99711L130.766 1.34734L132.244 1.42657Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M139.55 7.08018L136.065 6.61023L135.722 9.21106L139.796 9.75177L139.639 10.9244L134.087 10.1994L135.214 1.73528L140.736 2.46056L140.564 3.64834L136.521 3.12243L136.207 5.46772L139.692 5.92266L139.55 7.08018Z"
            class="snowflake-labels__label-text"
          ></path>
        </g>
        <g class="snowflake-chart__labels-dividend">
          <path
            d="M8.95363 114.171L0.490265 113.412L0.714163 110.928C0.77387 110.184 1.01269 109.53 1.38586 108.995C1.77395 108.444 2.28145 108.043 2.9233 107.775C3.56514 107.507 4.28161 107.418 5.07272 107.492L5.49067 107.522C6.2967 107.596 6.98332 107.82 7.56546 108.191C8.1476 108.563 8.56554 109.054 8.84914 109.679C9.13275 110.303 9.23724 110.988 9.1626 111.746L8.95363 114.171ZM1.8038 112.059L7.89384 112.594L7.9834 111.642C8.04311 110.869 7.86399 110.259 7.41619 109.813C6.9684 109.366 6.2967 109.084 5.40111 109.009L4.92346 108.965C4.01294 108.89 3.28153 109.024 2.77403 109.381C2.2516 109.738 1.968 110.289 1.89336 111.047L1.8038 112.059Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M10.0433 104.205L9.83437 105.648L1.43071 104.428L1.63968 102.986L10.0433 104.205Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M9.20727 98.3897L3.13215 94.9688L3.46054 93.3922L11.1776 98.0625L10.894 99.4606L1.96788 100.74L2.29626 99.1631L9.20727 98.3897Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M12.6407 91.9347L12.2675 93.3477L4.05791 91.191L4.43107 89.778L12.6407 91.9347Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M13.2973 89.4656L5.22203 86.8479L5.99821 84.4681C6.23704 83.7542 6.59528 83.1741 7.08785 82.7279C7.58043 82.2817 8.17749 81.9991 8.86411 81.895C9.55074 81.776 10.2672 81.8504 11.0135 82.0883L11.4166 82.2222C12.1778 82.4751 12.8047 82.8469 13.2824 83.3377C13.76 83.8285 14.0735 84.4086 14.2078 85.0779C14.3422 85.7472 14.2825 86.4314 14.0436 87.1602L13.2973 89.4656ZM6.81917 85.8067L12.6405 87.6957L12.9391 86.7884C13.1779 86.0596 13.1331 85.42 12.8047 84.8697C12.4763 84.3194 11.8793 83.9178 11.0135 83.6352L10.5657 83.4865C9.68508 83.2039 8.95367 83.1741 8.37154 83.4121C7.7894 83.6352 7.37146 84.1111 7.13263 84.8399L6.81917 85.8067Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M14.372 75.4547L13.0585 78.6674L15.4766 79.649L17.014 75.886L18.1037 76.3322L16.014 81.4636L8.14766 78.2806L10.2225 73.1939L11.327 73.6401L9.80451 77.3585L11.9838 78.236L13.2973 75.0233L14.372 75.4547Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M21.8648 68.598L21.208 69.9218L14.1328 70.6357L19.5362 73.2981L18.8795 74.6218L11.2818 70.8588L11.9386 69.5351L19.0437 68.8212L13.6253 66.1439L14.2821 64.8351L21.8648 68.598Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M23.0741 66.4265L15.7899 62.0834L17.0736 59.9416C17.4617 59.3021 17.9394 58.8112 18.5364 58.4989C19.1186 58.1717 19.7604 58.0378 20.447 58.0676C21.1336 58.0973 21.8203 58.3353 22.5069 58.7369L22.8651 58.96C23.5517 59.3764 24.0742 59.8673 24.4324 60.4622C24.7907 61.0571 24.9548 61.6818 24.9399 62.3511C24.925 63.0204 24.716 63.6898 24.313 64.3442L23.0741 66.4265ZM17.5662 61.429L22.8203 64.5673L23.3129 63.7493C23.7159 63.0948 23.8055 62.4553 23.6115 61.8603C23.4025 61.2654 22.9248 60.7151 22.1487 60.254L21.7456 60.016C20.9545 59.54 20.253 59.3616 19.6261 59.4508C18.9991 59.54 18.4916 59.9119 18.1036 60.5663L17.5662 61.429Z"
            class="snowflake-labels__label-text"
          ></path>
        </g>
        <g class="snowflake-chart__labels-future">
          <path
            d="M223.523 68.4198L221.896 65.4302L218.732 67.1406L218.03 65.8466L225.493 61.8159L228.061 66.5457L227.016 67.1109L225.15 63.6751L222.926 64.8799L224.553 67.8694L223.523 68.4198Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M231.763 74.4285L226.598 76.7637C225.777 77.1355 225.001 77.1653 224.284 76.8529C223.568 76.5406 223.016 75.9605 222.613 75.083C222.21 74.2054 222.135 73.3874 222.359 72.6586C222.583 71.9298 223.135 71.3646 223.971 70.9928L229.136 68.6576L229.748 69.9962L224.583 72.3314C224.061 72.5694 223.732 72.8817 223.583 73.2535C223.434 73.6254 223.463 74.0864 223.702 74.5921C224.165 75.6184 224.956 75.8861 226.046 75.3953L231.181 73.0751L231.763 74.4285Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M233.867 83.323L232.957 80.854L226.105 83.3676L225.598 81.9992L232.449 79.4856L231.539 77.0315L232.658 76.6299L234.972 82.9363L233.867 83.323Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M237.45 91.2506L231.987 92.7974C231.121 93.0503 230.36 92.9611 229.688 92.5446C229.016 92.1281 228.554 91.4737 228.3 90.5515C228.031 89.6145 228.076 88.8113 228.419 88.1272C228.763 87.443 229.375 86.967 230.27 86.7142L235.718 85.1673L236.121 86.5803L230.658 88.1272C230.106 88.2759 229.733 88.5436 229.524 88.9006C229.315 89.2575 229.285 89.7037 229.434 90.2392C229.748 91.325 230.479 91.7117 231.628 91.3845L237.047 89.8525L237.45 91.2506Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M233.658 98.256L233.33 96.6497L230.135 97.3041L229.837 95.8614L238.151 94.1658L238.748 97.081C238.942 98.0329 238.882 98.8212 238.554 99.4311C238.226 100.041 237.658 100.428 236.838 100.591C236.285 100.71 235.793 100.666 235.36 100.472C234.927 100.279 234.569 99.9665 234.27 99.5352L231.18 102.108L231.106 102.123L230.792 100.576L233.658 98.256ZM234.494 96.4266L234.793 97.914C234.897 98.4048 235.091 98.7469 235.39 98.97C235.688 99.1931 236.061 99.2674 236.479 99.1782C236.927 99.089 237.241 98.8956 237.435 98.5833C237.629 98.2858 237.673 97.8842 237.584 97.3785L237.27 95.8614L234.494 96.4266Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M235.778 108.296L235.315 104.845L232.733 105.187L233.27 109.218L232.106 109.366L231.374 103.878L239.793 102.778L240.509 108.221L239.33 108.37L238.808 104.384L236.479 104.696L236.927 108.147L235.778 108.296Z"
            class="snowflake-labels__label-text"
          ></path>
        </g>
        <g class="snowflake-chart__labels-health">
          <path
            d="M35.9111 207.026L34.8961 205.97L37.6127 203.367L34.9856 200.645L32.269 203.248L31.2391 202.192L37.359 196.332L38.374 197.388L35.8215 199.827L38.4486 202.549L41.001 200.11L42.0161 201.166L35.9111 207.026Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M44.3297 209.584L41.7325 207.264L39.9861 209.197L43.0162 211.904L42.2251 212.782L38.0904 209.093L43.7625 202.802L47.8673 206.476L47.0762 207.353L44.076 204.661L42.5087 206.401L45.1059 208.721L44.3297 209.584Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M49.3453 215.905L46.7481 213.898L45.0017 215.043L43.7777 214.106L51.5097 209.361L52.5545 210.164L49.8976 218.821L48.6736 217.884L49.3453 215.905ZM47.793 213.213L49.7334 214.716L50.9126 211.191L47.793 213.213Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M53.6438 219.936L56.853 222.063L56.1963 223.045L51.7631 220.1L56.4799 213.064L57.7038 213.882L53.6438 219.936Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M66.3167 220.561L64.0329 219.222L60.346 225.499L59.0773 224.755L62.7641 218.479L60.4953 217.155L61.0924 216.129L66.8988 219.52L66.3167 220.561Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M70.7946 230.913L69.4811 230.273L71.1379 226.897L67.7197 225.231L66.0629 228.607L64.7344 227.968L68.4511 220.367L69.7796 221.007L68.2272 224.175L71.6454 225.841L73.1978 222.673L74.5113 223.312L70.7946 230.913Z"
            class="snowflake-labels__label-text"
          ></path>
        </g>
        <g class="snowflake-chart__labels-past">
          <path
            d="M178.37 223.461L179.953 226.183L178.669 226.927L174.415 219.609L177.221 217.988C178.042 217.512 178.818 217.348 179.55 217.497C180.281 217.646 180.848 218.062 181.251 218.776C181.669 219.49 181.759 220.189 181.52 220.858C181.281 221.528 180.729 222.108 179.878 222.599L178.37 223.461ZM177.773 222.435L179.311 221.543C179.759 221.275 180.057 220.977 180.162 220.62C180.281 220.263 180.221 219.892 179.983 219.49C179.759 219.088 179.445 218.85 179.072 218.746C178.699 218.657 178.296 218.717 177.863 218.955L176.296 219.862L177.773 222.435Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M188.61 218.434L185.878 220.263L186.416 222.271L185.147 223.134L183.042 214.329L184.132 213.585L191.55 218.806L190.282 219.668L188.61 218.434ZM185.565 219.059L187.61 217.69L184.625 215.474L185.565 219.059Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M195.417 213.064C195.193 212.767 194.909 212.633 194.581 212.633C194.252 212.633 193.745 212.767 193.088 213.035C192.416 213.302 191.849 213.451 191.386 213.496C190.476 213.585 189.774 213.332 189.297 212.722C188.879 212.187 188.744 211.577 188.909 210.878C189.073 210.194 189.506 209.569 190.207 209.019C190.67 208.662 191.148 208.409 191.655 208.305C192.148 208.186 192.625 208.216 193.088 208.364C193.551 208.513 193.924 208.781 194.223 209.168L193.073 210.075C192.805 209.733 192.476 209.539 192.103 209.51C191.73 209.48 191.342 209.629 190.939 209.956C190.566 210.253 190.327 210.566 190.252 210.893C190.177 211.22 190.237 211.532 190.476 211.815C190.67 212.053 190.939 212.172 191.297 212.157C191.655 212.142 192.148 212.008 192.79 211.756C193.431 211.503 193.984 211.354 194.461 211.294C194.939 211.25 195.342 211.294 195.685 211.428C196.029 211.562 196.342 211.8 196.611 212.142C197.044 212.693 197.178 213.302 197.014 213.972C196.85 214.641 196.402 215.251 195.67 215.831C195.193 216.203 194.67 216.47 194.133 216.604C193.581 216.738 193.073 216.738 192.61 216.604C192.133 216.47 191.745 216.188 191.401 215.771L192.566 214.864C192.864 215.236 193.222 215.429 193.64 215.444C194.058 215.459 194.491 215.281 194.969 214.909C195.372 214.596 195.611 214.269 195.685 213.957C195.7 213.63 195.641 213.332 195.417 213.064Z"
            class="snowflake-labels__label-text"
          ></path>
          <path
            d="M199.537 202.698L197.581 204.468L202.492 209.852L201.403 210.834L196.492 205.449L194.551 207.204L193.745 206.327L198.731 201.82L199.537 202.698Z"
            class="snowflake-labels__label-text"
          ></path>
        </g>
      </svg>
    </div>
    <div class="snowflake-chart__chart">
      <charts constructorType="chart" :options="options" />
    </div>
  </div>
</template>

<style lang="scss">
.snowflake-chart {
  position: relative;
  display: grid;
  justify-content: center;
  align-items: center;

  &__chart {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}
.snowflake-chart__labels-value {
  transform: translate(0%, 2%);
}
.snowflake-chart__labels-future {
  transform: translate(-4%, -1%);
}
.snowflake-chart__labels-past {
  transform: translate(-2.3%, -5.6%);
}
.snowflake-chart__labels-health {
  transform: translate(3%, -5%);
}
.snowflake-chart__labels-dividend {
  transform: translate(4.4%, -1.7%) rotate(0.4deg);
}
.snowflake-chart__labels {
  fill: rgb(var(--v-theme-on-surface-light));
}
.highcharts-tooltip-container {
  > svg {
    display: none;
  }
}
.snowflake-chart-tooltip {
  background: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-on-surface));
  padding: 16px 8px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  width: 296px;

  &__title {
    &-separator {
      display: inline-block;
      height: 16px;
      background-color: white;
      width: 1px;
      margin: 0 4px;
    }
  }
  &__desc {
    text-wrap: initial;
  }
  &__success-icon {
    fill-rule: evenodd;
    fill: rgb(var(--v-theme-success));
    opacity: var(--v-medium-emphasis-opacity);
  }
  &__error-icon {
    fill-rule: evenodd;
    fill: rgb(var(--v-theme-error));
    opacity: var(--v-medium-emphasis-opacity);
  }
}
</style>
