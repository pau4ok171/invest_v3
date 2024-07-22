<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import CompanyDetailCheck from "@/components/company_detail/content_list/CompanyDetailCheck.vue";
import MultiplierVsFairChart from "@/components/charts/MultiplierVsFairChart.vue";

export default defineComponent({
  name: "MultiplierVsFair",
  components: {
    MultiplierVsFairChart,
    CompanyDetailCheck,
    DetailAnalysisDesc,
    DetailAnalysisTitle
  },
  data() {
    return {
      checks: [
          {id: 5, status: 'passed', title: 'Price-To-Earnings vs Fair Ratio', description: 'SBER is good value based on its Price-To-Earnings Ratio (2.6x) compared to the estimated Fair Price-To-Earnings Ratio (4.3x)'},
      ]
    }
  }
})
</script>

<template>
<section>

  <DetailAnalysisTitle>
    <span>1.6</span>Price to Earnings Ratio vs Fair Ratio
  </DetailAnalysisTitle>

  <DetailAnalysisDesc>
    What is SBER's PE Ratio compared to its Fair PE Ratio? This is the expected PE Ratio taking into account the company's forecast earnings growth, profit margins and other risk factors.
  </DetailAnalysisDesc>

  <div class="detail__content">

    <div class="detail__content-item">

      <MultiplierVsFairChart/>

    </div>

    <div class="detail__content-item detail__point-list">
      <CompanyDetailCheck name="IsGoodValueComparingRatioToFairRatio"/>
    </div>

  </div>

</section>
</template>
