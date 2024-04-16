<template>
  <div class="detail__summary">

    <CompanyDetailStockOverview
      :company
    />

    <CompanyDetailNotes/>

    <CompanyDetailCompetitors
      :company
    />

    <CompanyDetailPriceHistoryPerformance
      :company
    />

    <CompanyDetailAboutCompany
      :company
    />

    <CompanyDetailFundamentalSummary
      :company
    />

</div>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailStockOverview from "@/components/company_detail/summary/CompanyDetailStockOverview.vue";
import CompanyDetailNotes from "@/components/company_detail/summary/CompanyDetailNotes.vue";
import CompanyDetailCompetitors from "@/components/company_detail/summary/CompanyDetailCompetitors.vue";
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
  props: {
    company: {
      type: Object,
      required: true,
    }
  }
})
</script>
