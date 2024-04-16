<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import DCFChart from "@/components/charts/DCFChart.vue";
import CompanyDetailCheck from "@/components/company_detail/CompanyDetailCheck.vue";

export default defineComponent({
  name: "ShareVsFairPrice",
  components: {CompanyDetailCheck, DCFChart, DetailAnalysisDesc, DetailAnalysisTitle},
  data() {
    return {
      checks: [
          {id: 1, status: 'passed', title: 'Below Fair Value', description: 'SBER is trading below our estimate of fair value'},
          {id: 2, status: 'passed', title: 'Significantly Below Fair Value', description: 'SBER is trading below fair value by more than 20%'},
      ]
    }
  }
})
</script>

<template>
  <section>

    <DetailAnalysisTitle>
      <span>1.1</span>Share Price vs Fair Value
    </DetailAnalysisTitle>
    <DetailAnalysisDesc>
      What is the Fair Price of MSFT when looking at its future cash flows? For this estimate we use a Discounted Cash Flow model.
    </DetailAnalysisDesc>

    <div class="detail__content">

      <div class="detail__content-item">
        <DCFChart/>
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
