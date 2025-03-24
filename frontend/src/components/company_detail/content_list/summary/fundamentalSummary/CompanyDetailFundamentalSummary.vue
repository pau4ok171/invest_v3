<script setup lang="ts">
// Components
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseCardTitle from '@/apps/visagiste/components/BaseCard/BaseCardTitle.vue'
import BaseDivider from '@/apps/visagiste/components/BaseDivider/BaseDivider.vue'
import BaseCardItem from '@/apps/visagiste/components/BaseCard/BaseCardItem.vue'
import BaseRow from '@/apps/visagiste/components/BaseGrid/BaseRow.vue'
import BaseCol from '@/apps/visagiste/components/BaseGrid/BaseCol.vue'
import FundamentalSummaryChart from '@/components/charts/FundamentalSummaryChart.vue'
import CompanyDetailFundamentalSummaryTable from '@/components/company_detail/content_list/summary/fundamentalSummary/CompanyDetailFundamentalSummaryTable.vue'
import EarningsRevenueChart from '@/components/charts/EarningsRevenueChart.vue'
import CompanyDetailEarningsRevenueTable from '@/components/company_detail/content_list/summary/fundamentalSummary/CompanyDetailEarningsRevenueTable.vue'
import CompanyDetailDividendsTable from '@/components/company_detail/content_list/summary/fundamentalSummary/CompanyDetailDividendsTable.vue'
import DividendPaydayChart from '@/components/charts/DividendPaydayChart.vue'
import CompanyDetailInducement from '@/components/company_detail/base/CompanyDetailInducement.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

const store = useCompanyDetailStore()
const company = computed(() => store.company)
</script>

<template>
  <base-card color="surface-light" class="mb-4">
    <base-card-title>{{ company.title }} Fundamental Summary</base-card-title>
    <base-card-item>
      <base-row>
        <base-col cols="6">
          <FundamentalSummaryChart />
        </base-col>
        <base-col cols="6">
          <CompanyDetailFundamentalSummaryTable />
          <company-detail-inducement
            question="Is SBER overvalued?"
            response="See Fair Value and valuation analysis"
          />
        </base-col>
      </base-row>

      <base-divider class="mt-4" />
    </base-card-item>

    <base-card-title>Earnings & Revenue</base-card-title>
    <base-card-item>
      <base-row>
        <base-col cols="6">
          <EarningsRevenueChart />
        </base-col>
        <base-col cols="6">
          <CompanyDetailEarningsRevenueTable />
          <company-detail-inducement
            question="How did SBER perform over the long term?"
            response="See historical performance and comparison"
          />
        </base-col>
      </base-row>

      <base-divider class="mt-4" />
    </base-card-item>

    <base-card-title>Dividends</base-card-title>
    <base-card-item>
      <base-row>
        <base-col cols="6">
          <CompanyDetailDividendsTable />
          <company-detail-inducement
            question="Does SBER pay a reliable dividends?"
            response="See SBER dividend history and benchmarks"
          />
        </base-col>
        <base-col cols="6">
          <DividendPaydayChart />
        </base-col>
      </base-row>
    </base-card-item>
  </base-card>
</template>
