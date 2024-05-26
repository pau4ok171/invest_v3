<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/CompanyDetailSection.vue";
import CompanyDetailPriceHistory from "@/components/company_detail/summary/CompanyDetailPriceHistory.vue";
import CompanyDetailRecentNews from "@/components/company_detail/summary/news/CompanyDetailRecentNews.vue";
import CompanyDetailShareholderReturns from "@/components/company_detail/summary/CompanyDetailShareholderReturns.vue";
import CompanyDetailPriceVolatility from "@/components/company_detail/summary/CompanyDetailPriceVolatility.vue";
import DetailCompanySectionInRowItemBox from "@/components/company_detail/CompanySectionInRowItemBox.vue";

export default defineComponent({
  name: "CompanyDetailPriceHistoryPerformance",
  components: {
    DetailCompanySectionInRowItemBox,
    CompanyDetailPriceVolatility,
    CompanyDetailShareholderReturns,
    CompanyDetailRecentNews,
    CompanyDetailPriceHistory,
    CompanyDetailSection
  }
})
</script>

<template>
<CompanyDetailSection>

  <CompanyDetailPriceHistory/>

  <CompanyDetailRecentNews/>

  <DetailCompanySectionInRowItemBox>

    <CompanyDetailShareholderReturns class="detail-section__in-row-item"/>

    <CompanyDetailPriceVolatility class="detail-section__in-row-item"/>

  </DetailCompanySectionInRowItemBox>

</CompanyDetailSection>
</template>
