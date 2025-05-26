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
      :title="`5 ${t('companyDetail.dividend.title')}`"
      :subtitle="
        t('companyDetail.dividend.subtitle', {
          ticker: company.ticker,
          divYield: '0.036',
        })
      "
    >
      <v-row>
        <v-col md="6" cols="12">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>
              {{ `${t('companyDetail.dividend.score')} ${passed}/6` }}
            </v-card-text>
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
      :title="`5.1 ${t('companyDetail.dividend.upcomingPayment.title')}`"
      class="pt-8 px-8"
    >
      <upcoming-dividend-payment-chart />
    </v-card-item>

    <v-card-item
      :title="`5.2 ${t('companyDetail.dividend.stabilityAndGrowth.title')}`"
      class="pt-8 px-8"
    >
      <stability-growth-payments-chart class="mb-8" />

      <company-detail-check name="IsDividendStable" />
      <company-detail-check name="IsDividendGrowing" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      :title="`5.3 ${t('companyDetail.dividend.yieldVsMarket.title')}`"
      class="pt-8 px-8"
    >
      <forecast-annual-growth-chart
        class="mb-8"
        :data="[
          { name: t('finance.company'), value: 0.04, suffix: '%' },
          {
            name: t('companyDetail.dividend.yieldVsMarket.chart.marketBottom'),
            value: 1.6,
            suffix: '%',
          },
          {
            name: t('companyDetail.dividend.yieldVsMarket.chart.marketTop'),
            value: 4.9,
            suffix: '%',
          },
          {
            name: t(
              'companyDetail.dividend.yieldVsMarket.chart.industryAverage'
            ),
            value: 0.6,
            suffix: '%',
          },
          {
            name: t('companyDetail.dividend.yieldVsMarket.chart.forecast'),
            value: 0.04,
            suffix: '%',
          },
        ]"
        :title="t('companyDetail.dividend.yieldVsMarket.chart.title')"
      />

      <company-detail-check name="IsDividendSignificant" />
      <company-detail-check name="IsDividendYieldTopTier" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-row>
      <v-col md="6" cols="12">
        <v-card-item
          :title="`5.4 ${t('companyDetail.dividend.earningsPayout.title')}`"
          class="pt-8 px-8"
        >
          <round-gauge-chart
            class="my-4"
            :value="30"
            suffix="%"
            :title="t('companyDetail.dividend.earningsPayout.chart.current')"
            :series-text="
              t('companyDetail.dividend.earningsPayout.chart.paidAsDividend')
            "
            :rest-text="
              t('companyDetail.dividend.earningsPayout.chart.earningsRetained')
            "
          />

          <company-detail-check name="IsDividendCovered" />
        </v-card-item>
      </v-col>
      <v-col md="6" cols="12">
        <v-card-item
          :title="`5.5 ${t('companyDetail.dividend.cashPayout.title')}`"
          class="pt-8 px-8"
        >
          <round-gauge-chart
            class="my-4"
            value="29"
            suffix="%"
            title="2028"
            :series-text="
              t('companyDetail.dividend.earningsPayout.chart.paidAsDividend')
            "
            :rest-text="
              t('companyDetail.dividend.earningsPayout.chart.earningsRetained')
            "
          />

          <company-detail-check name="IsDividendCoveredByFreeCashFlow" />
        </v-card-item>
      </v-col>
    </v-row>
  </v-card>
</template>
