<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import DCFChart from "@/components/charts/DCFChart.vue";
import CompanyDetailCheck from "@/components/company_detail/content_list/CompanyDetailCheck.vue";
import {mapGetters} from "vuex";
import FetchingData from "@/components/charts/FetchingData.vue";

export default defineComponent({
  name: "ShareVsFairPrice",
  components: {
    FetchingData,
    CompanyDetailCheck,
    DCFChart,
    DetailAnalysisDesc,
    DetailAnalysisTitle
  },
  data() {
    return {
      sectionDesc: '',
    }
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      pageIsReady: 'companyDetail/getPageIsReady',
    }),
  },
  watch: {
    company() {
      this.sectionDesc = `What is the Fair Price of ${this.company.slug.toUpperCase()} when looking at its future cash flows? For this estimate we use a Discounted Cash Flow model.`
    },
  },
})
</script>

<template>
<section>

  <DetailAnalysisTitle>
    <span>1.1</span>Share Price vs Fair Value
  </DetailAnalysisTitle>
  <DetailAnalysisDesc>
    {{ sectionDesc }}
  </DetailAnalysisDesc>

  <div class="detail__content">

    <div class="detail__content-item">
      <DCFChart v-if="pageIsReady"/>
      <FetchingData style="height: 358px"  v-else/>
    </div>

    <div class="detail__content-item detail__point-list">
      <CompanyDetailCheck name="IsUndervaluedBasedOnDCF"/>
      <CompanyDetailCheck name="IsHighlyUndervaluedBasedOnDCF"/>
    </div>

  </div>

</section>
</template>
