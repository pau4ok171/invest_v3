<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import CompanyDetailCheck from "@/components/company_detail/content_list/CompanyDetailCheck.vue";
import MultiplierVsIndustryTabList from "@/components/company_detail/content_list/valuation/MultiplierVsIndustryTabList.vue";
import MultiplierVsIndustryChart from "@/components/charts/MultiplierVsIndustryChart.vue";

export default defineComponent({
  name: "MultiplierVsIndustry",
  components: {
    MultiplierVsIndustryChart,
    MultiplierVsIndustryTabList, CompanyDetailCheck, DetailAnalysisDesc, DetailAnalysisTitle},
  data() {
    return {
      checks: [
          {id: 4, status: 'passed', title: 'Price-To-Earnings vs Industry', description: 'SBER is good value based on its Price-To-Earnings Ratio (2.6x) compared to the European Banks industry average (7.3x)'},
      ]
    }
  }
})
</script>

<template>
<section>
  <DetailAnalysisTitle>
    <span>1.5</span>Price to Earnings Ratio vs Industry
  </DetailAnalysisTitle>

  <DetailAnalysisDesc>
    How does SBER's PE Ratio compare vs other companies in the European Banks Industry?
  </DetailAnalysisDesc>

  <div class="detail__content">
    <div class="detail__content-item">

      <div class="detail-multiple-vs-industry-chart__wrapper">

        <MultiplierVsIndustryTabList/>

        <MultiplierVsIndustryChart/>

      </div>
    </div>

    <div class="detail__content-item detail__point-list">

      <CompanyDetailCheck
          v-for="check in checks"
          :check
          :key="check.id"
      />

    </div>
  </div>
</section>
</template>

<style scoped>
.detail-multiple-vs-industry-chart__wrapper {
  height: 364px;
}
</style>