<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

const store = useCompanyDetailStore()
const company = computed(() => store.company)

const pe = computed(() => {
  const marketCap = company.value.price_data.capitalisation
  const report = company.value.reports[0]
  if (!report || !marketCap) return 'n/a'

  const earnings = report.income_net
  const scale_unit = report.scale_unit
  return `${(marketCap / (earnings * scale_unit)).toFixed(1)}x`
})
const pb = computed(() => {
  const marketCap = company.value.price_data.capitalisation
  const report = company.value.reports[0]
  if (!report || !marketCap) return 'n/a'

  const bookValue = report.assets
  const scale_unit = report.scale_unit
  return `${(marketCap / (bookValue * scale_unit)).toFixed(1)}x`
})
</script>

<template>
  <div class="detail-fundamental-summary-table">
    <div class="detail-fundamental-summary-table__in-row-item-box">
      <div class="detail-fundamental-summary-table__in-row-item">
        <h3 class="detail-fundamental-summary-table__title">{{ pe }}</h3>
        <span class="detail-fundamental-summary-table__text">P/E Ratio</span>
      </div>
      <div
        class="detail-fundamental-summary-table__in-row-item detail-fundamental-summary-table__flex-end"
      >
        <div>
          <h3 class="detail-fundamental-summary-table__subtitle">{{ pb }}</h3>
          <span class="detail-fundamental-summary-table__subtext"
            >P/B Ratio</span
          >
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.detail-fundamental-summary-table {
  margin-top: 50px;
}
.detail-fundamental-summary-table__in-row-item-box {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
.detail-fundamental-summary-table__in-row-item {
  padding-bottom: 24px;
  margin-top: 32px;
  max-width: 100%;
  flex: 0 0 50%;
}
.detail-fundamental-summary-table__flex-end {
  display: flex;
  align-items: flex-end;
}
.detail-fundamental-summary-table__title {
  font-size: 2.25rem;
  line-height: 1.25;
  font-weight: 500;
  margin-bottom: 2px;
}
.detail-fundamental-summary-table__subtitle {
  font-size: 1.25rem;
  line-height: 1.25;
  font-weight: 500;
  margin-bottom: 2px;
}
.detail-fundamental-summary-table__text {
  font-size: 1rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
}
.detail-fundamental-summary-table__subtext {
  font-size: 0.875rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
}
</style>
