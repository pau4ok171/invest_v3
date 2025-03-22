<script setup lang="ts">
// Components
import CompanyDetailStockOverview from '@/components/company_detail/content_list/summary/CompanyDetailStockOverview.vue'
import CompanyDetailNotes from '@/components/company_detail/content_list/summary/notes/CompanyDetailNotes.vue'
import CompanyDetailCompetitors from '@/components/company_detail/content_list/summary/competitors/CompanyDetailCompetitors.vue'
import CompanyDetailPriceHistoryPerformance from '@/components/company_detail/content_list/summary/CompanyDetailPriceHistoryPerformance.vue'
import CompanyDetailAboutCompany from '@/components/company_detail/content_list/summary/CompanyDetailAboutCompany.vue'
import CompanyDetailFundamentalSummary from '@/components/company_detail/content_list/summary/CompanyDetailFundamentalSummary.vue'
</script>

<template>
  <div class="detail__summary">
    <CompanyDetailStockOverview />
    <CompanyDetailNotes />
    <CompanyDetailCompetitors />
    <CompanyDetailPriceHistoryPerformance />
    <CompanyDetailAboutCompany />
    <CompanyDetailFundamentalSummary />
  </div>
</template>
