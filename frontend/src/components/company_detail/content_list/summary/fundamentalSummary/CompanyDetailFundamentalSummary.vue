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
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

const store = useCompanyDetailStore()
const company = computed(() => store.company)
const { t } = useI18n()
</script>

<template>
  <v-card color="surface-light" class="mb-4 pa-4">
    <v-card-title>
      {{
        t('companyDetail.overview.fundamentalSummary.header', {
          title: company.title,
        })
      }}
    </v-card-title>
    <v-card-item>
      <v-row>
        <v-col cols="6">
          <fundamental-summary-chart />
        </v-col>
        <v-col cols="6">
          <company-detail-fundamental-summary-table />
          <company-detail-inducement
            :question="
              t(
                'companyDetail.overview.fundamentalSummary.inducement.question',
                { ticker: company.ticker }
              )
            "
            :response="
              t('companyDetail.overview.fundamentalSummary.inducement.response')
            "
          />
        </v-col>
      </v-row>

      <v-divider class="mt-4" />
    </v-card-item>

    <v-card-title>
      {{ t('companyDetail.overview.earningsAndRevenue.header') }}
    </v-card-title>
    <v-card-item>
      <v-row>
        <v-col cols="6">
          <earnings-revenue-chart />
        </v-col>
        <v-col cols="6">
          <company-detail-earnings-revenue-table />
          <company-detail-inducement
            :question="
              t(
                'companyDetail.overview.earningsAndRevenue.inducement.question',
                { ticker: company.ticker }
              )
            "
            :response="
              t('companyDetail.overview.earningsAndRevenue.inducement.response')
            "
          />
        </v-col>
      </v-row>

      <v-divider class="mt-4" />
    </v-card-item>

    <v-card-title>
      {{ t('companyDetail.overview.dividends.header') }}
    </v-card-title>
    <v-card-item>
      <v-row>
        <v-col cols="6">
          <company-detail-dividends-table />
          <company-detail-inducement
            :question="
              t('companyDetail.overview.dividends.inducement.question', {
                ticker: company.ticker,
              })
            "
            :response="
              t('companyDetail.overview.dividends.inducement.response')
            "
          />
        </v-col>
        <v-col cols="6">
          <dividend-payday-chart />
        </v-col>
      </v-row>
    </v-card-item>
  </v-card>
</template>
