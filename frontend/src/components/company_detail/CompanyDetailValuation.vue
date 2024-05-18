<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/CompanyDetailSection.vue";
import CompanyDetailSectionIntro from "@/components/company_detail/CompanyDetailSectionIntro.vue";
import ShareVsFairPrice from "@/components/company_detail/valuation/ShareVsFairPrice.vue";
import KeyValuationMetric from "@/components/company_detail/valuation/KeyValuationMetric.vue";
import MultiplierVsPeers from "@/components/company_detail/valuation/MultiplierVsPeers.vue";
import HistoricalMultiplier from "@/components/company_detail/valuation/HistoricalMultiplier.vue";
import MultiplierVsIndustry from "@/components/company_detail/valuation/MultiplierVsIndustry.vue";
import MultiplierVsFair from "@/components/company_detail/valuation/MultiplierVsFair.vue";
import AnalystPriceTargets from "@/components/company_detail/valuation/AnalystPriceTargets.vue";

export default defineComponent({
  name: "CompanyDetailValuation",
  components: {
    AnalystPriceTargets,
    MultiplierVsFair,
    MultiplierVsIndustry,
    HistoricalMultiplier,
    MultiplierVsPeers,
    KeyValuationMetric,
    ShareVsFairPrice,
    CompanyDetailSectionIntro,
    CompanyDetailSection
  },
  data() {
    return {
      section: {
        num: 1,
        name: 'Valuation',
        desc: 'Is SBER undervalued compared to its fair value, analyst forecasts and its price relative to the market?',
        area: 'VALUE',
      },
    }
  },
})
</script>

<template>
<CompanyDetailSection>

  <CompanyDetailSectionIntro :section/>

  <ShareVsFairPrice/>

  <hr>

  <KeyValuationMetric/>

  <hr>

  <MultiplierVsPeers/>

  <hr>

  <HistoricalMultiplier/>

  <hr>

  <MultiplierVsIndustry/>

  <hr>

  <MultiplierVsFair/>

  <hr>

  <AnalystPriceTargets/>

</CompanyDetailSection>
</template>
