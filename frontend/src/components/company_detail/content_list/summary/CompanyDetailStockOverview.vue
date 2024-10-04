<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/content_list/CompanyDetailSection.vue";
import CompanyDetailContentGroup from "@/components/company_detail/content_list/CompanyDetailContentGroup.vue";
import CompanyDetailSnowflakeTable from "@/components/company_detail/content_list/summary/CompanyDetailSnowflakeTable.vue";
import SnowflakeChart from "@/components/charts/SnowflakeChart.vue";
import CompanyDetailRiskRewardItem from "@/components/company_detail/content_list/summary/CompanyDetailRiskRewardItem.vue";
import CompanyDetailRiskReward from "@/components/company_detail/content_list/summary/CompanyDetailRiskReward.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import DetailSectionText from "@/components/UI/text/DetailSectionText.vue";
import {mapGetters} from "vuex";
import BaseButton from "@/components/UI/base/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailStockOverview",
  components: {
    BaseButton,
    DetailSectionText,
    DetailSectionTitle,
    CompanyDetailRiskReward,
    CompanyDetailRiskRewardItem,
    SnowflakeChart,
    CompanyDetailSnowflakeTable,
    CompanyDetailContentGroup,
    CompanyDetailSection
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      snowflake: 'companyDetail/getSnowflake',
    }),
  },
  methods: {
    scrollToAboutTheCompanySection() {
      const goTo = (document as any).querySelector('#about-company-section').getBoundingClientRect()
      const windowScroll = document.documentElement.scrollTop
      const scrollTop = goTo.top + windowScroll - 80
      window.scrollTo({top: scrollTop, behavior: 'smooth'})
    }
  },
})
</script>

<template>
<CompanyDetailSection :useGrid="true" :useMinH="true">
  <CompanyDetailContentGroup>
    <DetailSectionTitle>{{ company.ticker }} Stock Overview</DetailSectionTitle>
    <DetailSectionText>{{ company.short_description }}</DetailSectionText>

    <base-button
      prepend-icon="InfoIcon"
      text="about the company"
      variant="plain"
      color="var(--blue)"
      @click="scrollToAboutTheCompanySection"
    />

  </CompanyDetailContentGroup>

  <CompanyDetailContentGroup :useGridRow="true">

    <CompanyDetailSnowflakeTable v-if="false"/>

    <SnowflakeChart :chartData="snowflake" v-else/>

  </CompanyDetailContentGroup>

  <CompanyDetailContentGroup :useGrid="true">

    <CompanyDetailRiskReward/>

  </CompanyDetailContentGroup>

</CompanyDetailSection>
</template>
