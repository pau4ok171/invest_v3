<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailStockOverview from "@/components/company_detail/content_list/summary/CompanyDetailStockOverview.vue";
import CompanyDetailNotes from "@/components/company_detail/content_list/summary/notes/CompanyDetailNotes.vue";
import CompanyDetailCompetitors from "@/components/company_detail/content_list/summary/competitors/CompanyDetailCompetitors.vue";
import CompanyDetailPriceHistoryPerformance
  from "@/components/company_detail/content_list/summary/CompanyDetailPriceHistoryPerformance.vue";
import CompanyDetailAboutCompany from "@/components/company_detail/content_list/summary/CompanyDetailAboutCompany.vue";
import CompanyDetailFundamentalSummary from "@/components/company_detail/content_list/summary/CompanyDetailFundamentalSummary.vue";

export default defineComponent({
  name: "CompanyDetailSummary",
  components: {
    CompanyDetailStockOverview,
    CompanyDetailNotes,
    CompanyDetailCompetitors,
    CompanyDetailPriceHistoryPerformance,
    CompanyDetailAboutCompany,
    CompanyDetailFundamentalSummary,
  },
})
</script>

<template>
<div class="detail__summary">

  <CompanyDetailStockOverview/>

  <CompanyDetailNotes/>

  <CompanyDetailCompetitors/>

  <CompanyDetailPriceHistoryPerformance/>

  <CompanyDetailAboutCompany/>

  <CompanyDetailFundamentalSummary/>

</div>
</template>
