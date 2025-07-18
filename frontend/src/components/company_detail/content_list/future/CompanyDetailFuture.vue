<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'
import CompanyDetailCheck from '@/components/company_detail/base/CompanyDetailCheck.vue'
import EarningsAndRevenueGrowthForecastChart from '@/components/charts/EarningsAndRevenueGrowthForecastChart.vue'
import ForecastAnnualGrowthChart from '@/components/charts/ForecastAnnualGrowthChart.vue'
import EPSGrowthForecastChart from '@/components/charts/EPSGrowthForecastChart.vue'
import GaugeChart from '@/components/charts/GaugeChart.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'
import type { Statement } from '@/types/statements'

const store = useCompanyDetailStore()
const company = computed<DetailCompany>(() => store.company)
const { t } = useI18n()
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
      :title="`2 ${t('companyDetail.future.title')}`"
      :subtitle="
        t('companyDetail.future.subtitle', {
          ticker: company.ticker,
          earningsGrowth: 20.6,
          revenueGrowth: 20.4,
          epsGrowth: 20.3,
          roeGrowth: 50.3,
        })
      "
    >
      <v-row>
        <v-col md="6" cols="12">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>{{
              `${t('companyDetail.future.score')} ${passed}/6`
            }}</v-card-text>
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

        <v-col md="6" cols="12">
          <snowflake-chart
            :data="store.snowflake"
            size="200"
            :interactive="false"
          />
        </v-col>
      </v-row>
    </v-card-item>

    <v-card-item
      :title="`2.1 ${t('companyDetail.future.earningsAndRevenueGrowth.title')}`"
      class="pt-8 px-8"
    >
      <earnings-and-revenue-growth-forecast-chart />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      :title="`2.2 ${t('companyDetail.future.analystFutureGrowth.title')}`"
      class="pt-8 px-8"
    >
      <v-row class="mt-2">
        <v-col md="6" cols="12">
          <forecast-annual-growth-chart
            :data="[
              { name: t('finance.company'), value: 20.6, suffix: '%' },
              { name: t('finance.industry'), value: 22.9, suffix: '%' },
              { name: t('finance.market'), value: 13.3, suffix: '%' },
            ]"
            :title="
              t('companyDetail.future.analystFutureGrowth.earningsGrowthTitle')
            "
          />
        </v-col>
        <v-col md="6" cols="12">
          <forecast-annual-growth-chart
            :data="[
              { name: t('finance.company'), value: 20.2, suffix: '%' },
              { name: t('finance.industry'), value: 16.0, suffix: '%' },
              { name: t('finance.market'), value: 8.2, suffix: '%' },
            ]"
            :title="
              t('companyDetail.future.analystFutureGrowth.revenueGrowthTitle')
            "
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
      :title="`2.3 ${t('companyDetail.future.epsGrowth.title')}`"
      class="pt-8 px-8"
    >
      <e-p-s-growth-forecast-chart />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      :title="`2.4 ${t('companyDetail.future.futureROE.title')}`"
      class="pt-8 px-8"
    >
      <v-row class="my-2">
        <v-col md="6" cols="12">
          <gauge-chart
            :data="[
              { name: t('finance.company'), value: 52.9 },
              { name: t('finance.industry'), value: 11.9 },
            ]"
            :title="t('companyDetail.future.futureROE.title')"
          />
        </v-col>
        <v-col md="6" cols="12">
          <company-detail-check name="IsReturnOnEquityForecastAboveBenchmark" />
        </v-col>
      </v-row>
    </v-card-item>
  </v-card>
</template>
