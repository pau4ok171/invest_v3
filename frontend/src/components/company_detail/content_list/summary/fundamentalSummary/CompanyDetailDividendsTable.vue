<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

const store = useCompanyDetailStore()
const company = computed(() => store.company)
const { t } = useI18n()

const dividendYield = computed(() => {
  if (company.value.next_dividend.dividend_yield === undefined) {
    return 'n/a'
  }
  return `${company.value.next_dividend.dividend_yield}%`
})
const payoutRatio = computed(() => {
  if (
    company.value.next_dividend.dividend_amount === undefined ||
    !company.value.reports.length
  ) {
    return 'n/a'
  }
  const scale =
    (company.value.next_dividend.scale_unit || 1) /
    (company.value.reports[0].scale_unit || 1)
  return `${(((company.value.next_dividend.dividend_amount * scale) / company.value.reports[0].income_net) * 100).toFixed(2)}%`
})
</script>

<template>
  <div>
    <div class="detail-dividends-table">
      <div class="detail-dividends-table__item">
        <h3 class="detail-dividends-table__title">{{ dividendYield }}</h3>
        <span class="detail-dividends-table__text">
          {{ t('finance.currentDivYield') }}
        </span>
      </div>
      <div class="detail-dividends-table__item">
        <h3 class="detail-dividends-table__title">{{ payoutRatio }}</h3>
        <span class="detail-dividends-table__text">
          {{ t('finance.payoutRatio') }}
        </span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.detail-dividends-table {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
.detail-dividends-table__item {
  max-width: 100%;
  flex: 0 0 50%;
}
.detail-dividends-table__title {
  font-size: 1.25rem;
  line-height: 1.25;
  font-weight: 500;
  margin-top: 24px;
  margin-bottom: 2px;
}
.detail-dividends-table__text {
  font-size: 1rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface-light), 0.7);
}
</style>
