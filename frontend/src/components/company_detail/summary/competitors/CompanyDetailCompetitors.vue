<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/CompanyDetailSection.vue";
import CompanyDetailSnowflakeTable from "@/components/company_detail/summary/CompanyDetailSnowflakeTable.vue";
import SnowflakeChart from "@/components/charts/SnowflakeChart.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import {mapGetters} from "vuex";
import TheCompanyDetailCompetitorsItem
  from "@/components/company_detail/summary/competitors/TheCompanyDetailCompetitorsItem.vue";

export default defineComponent({
  name: "CompanyDetailCompetitors",
  components: {
    TheCompanyDetailCompetitorsItem,
    DetailSectionTitle, SnowflakeChart, CompanyDetailSnowflakeTable, CompanyDetailSection},
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      competitors: "companyDetail/getCompetitors",
    })
  },
})
</script>

<template>
<CompanyDetailSection>

  <DetailSectionTitle>{{ company.slug.toUpperCase() }} Competitors</DetailSectionTitle>

  <div class="detail-competitors">
    <TheCompanyDetailCompetitorsItem
        v-for="competitor in competitors"
        :key="competitor.id"
        :competitor
    />
  </div>

</CompanyDetailSection>
</template>

<style scoped>
.detail-competitors {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  font-size: 1.2rem;
}
</style>