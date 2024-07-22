<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import CompanyDetailCheck from "@/components/company_detail/content_list/CompanyDetailCheck.vue";
import MultiplierVsFairChart from "@/components/charts/MultiplierVsFairChart.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "MultiplierVsFair",
  components: {
    MultiplierVsFairChart,
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
      return `What is ${this.company.slug.toUpperCase()}'s PE Ratio compared to its Fair PE Ratio? This is the expected PE Ratio taking into account the company's forecast earnings growth, profit margins and other risk factors.`
    },
  },
})
</script>

<template>
<section>

  <DetailAnalysisTitle>
    <span>1.6</span>Price to Earnings Ratio vs Fair Ratio
  </DetailAnalysisTitle>

  <DetailAnalysisDesc>
    {{ get_section_desc }}
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
