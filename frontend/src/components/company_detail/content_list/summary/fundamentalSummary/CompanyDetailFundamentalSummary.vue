<script setup lang="ts">
// Components
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
  <v-card color="surface-light" class="mb-4">
    <v-card-title>{{ company.title }} Fundamental Summary</v-card-title>
    <v-card-item>
      <v-row>
        <v-col cols="6">
          <FundamentalSummaryChart />
        </v-col>
        <v-col cols="6">
          <CompanyDetailFundamentalSummaryTable />
          <company-detail-inducement
            question="Is SBER overvalued?"
            response="See Fair Value and valuation analysis"
          />
        </v-col>
      </v-row>

      <v-divider class="mt-4" />
    </v-card-item>

    <v-card-title>Earnings & Revenue</v-card-title>
    <v-card-item>
      <v-row>
        <v-col cols="6">
          <EarningsRevenueChart />
        </v-col>
        <v-col cols="6">
          <CompanyDetailEarningsRevenueTable />
          <company-detail-inducement
            question="How did SBER perform over the long term?"
            response="See historical performance and comparison"
          />
        </v-col>
      </v-row>

      <v-divider class="mt-4" />
    </v-card-item>

    <v-card-title>Dividends</v-card-title>
    <v-card-item>
      <v-row>
        <v-col cols="6">
          <CompanyDetailDividendsTable />
          <company-detail-inducement
            question="Does SBER pay a reliable dividends?"
            response="See SBER dividend history and benchmarks"
          />
        </v-col>
        <v-col cols="6">
          <DividendPaydayChart />
        </v-col>
      </v-row>
    </v-card-item>
  </v-card>
</template>
