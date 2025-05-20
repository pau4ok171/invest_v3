<script setup lang="ts">
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

function humanize(value: number = 0) {
  return `${(value * 100).toFixed(1)}%`
}
function getClass(value: number | undefined) {
  if (value == undefined) return

  if (value > 0) {
    return 'text-success'
  }
  if (value < 0) {
    return 'text-error'
  }
}
</script>

<template>
  <table class="detail-shareholder-return__table">
    <thead>
      <tr>
        <th></th>
        <th>{{ company.ticker?.toUpperCase() }}</th>
        <th>
          {{ company.country.slug?.toUpperCase() }} {{ company.sector.title }}
        </th>
        <th>{{ `${company.country.slug?.toUpperCase()} ${t('finance.market')}` }}</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>{{ t('date.shortDays', 7) }}</td>
        <td :class="getClass(company.return_7d)">
          {{ humanize(company.return_7d) }}
        </td>
        <td :class="getClass(company.sector_market.return_7d)">
          {{ humanize(company.sector_market.return_7d) }}
        </td>
        <td :class="getClass(company.market.return_7d)">
          {{ humanize(company.market.return_7d) }}
        </td>
      </tr>
      <tr>
        <td>{{ t('date.shortYears', 1) }}</td>
        <td :class="getClass(company.return_1y)">
          {{ humanize(company.return_1y) }}
        </td>
        <td :class="getClass(company.sector_market.return_1y)">
          {{ humanize(company.sector_market.return_1y) }}
        </td>
        <td :class="getClass(company.market.return_1y)">
          {{ humanize(company.market.return_1y) }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style lang="scss" scoped>
.detail-shareholder-return__table {
  color: rgba(var(--v-theme-on-surface-light), 0.5);
  border-spacing: 0;
  border-radius: 8px;
  border: 1px solid rgba(var(--v-theme-on-surface-light), 0.1);
  margin-bottom: 16px;
}
.detail-shareholder-return__table tr {
  font-size: 0.75rem;
  line-height: 1.5;
  font-weight: 500;
}
.detail-shareholder-return__table tbody tr {
  font-size: 1.125rem;
}
.detail-shareholder-return__table th,
.detail-shareholder-return__table td {
  width: 25%;
  vertical-align: top;
  padding: 4px;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.1);
}
.detail-shareholder-return__table th:first-child,
.detail-shareholder-return__table td:first-child {
  width: 10%;
  padding-left: 8px;
}
.detail-shareholder-return__table tbody tr:last-child td {
  border-bottom: none;
}
.detail-shareholder-return__table th {
  font-weight: normal;
  text-align: left;
  line-height: 1.5;
}
</style>
