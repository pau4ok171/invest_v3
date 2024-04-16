<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailSection from "@/components/company_detail/CompanyDetailSection.vue";
import DetailCompanySectionInRowItemBox from "@/components/company_detail/DetailCompanySectionInRowItemBox.vue";
import FundamentalSummaryChart from "@/components/charts/FundamentalSummaryChart.vue";
import CompanyDetailFundamentalSummaryTable
  from "@/components/company_detail/summary/CompanyDetailFundamentalSummaryTable.vue";
import EarningsRevenueChart from "@/components/charts/EarningsRevenueChart.vue";
import CompanyDetailEarningsRevenueTable
  from "@/components/company_detail/summary/CompanyDetailEarningsRevenueTable.vue";
import CompanyDetailDividendsTable from "@/components/company_detail/summary/CompanyDetailDividendsTable.vue";
import DividendPaydayChart from "@/components/charts/DividendPaydayChart.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";

export default defineComponent({
  name: "CompanyDetailFundamentalSummary",
  components: {
    DetailSectionTitle,
    DividendPaydayChart,
    CompanyDetailDividendsTable,
    CompanyDetailEarningsRevenueTable,
    EarningsRevenueChart,
    CompanyDetailFundamentalSummaryTable,
    FundamentalSummaryChart, DetailCompanySectionInRowItemBox, CompanyDetailSection},
  props: {
    company: {
      type: Object,
      required: true,
    }
  },
})
</script>

<template>
  <CompanyDetailSection>
    
    <DetailSectionTitle>{{ company.title }} Fundamental Summary</DetailSectionTitle>

    <DetailCompanySectionInRowItemBox>
      <FundamentalSummaryChart class="detail-section__in-row-item"/>
      <CompanyDetailFundamentalSummaryTable class="detail-section__in-row-item"/>
    </DetailCompanySectionInRowItemBox>

    <hr>

    <DetailSectionTitle>Earnings & Revenue</DetailSectionTitle>

    <DetailCompanySectionInRowItemBox>
      <EarningsRevenueChart class="detail-section__in-row-item"/>
      <CompanyDetailEarningsRevenueTable class="detail-section__in-row-item"/>
    </DetailCompanySectionInRowItemBox>

    <hr>

    <DetailSectionTitle>Dividends</DetailSectionTitle>

    <DetailCompanySectionInRowItemBox>
      <CompanyDetailDividendsTable class="detail-section__in-row-item"/>
      <DividendPaydayChart class="detail-section__in-row-item"/>
    </DetailCompanySectionInRowItemBox>

  </CompanyDetailSection>
</template>
