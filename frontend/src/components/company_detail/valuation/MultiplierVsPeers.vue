<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import MultiplierVsPeersTabList from "@/components/company_detail/valuation/MultiplierVsPeersTabList.vue";
import MultiplierVsPeersChart from "@/components/charts/MultiplierVsPeersChart.vue";
import CompanyDetailCheck from "@/components/company_detail/CompanyDetailCheck.vue";

export default defineComponent({
  name: "MultiplierVsPeers",
  components: {
    CompanyDetailCheck,
    MultiplierVsPeersChart, MultiplierVsPeersTabList, DetailAnalysisDesc, DetailAnalysisTitle},
  data() {
    return {
      checks: [
          {id: 3, status: 'passed', title: 'Price-To-Earnings vs Peers', description: 'SBER is good value based on its Price-To-Earnings Ratio (2.6x) compared to the peer average (7.9x)'},
      ]
    }
  }
})
</script>

<template>
  <section>
    <DetailAnalysisTitle>
      <span>1.3</span>Price to Earnings Ratio vs Peers
    </DetailAnalysisTitle>

    <DetailAnalysisDesc>
      How does SBER's PE Ratio compare to its peers?
    </DetailAnalysisDesc>

    <div class="detail__content">
      <div class="detail__content-item">

        <MultiplierVsPeersTabList/>

        <MultiplierVsPeersChart/>

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
