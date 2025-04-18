<script setup lang="ts">
// Components
import DataNotAvailable from '@/components/charts/DataNotAvailable.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, shallowRef } from 'vue'
import { DateTime } from 'luxon'

const store = useCompanyDetailStore()
const company = computed(() => store.company)

const available = shallowRef(true)
const dividendTooltip = {
  content:
    'You must be a shareholder of the company before this date to receive the next dividend payment',
  theme: 'black',
  maxWidth: 225,
}

const exDividendDate = computed(() => {
  if (!company.value.next_dividend) return

  const ex_dividend_date = DateTime.fromISO(
    company.value.next_dividend.ex_dividend_date as string
  )
  if (!ex_dividend_date.isValid) available.value = false
  return humanize(ex_dividend_date)
})
const payDay = computed(() => {
  if (!company.value.next_dividend) return

  const pay_date = DateTime.fromISO(
    company.value.next_dividend.pay_date as string
  )
  if (!pay_date.isValid) available.value = false
  return humanize(pay_date)
})
const today = computed(() => {
  if (!company.value.next_dividend) return
  const today = DateTime.now()
  return humanize(today)
})
const buyPeriod = computed(() => {
  if (!company.value.next_dividend) return
  const now = DateTime.now()
  const today = DateTime.fromObject({
    year: now.year,
    month: now.month,
    day: now.day,
  })
  let ex_dividend_date = DateTime.fromISO(
    company.value.next_dividend.ex_dividend_date as string
  )
  ex_dividend_date = ex_dividend_date.plus({ days: 1 })
  if (ex_dividend_date.isValid) {
    return ex_dividend_date.diff(today, ['days']).toObject().days
  }
  return null
})

function humanize(date: DateTime) {
  return date.toFormat('LLL dd yyyy')
}
</script>

<template>
  <div class="dividend-payday-chart__wrapper">
    <data-not-available v-if="!available" chart-name="Dividend Payday Chart" />
    <div v-else class="dividend-payday-chart">
      <svg height="168" width="100%" shape-rendering="crispEdges">
        <svg
          x="69.0888224509714%"
          y="12"
          shape-rendering="geometricPrecision"
          class="dividend-payday-chart__label"
        >
          <g
            v-tippy="dividendTooltip"
            transform="translate(-20 -2)"
            tabindex="0"
            style="outline: none; user-select: none"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              class="dividend-payday-chart__more-info-icon"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M5 12C5 15.866 8.13401 19 12 19C15.866 19 19 15.866 19 12C19 8.13401 15.866 5 12 5C8.13401 5 5 8.13401 5 12ZM12 4C7.58172 4 4 7.58172 4 12C4 16.4183 7.58172 20 12 20C16.4183 20 20 16.4183 20 12C20 7.58172 16.4183 4 12 4ZM13 8V10H11V8H13ZM13 16V11H11V16H13Z"
              ></path>
            </svg>
            <rect width="24" height="24" fill="transparent"></rect>
          </g>
          <g class="dividend-payday-chart__text" transform="translate(0, 0)">
            <svg x="-20" y="4" style="overflow: visible">
              <text transform="" fill="rgba(255,255,255,0.5)" text-anchor="end">
                <tspan x="0" dy="0.71em">Ex Dividend Date</tspan>
              </text>
            </svg>
          </g>
          <g class="dividend-payday-chart__text" transform="translate(0, 0)">
            <svg x="0" y="24" style="overflow: visible">
              <text transform="" fill="#fff" text-anchor="end">
                <tspan x="0" dy="0.71em">{{ exDividendDate }}</tspan>
              </text>
            </svg>
          </g>
        </svg>
        <svg
          x="98%"
          y="121"
          shape-rendering="geometricPrecision"
          class="dividend-payday-chart__label"
        >
          <g class="dividend-payday-chart__text" transform="translate(0, 0)">
            <svg x="0" y="4" style="overflow: visible">
              <text transform="" fill="rgba(255,255,255,0.5)" text-anchor="end">
                <tspan x="0" dy="0.71em">Dividend Pay Date</tspan>
              </text>
            </svg>
          </g>
          <g class="dividend-payday-chart__text" transform="translate(0, 0)">
            <svg x="0" y="24" style="overflow: visible">
              <text transform="" fill="#fff" text-anchor="end">
                <tspan x="0" dy="0.71em">{{ payDay }}</tspan>
              </text>
            </svg>
          </g>
        </svg>
        <svg
          x="2%"
          y="121"
          shape-rendering="geometricPrecision"
          class="dividend-payday-chart__label"
        >
          <g class="dividend-payday-chart__text" transform="translate(0, 0)">
            <svg x="0" y="4" style="overflow: visible">
              <text
                transform=""
                fill="rgba(255,255,255,0.5)"
                text-anchor="start"
              >
                <tspan x="0" dy="0.71em">Today</tspan>
              </text>
            </svg>
          </g>
          <g class="dividend-payday-chart__text" transform="translate(0, 0)">
            <svg x="0" y="24" style="overflow: visible">
              <text transform="" fill="#fff" text-anchor="start">
                <tspan x="0" dy="0.71em">{{ today }}</tspan>
              </text>
            </svg>
          </g>
        </svg>
        <line
          x1="69.0888224509714%"
          x2="69.0888224509714%"
          y1="67"
          y2="59"
          class="dividend-payday-chart__connector"
        ></line>
        <line
          x1="98%"
          x2="98%"
          y1="67"
          y2="121"
          class="dividend-payday-chart__connector"
        ></line>
        <line
          x1="2%"
          x2="2%"
          y1="67"
          y2="121"
          class="dividend-payday-chart__connector"
        ></line>
        <svg y="43" height="120" width="100%" shape-rendering="crispEdges">
          <g class="dividend-payday-chart__text" transform="translate(0, 0)">
            <svg x="20" y="24" style="overflow: visible">
              <text transform="" y="28" fill="#2394df" text-anchor="start">
                <tspan x="0" dy="-0.395em">
                  Buy in the next {{ buyPeriod }} days to
                </tspan>
                <tspan x="0" dy="1.5em">receive the upcoming dividend</tspan>
              </text>
            </svg>
          </g>
          <line
            x1="2%"
            y1="24"
            x2="98%"
            y2="24"
            class="dividend-payday-chart__principal-line"
          ></line>
          <line
            x1="2%"
            y1="24"
            x2="69.0888224509714%"
            y2="24"
            class="dividend-payday-chart__remaining-line"
          ></line>
          <circle
            cx="69.0888224509714%"
            cy="24"
            r="4.5"
            class="dividend-payday-chart__line-point"
          ></circle>
          <circle
            cx="98%"
            cy="24"
            r="4.5"
            class="dividend-payday-chart__line-point"
          ></circle>
          <circle
            cx="2%"
            cy="24"
            r="4.5"
            class="dividend-payday-chart__remaining-line-point"
          ></circle>
        </svg>
      </svg>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.dividend-payday-chart svg {
  width: 100%;
  height: 100%;
}
.dividend-payday-chart__wrapper {
  height: 200px;
}
.dividend-payday-chart__label {
  overflow: visible;
}
.dividend-payday-chart__text {
  font-size: 0.875rem;
  line-height: 1.5;
}
.dividend-payday-chart__more-info-icon {
  opacity: 0.5;
}
.dividend-payday-chart__more-info-icon > path {
  fill: rgb(var(--v-theme-on-surface-light));
}
.dividend-payday-chart__connector {
  stroke: #5f6875;
  stroke-width: 1;
}
.dividend-payday-chart__principal-line {
  stroke: #3e4855;
  stroke-width: 4;
}
.dividend-payday-chart__remaining-line {
  stroke: #2394df;
  stroke-width: 4;
}
.dividend-payday-chart__line-point {
  fill: #5f6875;
}
.dividend-payday-chart__remaining-line-point {
  fill: #2394df;
}
</style>
