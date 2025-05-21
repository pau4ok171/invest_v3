<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

const store = useCompanyDetailStore()
const company = computed(() => store.company)
const { t } = useI18n()
</script>

<template>
  <div class="key-valuation-metrics__table-wrapper">
    <table class="key-valuation-metrics__table">
      <caption>
        {{
          t('companyDetail.valuation.keyValuationMetric.caption', {
            ticker: company.ticker,
          })
        }}
      </caption>
      <thead>
        <tr>
          <th colspan="2">
            {{ t('companyDetail.valuation.keyValuationMetric.keyStatistics') }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <span tabindex="0" class="key-valuation-metrics__table-text">
              {{ t('companyDetail.valuation.keyValuationMetric.evToRevenue') }}
            </span>
          </td>
          <td>n/a</td>
        </tr>
        <tr>
          <td>
            <span tabindex="0" class="key-valuation-metrics__table-text">
              {{ t('companyDetail.valuation.keyValuationMetric.evToEBITDA') }}
            </span>
          </td>
          <td>n/a</td>
        </tr>
        <tr>
          <td>
            <span tabindex="0" class="key-valuation-metrics__table-text">
              {{ t('companyDetail.valuation.keyValuationMetric.pegRatio') }}
            </span>
          </td>
          <td>0.3x</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style lang="scss" scoped>
.key-valuation-metrics__table-wrapper {
  min-height: 280px;
}
.key-valuation-metrics__table {
  line-height: 1.5;
  font-weight: 500;
  width: 100%;
  border-spacing: 0;
  font-size: 1rem;
  margin-top: 0;
}
.key-valuation-metrics__table caption {
  line-height: 1.5;
  opacity: 0.5;
  padding-top: 8px;
  caption-side: bottom;
  text-align: left;
  font-size: 0.75rem;
}
.key-valuation-metrics__table th {
  text-align: left;
  line-height: 1.5;
  font-weight: 500;
  font-size: 0.75rem;
}
.key-valuation-metrics__table td {
  font-size: 1rem;
  box-sizing: border-box;
  height: 38px;
  padding-bottom: 8px;
  vertical-align: bottom;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.1);
}
.key-valuation-metrics__table-text {
  line-height: 1.5;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface-light), 0.7);
  border-bottom: 1px dotted rgb(35, 148, 223);
  cursor: help;
  width: fit-content;
  font-size: 1rem;
}
</style>
