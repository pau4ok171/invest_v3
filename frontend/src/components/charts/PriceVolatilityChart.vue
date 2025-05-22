<script setup lang="ts">
// Components
import DataNotAvailable from '@/components/charts/DataNotAvailable.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'

const store = useCompanyDetailStore()
const company = computed<DetailCompany>(() => store.company)
const { t } = useI18n()

const companyTooltip = computed(() => ({
  content: t('companyDetail.overview.priceVolatility.companyTooltip', {
    ticker: company.value.ticker,
    value: humanize(company.value.average_weekly_mouvement),
  }),
  theme: 'black',
}))
const marketTooltip = computed(() => ({
  content: t('companyDetail.overview.priceVolatility.marketTooltip', {
    market: company.value.country.slug.toUpperCase(),
    value: humanize(company.value.market.average_weekly_mouvement),
  }),
  theme: 'black',
}))
const sectorTooltip = computed(() => ({
  content: t('companyDetail.overview.priceVolatility.industryTooltip', {
    industry: company.value.sector.title,
    value: humanize(company.value.sector_market.average_weekly_mouvement),
  }),
  theme: 'black',
}))
const available = computed(
  () =>
    !!company.value.market &&
    !!company.value.sector_market &&
    !!company.value.average_weekly_mouvement &&
    !!company.value.market.average_weekly_mouvement &&
    !!company.value.sector_market.average_weekly_mouvement
)

function getLabelPosition(value: number = 0) {
  if (!company.value.market) return 0

  const l = 320
  const low = company.value.market.volatility_10p
  const high = company.value.market.volatility_90p

  if (!low || !high) return

  const label_position = ((value - low) / (high - low)) * l - 0.5 * l
  if (label_position > 320 / 2) {
    return 320 / 2
  }
  if (label_position < -320 / 2) {
    return -320 / 2
  }
  return label_position
}

function humanize(value: number = 0) {
  return `${(value * 100).toFixed(1)}%`
}
</script>

<template>
  <data-not-available v-if="!available" chart-name="Price Volatility Chart" />
  <div v-else class="price-volatility-chart__wrapper mb-10">
    <div id="price-volatility-chart" class="price-volatility-chart">
      <svg
        v-if="company.market"
        viewBox="0 0 396 137"
        xmlns="http://www.w3.org/2000/svg"
        class="price-volatility-chart__svg"
      >
        <g>
          <path d="M35 49V45H360V49H35Z" fill="url(#paint0_linear)"></path>
          <rect
            x="34"
            y="43"
            width="1"
            height="8"
            fill="rgb(var(--v-theme-on-surface-light))"
          ></rect>
          <rect
            x="360"
            y="43"
            width="1"
            height="8"
            fill="rgb(var(--v-theme-on-surface-light))"
          ></rect>
          <text
            x="0"
            y="51"
            font-size="14"
            class="price-volatility-chart__label"
          >
            {{ t('companyDetail.overview.priceVolatility.low') }}
          </text>
          <text
            x="367"
            y="51"
            font-size="14"
            class="price-volatility-chart__label"
          >
            {{ t('companyDetail.overview.priceVolatility.high') }}
          </text>
          <defs>
            <linearGradient
              id="paint0_linear"
              x1="35"
              y1="45.6667"
              x2="360"
              y2="45.667"
              gradientUnits="userSpaceOnUse"
            >
              <stop
                offset="0"
                class="price-volatility-chart__gradient--start"
              ></stop>
              <stop
                offset="0.491713"
                class="price-volatility-chart__gradient--middle"
              ></stop>
              <stop
                offset="1"
                class="price-volatility-chart__gradient--end"
              ></stop>
            </linearGradient>
          </defs>
        </g>
        <svg
          v-tippy="companyTooltip"
          fill="rgb(35, 148, 223)"
          color="#fff"
          :x="getLabelPosition(company.average_weekly_mouvement)"
          tabindex="0"
          class="price-volatility-chart__svg"
        >
          <rect x="159" width="81" height="32" rx="2" fill="#2394df"></rect>
          <rect
            x="199"
            y="24"
            width="10.2426"
            fill="#2394df"
            height="10.2426"
            transform="rotate(45 199 24)"
          ></rect>
          <text
            x="200"
            y="22"
            font-size="16"
            text-anchor="middle"
            class="price-volatility-chart__label"
          >
            {{ company.ticker }}
          </text>
        </svg>
        <svg
          :x="getLabelPosition(company.market.average_weekly_mouvement)"
          y="55"
          class="price-volatility-chart__svg"
        >
          <rect
            x="198"
            y="-6"
            width="1"
            height="68"
            fill="rgb(var(--v-theme-on-surface-light))"
          ></rect>
          <text
            v-tippy="marketTooltip"
            x="198"
            y="80"
            font-size="14"
            text-anchor="middle"
            tabindex="0"
            class="price-volatility-chart__label"
          >
            {{ t('companyDetail.overview.priceVolatility.marketLabel') }}
          </text>
        </svg>
        <svg
          v-tippy="sectorTooltip"
          :x="getLabelPosition(company.sector_market.average_weekly_mouvement)"
          tabindex="0"
          class="price-volatility-chart__svg"
        >
          <rect
            x="159"
            y="61"
            width="83"
            height="32"
            rx="2"
            fill="#71e7d6"
          ></rect>
          <rect
            x="194"
            y="43"
            width="10.2426"
            height="10.2426"
            fill="#71e7d6"
            transform="rotate(45 183 54)"
          ></rect>
          <text
            x="170"
            y="83"
            font-size="16"
            class="price-volatility- price-volatility-chart__label--dark"
          >
            {{ t('finance.industry') }}
          </text>
        </svg>
      </svg>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.price-volatility-chart__wrapper {
  visibility: visible;
  height: 170px;
}
.price-volatility-chart {
  position: relative;
  height: 140px;
}
.price-volatility-chart svg {
  width: 100%;
  height: 100%;
  outline: none;
  user-select: none;
}
.price-volatility-chart__svg {
  margin-top: 50px;
  max-height: 180px;
  position: absolute;
  overflow: visible;
  inset: 0;
}
.price-volatility-chart__svg > text {
  user-select: none;
  outline: none;
}
.price-volatility-chart__label {
  fill: rgb(var(--v-theme-on-surface-light));
}
.price-volatility-chart__label--dark {
  fill: #262e3a;
}
.price-volatility-chart__gradient--start {
  stop-color: #2dc97e;
}
.price-volatility-chart__gradient--middle {
  stop-color: #eeb219;
}
.price-volatility-chart__gradient--end {
  stop-color: #e64141;
}
</style>
