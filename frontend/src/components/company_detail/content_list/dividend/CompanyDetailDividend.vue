<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'
import CompanyDetailCheck from '@/components/company_detail/base/CompanyDetailCheck.vue'
import UpcomingDividendPaymentChart from '@/components/charts/UpcomingDividendPaymentChart.vue'
import StabilityGrowthPaymentsChart from '@/components/charts/StabilityGrowthPaymentsChart.vue'
import ForecastAnnualGrowthChart from '@/components/charts/ForecastAnnualGrowthChart.vue'
import RoundGaugeChart from '@/components/charts/RoundGaugeChart.vue'

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
    (s) => s.area === 'DIVIDENDS' && s.outcome === 1002
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
      title="5 Dividends and Buybacks"
      :subtitle="`${company.ticker} is a dividend paying company with a current yield of 0.036%.`"
    >
      <v-row>
        <v-col md="6" cols="12">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>Dividend Score {{ passed }}/6</v-card-text>
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

    <v-card-item title="5.1 Upcoming Dividend Payment" class="pt-8 px-8">
      <upcoming-dividend-payment-chart />
    </v-card-item>

    <v-card-item title="5.2 Stability and Growth of Payments" class="pt-8 px-8">
      <stability-growth-payments-chart class="mb-8" />

      <company-detail-check name="IsDividendStable" />
      <company-detail-check name="IsDividendGrowing" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item title="5.3 Dividend Yield vs Market" class="pt-8 px-8">
      <forecast-annual-growth-chart
        class="mb-8"
        :data="[
          { name: 'Company', value: 0.04, suffix: '%' },
          { name: 'Market Bottom 25%', value: 1.6, suffix: '%' },
          { name: 'Market Top 25%', value: 4.9, suffix: '%' },
          { name: 'Industry Average', value: 0.6, suffix: '%' },
          { name: 'Forecast (up to 3 years)', value: 0.04, suffix: '%' },
        ]"
        title="Current Dividend Yield Vs Market & Industry"
      />

      <company-detail-check name="IsDividendSignificant" />
      <company-detail-check name="IsDividendYieldTopTier" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-row>
      <v-col md="6" cols="12">
        <v-card-item
          title="5.4 Earnings Payout to Shareholders"
          class="pt-8 px-8"
        >
          <round-gauge-chart
            class="my-4"
            :value="30"
            suffix="%"
            title="Current"
            series-text="Paid as dividend"
            rest-text="Earnings Retained"
          />

          <company-detail-check name="IsDividendCovered" />
        </v-card-item>
      </v-col>
      <v-col md="6" cols="12">
        <v-card-item title="5.5 Cash Payout to Shareholders" class="pt-8 px-8">
          <round-gauge-chart
            class="my-4"
            value="29"
            suffix="%"
            title="2028"
            series-text="Paid as dividend"
            rest-text="Earnings Retained"
          />

          <company-detail-check name="IsDividendCoveredByFreeCashFlow" />
        </v-card-item>
      </v-col>
    </v-row>
  </v-card>
</template>
