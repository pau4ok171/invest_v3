<script lang="ts">
import {defineComponent} from 'vue'
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import CompanyDetailSectionIntroScore from "@/components/company_detail/CompanyDetailSectionIntroScore.vue";
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import {mapState} from "vuex";

export default defineComponent({
  name: "CompanyDetailSectionIntro",
  components: {
    DetailAnalysisDesc,
    DetailAnalysisTitle,
    CompanyDetailSectionIntroScore,
    DetailSectionTitle
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapState({
      statements: state => state.companyDetail.statements
    }),
    filtered_statements(){
      console.log(this.section.area)
      return [...this.statements].filter(s => s.area === this.section.area)
    },
  },
})
</script>

<template>
  <div class="detail-section-intro">

    <DetailAnalysisTitle class="detail-section-intro__title">
      <span>{{ section.num }}</span>{{ section.name }}
    </DetailAnalysisTitle>

    <DetailAnalysisDesc>
      {{ section.desc }}
    </DetailAnalysisDesc>

    <CompanyDetailSectionIntroScore :statements="filtered_statements"/>

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