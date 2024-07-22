<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import CompanyDetailCheck from "@/components/company_detail/content_list/CompanyDetailCheck.vue";

export default defineComponent({
  name: "AnalystPriceTargets",
  components: {CompanyDetailCheck, DetailAnalysisDesc, DetailAnalysisTitle},
  data() {
    return {
      checks: [
          {id: 6, status: 'failed', title: 'Analyst Forecast', description: 'Insufficient data to show price forecast'},
      ]
    }
  }
})
</script>

<template>
<section>
  <DetailAnalysisTitle>
    <span>1.7</span>Analyst Price Targets
  </DetailAnalysisTitle>

  <DetailAnalysisDesc>
    What is the analyst 12-month forecast and do we have any statistical confidence in the consensus price target?
  </DetailAnalysisDesc>

  <div class="detail__content">

    <div class="detail__content-item">
      <div class="analyst-price-targets-chart">[ANALYST PRICE TARGETS CHART]</div>
    </div>

    <div class="detail__content-item detail__point-list">
      <CompanyDetailCheck name="IsAnalystForecastTrustworthy"/>
    </div>
  </div>
</section>
</template>

<style scoped>
.analyst-price-targets-chart {
  height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  background-color: rgb(57, 67, 87);
  font-size: 3rem;
}
</style>