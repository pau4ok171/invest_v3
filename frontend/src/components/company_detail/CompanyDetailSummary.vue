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

<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailStockOverview from "@/components/company_detail/summary/CompanyDetailStockOverview.vue";
import CompanyDetailNotes from "@/components/company_detail/summary/notes/CompanyDetailNotes.vue";
import CompanyDetailCompetitors from "@/components/company_detail/summary/competitors/CompanyDetailCompetitors.vue";
import CompanyDetailPriceHistoryPerformance
  from "@/components/company_detail/summary/CompanyDetailPriceHistoryPerformance.vue";
import CompanyDetailAboutCompany from "@/components/company_detail/summary/CompanyDetailAboutCompany.vue";
import CompanyDetailFundamentalSummary from "@/components/company_detail/summary/CompanyDetailFundamentalSummary.vue";

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
