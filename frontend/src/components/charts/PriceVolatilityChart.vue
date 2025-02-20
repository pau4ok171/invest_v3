<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters} from "vuex";
import DataNotAvailable from "@/components/charts/DataNotAvailable.vue";

export default defineComponent({
  name: "PriceVolatilityChart",
  components: {DataNotAvailable},
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_company_tooltip() {
      return {
        content: `${this.company.ticker} Average Weekly Mouvement ${this.format_percent(this.company.average_weekly_mouvement)}`,
        theme: 'black'
      }
    },
    get_market_tooltip() {
      return {
        content: `${this.company.country.slug.toUpperCase()} Market Average Mouvement ${this.format_percent(this.company.market.average_weekly_mouvement)}`,
        theme: 'black'
      }
    },
    get_sector_tooltip() {
      return {
        content: `${this.company.country.slug.toUpperCase()} ${this.company.sector.title} Industry Average Mouvement ${this.format_percent(this.company.sector_market.average_weekly_mouvement)}`,
        theme: 'black'
      }
    },
    getDataIsAvailable() {
      return (
          !!this.company.market &&
          !!this.company.sector_market &&
          !!this.company.average_weekly_mouvement &&
          !!this.company.market.average_weekly_mouvement &&
          !!this.company.sector_market.average_weekly_mouvement
      );
    },
  },
  methods: {
     get_label_position(value: number) {
      if (!this.company.market) return 0
      const l = 320
      const low = this.company.market.volatility_10p
      const high = this.company.market.volatility_90p
      const label_position = (value-low) / (high-low) * l - (0.5 * l)
      if (label_position > 320 / 2) {
        return 320 / 2
      }
      if (label_position < -320 / 2) {
        return -320 / 2
      }
      return label_position
    },
    format_percent(value: number) {
       return `${(value * 100).toFixed(1)}%`
    },
  }
})
</script>

<template>
  <DataNotAvailable v-if="!getDataIsAvailable" chart-name="Price Volatility Chart"/>
  <div v-else class="price-volatility-chart__wrapper">
    <div id="price-volatility-chart" class="price-volatility-chart">
      <svg v-if="company.market" viewBox="0 0 396 137" xmlns="http://www.w3.org/2000/svg" class="price-volatility-chart__svg">
        <g>
          <path d="M35 49V45H360V49H35Z" fill="url(#paint0_linear)"></path>
          <rect x="34" y="43" width="1" height="8" fill="white"></rect>
          <rect x="360" y="43" width="1" height="8" fill="white"></rect>
          <text x="0" y="51" font-size="14" class="price-volatility-chart__label">Low</text>
          <text x="367" y="51" font-size="14" class="price-volatility-chart__label">High</text>
          <defs>
            <linearGradient id="paint0_linear" x1="35" y1="45.6667" x2="360" y2="45.667" gradientUnits="userSpaceOnUse">
              <stop offset="0" class="price-volatility-chart__gradient--start"></stop>
              <stop offset="0.491713" class="price-volatility-chart__gradient--middle"></stop>
              <stop offset="1" class="price-volatility-chart__gradient--end"></stop>
            </linearGradient>
          </defs>
        </g>
          <svg v-tippy="get_company_tooltip" fill="rgb(35, 148, 223)" color="#fff" :x="get_label_position(company.average_weekly_mouvement)" tabindex="0" class="price-volatility-chart__svg">
            <rect x="159" width="81" height="32" rx="2" fill="#2394df" ></rect>
            <rect x="199" y="24" width="10.2426" fill="#2394df" height="10.2426" transform="rotate(45 199 24)"></rect>
            <text x="200" y="22" font-size="16" text-anchor="middle" class="price-volatility-chart__label">{{ company.ticker }}</text>
          </svg>
          <svg :x="get_label_position(company.market.average_weekly_mouvement)" y="55" class="price-volatility-chart__svg">
            <rect x="198" y="-6" width="1" height="68" fill="white"></rect>
            <text v-tippy="get_market_tooltip" x="198" y="80" font-size="14" text-anchor="middle" tabindex="0" class="price-volatility-chart__label">Avg. Market Volatility</text>
          </svg>
          <svg v-tippy="get_sector_tooltip" :x="get_label_position(company.sector_market.average_weekly_mouvement)" tabindex="0" class="price-volatility-chart__svg">
            <rect x="159" y="61" width="83" height="32" rx="2" fill="#71e7d6"></rect>
            <rect x="194" y="43" width="10.2426" height="10.2426" fill="#71e7d6" transform="rotate(45 183 54)"></rect>
            <text x="170" y="83" font-size="16" class="price-volatility- price-volatility-chart__label--dark">Industry</text>
          </svg>
      </svg>
    </div>
  </div>
</template>

<style scoped>
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
    fill: #fff;
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