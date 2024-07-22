<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import CompanyDetailCheck from "@/components/company_detail/content_list/CompanyDetailCheck.vue";
import MultiplierVsIndustryTabList from "@/components/company_detail/content_list/valuation/MultiplierVsIndustryTabList.vue";
import MultiplierVsIndustryChart from "@/components/charts/MultiplierVsIndustryChart.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "MultiplierVsIndustry",
  components: {
    MultiplierVsIndustryChart,
    MultiplierVsIndustryTabList,
    CompanyDetailCheck,
    DetailAnalysisDesc,
    DetailAnalysisTitle
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_section_desc() {
      if (!this.company.slug) return ''
      return `How does ${this.company.slug.toUpperCase()}'s PE Ratio compare vs other companies in the European Banks Industry?`
    },
  },
})
</script>

<template>
<section>
  <DetailAnalysisTitle>
    <span>1.5</span>Price to Earnings Ratio vs Industry
  </DetailAnalysisTitle>

  <DetailAnalysisDesc>
    {{ get_section_desc }}
  </DetailAnalysisDesc>

  <div class="detail__content">
    <div class="detail__content-item">

      <div class="detail-multiple-vs-industry-chart__wrapper">

        <MultiplierVsIndustryTabList/>

        <MultiplierVsIndustryChart/>

      </div>
    </div>

    <div class="detail__content-item detail__point-list">
      <CompanyDetailCheck name="IsGoodValueComparingPriceToEarningsToIndustry"/>
    </div>
  </div>
</section>
</template>

<style scoped>
.detail-multiple-vs-industry-chart__wrapper {
  height: 364px;
}
</style>