<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'
import { DateTime } from 'luxon'

// Types
import type { Report } from '@/types/invest'

const store = useCompanyDetailStore()
const company = computed(() => store.company)
const { t, locale } = useI18n()

const lastEarnings = computed(() =>
  company.value.last_reported_earnings
    ? DateTime.fromISO(company.value.last_reported_earnings).toFormat('DD', {
        locale: locale.value,
      })
    : 'n/a'
)
const nextEarnings = computed(() =>
  company.value.next_earnings
    ? DateTime.fromISO(company.value.next_earnings).toFormat('DD', {
        locale: locale.value,
      })
    : 'n/a'
)
const eps = computed(() => {
  const report: Report = company.value.reports[0]
  if (!report) return 'n/a'
  return (
    (report.income_net * report.scale_unit) /
    report.share_outstanding
  ).toFixed(2)
})
const grossMargin = computed(() => {
  const report: Report = company.value.reports[0]
  if (!report) return 'n/a'
  return `${((report.gross_margin / report.sales) * 100).toFixed(2)}%`
})
const netProfitMargin = computed(() => {
  const report: Report = company.value.reports[0]
  if (!report) return 'n/a'
  return `${((report.income_net / report.sales) * 100).toFixed(2)}%`
})
const debtEquityRatio = computed(() => {
  const report: Report = company.value.reports[0]
  if (!report) return 'n/a'
  return `${((report.debt / report.equity) * 100).toFixed(2)}%`
})
</script>

<template>
  <section class="detail-earnings-revenue-table__box">
    <div class="detail-earnings-revenue-table__item">
      <p class="detail-earnings-revenue-table__title">
        {{
          t('companyDetail.overview.earningsAndRevenue.lastReportedEarnings')
        }}
      </p>
      <p class="detail-earnings-revenue-table__text">{{ lastEarnings }}</p>
    </div>
    <div class="detail-earnings-revenue-table__item">
      <p class="detail-earnings-revenue-table__title">
        {{ t('companyDetail.overview.earningsAndRevenue.nextEarnings') }}
      </p>
      <p class="detail-earnings-revenue-table__text">{{ nextEarnings }}</p>
    </div>

    <table class="detail-earnings-revenue-table table">
      <tbody>
        <tr>
          <td>
            <span>{{ t('finance.eps') }}</span>
          </td>
          <td>{{ eps }}</td>
        </tr>
        <tr>
          <td>
            <span>{{ t('finance.grossMargin') }}</span>
          </td>
          <td>{{ grossMargin }}</td>
        </tr>
        <tr>
          <td>
            <span>{{ t('finance.netProfitMargin') }}</span>
          </td>
          <td>{{ netProfitMargin }}</td>
        </tr>
        <tr>
          <td>
            <span>{{ t('finance.debtEquityRatio') }}</span>
          </td>
          <td>{{ debtEquityRatio }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style lang="scss" scoped>
.detail-earnings-revenue-table {
  font-size: 1rem;
  line-height: 1.5;
  margin-top: 32px;
}
.detail-earnings-revenue-table td {
  height: 38px;
  vertical-align: bottom;
  padding-bottom: 8px;
  padding-right: 8px;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.1);
}
.detail-earnings-revenue-table td:first-child {
  color: rgba(var(--v-theme-on-surface-light), 0.7);
}
.detail-earnings-revenue-table td:last-child {
  text-align: right;
}
.detail-earnings-revenue-table__box {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
.detail-earnings-revenue-table__item {
  max-width: 100%;
  flex: 0 0 50%;
}
.detail-earnings-revenue-table__title {
  font-size: 0.875rem;
  line-height: 1.5;
  color: rgba(var(--v-theme-on-surface-light), 0.5);
}
.detail-earnings-revenue-table__text {
  font-size: 0.875rem;
  line-height: 1.5;
}
</style>
