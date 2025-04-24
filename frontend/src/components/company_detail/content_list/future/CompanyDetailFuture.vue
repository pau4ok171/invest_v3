<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'
import CompanyDetailCheck from "@/components/company_detail/base/CompanyDetailCheck.vue";
import EarningsAndRevenueGrowthForecastChart from "@/components/charts/EarningsAndRevenueGrowthForecastChart.vue";
import ForecastAnnualGrowthChart from "@/components/charts/ForecastAnnualGrowthChart.vue";
import EPSGrowthForecastChart from "@/components/charts/EPSGrowthForecastChart.vue";

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'
import type { Statement } from '@/types/statements'
import GaugeChart from "@/components/charts/GaugeChart.vue";

const store = useCompanyDetailStore()
const company = computed<DetailCompany>(() => store.company)
const statements = computed<Statement[]>(() =>
  Object.values(store.statements).filter(
    (s) => s.area === 'FUTURE' && s.outcome === 1002
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
      title="2 Future Growth"
    >
      <v-card-subtitle style="white-space: normal;">
        {{ `${company.ticker} is forecast to grow earnings and revenue by 20.6% and 20.4% per year respectively. EPS is expected to grow by 20.3% per year. Return on equity is forecast to be 50.3% in 3 years.` }}
      </v-card-subtitle>

      <v-row>
        <v-col cols="6">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>Future Score {{ passed }}/6</v-card-text>
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
      title="2.1 Earnings and Revenue Growth Forecasts"
      class="pt-8 px-8"
    >
      <earnings-and-revenue-growth-forecast-chart />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      title="2.2 Analyst Future Growth Forecasts"
      class="pt-8 px-8"
    >
      <v-row class="mt-2">
        <v-col cols="6">
          <forecast-annual-growth-chart
            :data="[
              { name: 'Company', value: 20.6, suffix: '%' },
              { name: 'Industry', value: 22.9, suffix: '%' },
              { name: 'Market', value: 13.3, suffix: '%' },
            ]"
            title="Forecast Annual Earnings Growth"
          />
        </v-col>
        <v-col cols="6">
          <forecast-annual-growth-chart
            :data="[
              { name: 'Company', value: 20.2, suffix: '%' },
              { name: 'Industry', value: 16.0, suffix: '%' },
              { name: 'Market', value: 8.2, suffix: '%' },
            ]"
            title="Forecast Annual Revenue Growth"
          />
        </v-col>
      </v-row>

      <company-detail-check name="IsExpectedProfitGrowthAboveRiskFreeRate" />
      <company-detail-check name="IsExpectedAnnualProfitGrowthAboveMarket" />
      <company-detail-check name="IsExpectedAnnualProfitGrowthHigh" />
      <company-detail-check name="IsExpectedRevenueGrowthAboveMarket" />
      <company-detail-check name="IsExpectedRevenueGrowthHigh" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      title="2.3 Earnings per Share Growth Forecasts"
      class="pt-8 px-8"
    >
      <e-p-s-growth-forecast-chart />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      title="2.4 Future Return on Equity"
      class="pt-8 px-8"
    >
      <v-row class="my-2">
        <v-col cols="6">
          <gauge-chart :data="[{ name: 'Company', value: 52.9 }, { name: 'Industry', value: 11.9 }]" title="Future ROE (3yrs)" />
        </v-col>
        <v-col cols="6">
          <company-detail-check name="IsReturnOnEquityForecastAboveBenchmark" />
        </v-col>
      </v-row>

    </v-card-item>
  </v-card>
</template>
