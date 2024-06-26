<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/content_list/CompanyDetailSection.vue";
import CompanyDetailSectionIntro from "@/components/company_detail/content_list/CompanyDetailSectionIntro.vue";
import ShareVsFairPrice from "@/components/company_detail/content_list/valuation/ShareVsFairPrice.vue";
import KeyValuationMetric from "@/components/company_detail/content_list/valuation/KeyValuationMetric.vue";
import MultiplierVsPeers from "@/components/company_detail/content_list/valuation/MultiplierVsPeers.vue";
import HistoricalMultiplier from "@/components/company_detail/content_list/valuation/HistoricalMultiplier.vue";
import MultiplierVsIndustry from "@/components/company_detail/content_list/valuation/MultiplierVsIndustry.vue";
import MultiplierVsFair from "@/components/company_detail/content_list/valuation/MultiplierVsFair.vue";
import AnalystPriceTargets from "@/components/company_detail/content_list/valuation/AnalystPriceTargets.vue";
import {mapGetters} from "vuex";

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
        desc: '',
        area: 'VALUE',
      },
    }
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_section() {
      if (this.company.slug) {
        this.section.desc = `Is ${this.company.slug.toUpperCase()} undervalued compared to its fair value, analyst forecasts and its price relative to the market?`
      }
      return this.section
    },
  },
})
</script>

<template>
<CompanyDetailSection>

  <CompanyDetailSectionIntro :section="get_section"/>

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
