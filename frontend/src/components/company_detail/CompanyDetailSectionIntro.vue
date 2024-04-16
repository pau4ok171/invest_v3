<script lang="ts">
import {defineComponent} from 'vue'
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import CompanyDetailSectionIntroScore from "@/components/company_detail/CompanyDetailSectionIntroScore.vue";
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";

export default defineComponent({
  name: "CompanyDetailSectionIntro",
  components: {
    DetailAnalysisDesc,
    DetailAnalysisTitle,
    CompanyDetailSectionIntroScore,
    DetailSectionTitle
  },
  data() {
    return {
      section_list: {
        valuation: {
          num: 1,
          name: 'Valuation',
          desc: 'Is SBER undervalued compared to its fair value, analyst forecasts and its price relative to the market?',
        }
      },
      cur_section: {},
    }
  },
  props: {
    section_name: {
      type: String,
      required: true,
    },
  },
  mounted() {
    this.cur_section = this.section_list[this.section_name]
  }
})
</script>

<template>
  <div class="detail-section-intro">

    <DetailAnalysisTitle class="detail-section-intro__title">
      <span>{{ this.cur_section.num }}</span>{{ this.cur_section.name }}
    </DetailAnalysisTitle>

    <DetailAnalysisDesc>
      {{ this.cur_section.desc }}
    </DetailAnalysisDesc>

    <CompanyDetailSectionIntroScore/>

  </div>
</template>

<style scoped>
  .detail-section-intro {
      margin: -2.4rem -3.2rem 1.6rem;
      padding: 2.4rem 3.2rem 2.4rem;
      background-color: rgb(32, 40, 51);
      border-radius: 8px 8px 0 0;
  }
  .detail-section-intro__title {
    font-size: 2.8rem;
    margin-bottom: 8px;
  }
</style>