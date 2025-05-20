<script setup lang="ts">
// Components
import CompanyDetailStockOverview from '@/components/company_detail/content_list/summary/overview/CompanyDetailStockOverview.vue'
import CompanyDetailNotes from '@/components/company_detail/content_list/summary/notes/CompanyDetailNotes.vue'
import CompanyDetailCompetitors from '@/components/company_detail/content_list/summary/competitors/CompanyDetailCompetitors.vue'
import CompanyDetailPriceHistoryPerformance from '@/components/company_detail/content_list/summary/priceHistoryPerformance/CompanyDetailPriceHistoryPerformance.vue'
import CompanyDetailAboutCompany from '@/components/company_detail/content_list/summary/about/CompanyDetailAboutCompany.vue'
import CompanyDetailFundamentalSummary from '@/components/company_detail/content_list/summary/fundamentalSummary/CompanyDetailFundamentalSummary.vue'
</script>

<template>
  <div class="detail__summary">
    <company-detail-stock-overview />
    <company-detail-notes />
    <company-detail-competitors />
    <company-detail-price-history-performance />
    <company-detail-about-company />
    <company-detail-fundamental-summary />
  </div>
</template>
