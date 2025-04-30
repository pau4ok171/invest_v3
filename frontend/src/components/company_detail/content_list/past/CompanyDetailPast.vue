<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'
import CompanyDetailCheck from '@/components/company_detail/base/CompanyDetailCheck.vue'
import SankeyChart from "@/components/charts/SankeyChart.vue";
import EarningsRevenueHistoryChart from "@/components/charts/EarningsRevenueHistoryChart.vue";
import FCFAnalysisChart from "@/components/charts/FCFAnalysisChart.vue";
import ForecastAnnualGrowthChart from "@/components/charts/ForecastAnnualGrowthChart.vue";
import GaugeChart from "@/components/charts/GaugeChart.vue";

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'
import type { Statement } from '@/types/statements'

const store = useCompanyDetailStore()
const company = computed<DetailCompany>(() => store.company)
const statements = computed<Statement[]>(() =>
  Object.values(store.statements).filter(
    (s) => s.area === 'PAST' && s.outcome === 1002
  )
)
const passed = computed(() =>
  statements.value.reduce((acc, s) => {
    if (s.status === 'PASS') {
      acc += 1
    }
    return acc
  }, 0)
)
</script>

<template>
  <v-card color="surface-light" class="mb-4">
    <v-card-item
      class="bg-surface pt-8 px-8"
      title="3 Past Earnings Performance"
    >
      <v-card-subtitle>
        {{
          `${company.ticker} has been growing earnings at an average annual rate of 62.2%, while the ${company.sector.title} industry saw earnings growing at 13.5% annually. Revenues have been growing at an average rate of 46.6% per year. ${company.ticker}'s return on equity is 91.9%, and it has net margins of 55.8%.`
        }}
      </v-card-subtitle>

      <v-row>
        <v-col cols="6">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>Past Score {{ passed }}/6</v-card-text>
            <v-card-item>
              <v-list bg-color="surface-bright">
                <v-list-item
                  v-for="s in statements"
                  :key="s.id"
                  density="compact"
                  link
                  nav
                >
                  <template #prepend>
                    <v-icon
                      :icon="s.status === 'PASS' ? '$iCheck' : '$iCross'"
                      :color="s.status === 'PASS' ? 'success' : 'error'"
                      class="fill-rule-evenodd"
                    />
                  </template>
                  {{ s.title }}
                  <template #append>
                    <v-icon icon="$dropdown" />
                  </template>
                </v-list-item>
              </v-list>
            </v-card-item>
          </v-card>
        </v-col>

        <v-col cols="6">
          <snowflake-chart
            :data="store.snowflake"
            size="200"
            :interactive="false"
          />
        </v-col>
      </v-row>
    </v-card-item>

    <v-card-item
      title="3.1 Revenue & Expenses Breakdown"
      :subtitle="`How ${company.ticker} makes and spends money. Based on latest reported earnings, on an LTM basis.`"
      class="pt-8 px-8"
    >
      <sankey-chart class="mt-4" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item title="3.2 Earnings and Revenue History" class="pt-8 px-8">
      <earnings-revenue-history-chart class="mb-4" />

      <company-detail-check name="HasHighQualityPastEarnings" />
      <company-detail-check name="HasPastNetProfitMarginImprovedOverLastYear" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      title="3.3 Free Cash Flow vs Earnings Analysis"
      class="pt-8 px-8"
    >
      <f-c-f-analysis-chart />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item title="3.4 Past Earnings Growth Analysis" class="pt-8 px-8">
      <v-row class="mt-2">
        <v-col cols="6">
          <forecast-annual-growth-chart
            :data="[
              { name: 'Company', value: 62.2, suffix: '%' },
              { name: 'Industry', value: 12.4, suffix: '%' },
              { name: 'Market', value: 12.0, suffix: '%' },
            ]"
            title="Past 5 Years Annual Earnings Growth"
          />
        </v-col>
        <v-col cols="6">
          <forecast-annual-growth-chart
            :data="[
              { name: 'Company', value: 146.9, suffix: '%' },
              { name: 'Industry', value: -1.7, suffix: '%' },
              { name: 'Market', value: 4.8, suffix: '%' },
            ]"
            title="Last 1 Year Earnings Growth"
          />
        </v-col>
      </v-row>

      <company-detail-check name="HasGrownProfitsOverPast5Years" />
      <company-detail-check name="HasProfitGrowthAccelerated" />
      <company-detail-check name="IsGrowingFasterThanIndustry" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item title="3.5 Return on Equity" class="pt-8 px-8">
      <v-row>
        <v-col cols="6">
          <gauge-chart :data="[{name: 'Company', value: 91.9,}, {name: 'Industry', value: 11.9,}]" title="ROE" />
        </v-col>
        <v-col cols="6">
          <company-detail-check name="IsReturnOnEquityAboveThreshold" />
        </v-col>
      </v-row>

    </v-card-item>

    <v-divider class="my-4" />

      <v-row class="mb-2">
        <v-col cols="6">
          <v-card-item title="3.6 Return on Assets" class="pt-8 px-8">
            <gauge-chart :data="[{name: 'Company', value: 63.9,}, {name: 'Industry', value: 7.0,}]" title="ROA" />
          </v-card-item>
        </v-col>
        <v-col cols="6">
          <v-card-item title="3.7 Return on Capital Employed" class="pt-8 px-8">
            <gauge-chart :data="[{name: 'Last Year', value: 87.1,}, {name: '3 Years Ago', value: 25.1,}]" title="ROCE" />
          </v-card-item>
        </v-col>
      </v-row>
  </v-card>
</template>

<style scoped lang="scss"></style>
