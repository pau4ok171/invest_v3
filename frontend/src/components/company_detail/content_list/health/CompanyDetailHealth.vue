<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'
import CompanyDetailCheck from '@/components/company_detail/base/CompanyDetailCheck.vue'
import ForecastAnnualGrowthChart from '@/components/charts/ForecastAnnualGrowthChart.vue'
import DebtToEquityChart from '@/components/charts/DebtToEquityChart.vue'
import TreemapChart from '@/components/charts/TreemapChart.vue'

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
    (s) => s.area === 'HEALTH' && s.outcome === 1002
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
      :title="`4 ${t('companyDetail.health.title')}`"
      :subtitle="
        t('companyDetail.health.subtitle', {
          ticker: company.ticker,
          equity: '$79.3B',
          debt: '$8.5B',
          deRatio: '10.7',
          assets: '$111.6B',
          liabilities: '$32.3B',
          ebit: '$81.5B',
          interestCoverage: '52.9',
          cashAndEq: '$43.2B',
        })
      "
    >
      <v-row>
        <v-col md="6" cols="12">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>
              {{ `${t('companyDetail.health.score')} ${passed}/6` }}
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
      :title="`4.1 ${t('companyDetail.health.financialPosition.title')}`"
      class="pt-8 px-8"
    >
      <v-row class="mt-2">
        <v-col md="6" cols="12">
          <forecast-annual-growth-chart
            :data="[
              {
                name: t('companyDetail.health.financialPosition.assets'),
                value: 80.13,
                prefix: 'US$',
                suffix: 'B',
              },
              {
                name: t('companyDetail.health.financialPosition.liabilities'),
                value: 18.05,
                prefix: 'US$',
                suffix: 'B',
              },
            ]"
            :title="t('companyDetail.health.financialPosition.shortTerm')"
          />
        </v-col>
        <v-col md="6" cols="12">
          <forecast-annual-growth-chart
            :data="[
              {
                name: t('companyDetail.health.financialPosition.assets'),
                value: 31.48,
                prefix: 'US$',
                suffix: 'B',
              },
              {
                name: t('companyDetail.health.financialPosition.liabilities'),
                value: 14.23,
                prefix: 'US$',
                suffix: 'B',
              },
            ]"
            :title="t('companyDetail.health.financialPosition.longTerm')"
          />
        </v-col>
      </v-row>

      <company-detail-check name="AreShortTermLiabilitiesCovered" />
      <company-detail-check name="AreLongTermLiabilitiesCovered" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      :title="`4.2 ${t('companyDetail.health.deHistory.title')}`"
      class="pt-8 px-8"
    >
      <debt-to-equity-chart class="mb-8" />

      <company-detail-check name="IsDebtLevelAppropriate" />
      <company-detail-check name="HasDebtReducedOverTime" />
      <company-detail-check name="IsDebtCoveredByCashflow" />
      <company-detail-check name="IsInterestCoveredByProfit" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      :title="`4.3 ${t('companyDetail.health.balanceSheet.title')}`"
      class="pt-8 px-8"
    >
      <v-row class="mt-2">
        <v-col cols="6">
          <treemap-chart
            :title="t('companyDetail.health.balanceSheet.assets')"
            :data="{
              currency: 'US$',
              finUnit: 'B',
              finData: [
                { name: 'Cash & Short Term Investments', value: 43.2 },
                { name: 'Long Term & Other Assets', value: 27.2 },
                { name: 'Receivables', value: 23.1 },
                { name: 'Inventory', value: 10.1 },
                { name: 'Physical Assets', value: 8.1 },
              ],
            }"
          />
        </v-col>
        <v-col cols="6">
          <treemap-chart
            :title="`${t('companyDetail.health.balanceSheet.liabilities')} + ${t('companyDetail.health.balanceSheet.equity')}`"
            :data="{
              currency: 'US$',
              finUnit: 'B',
              finData: [
                { name: 'Equity', value: 79.2 },
                { name: 'Other Liabilities', value: 17.5 },
                { name: 'Debt', value: 8.5 },
                { name: 'Account Payable', value: 6.3 },
              ],
            }"
          />
        </v-col>
      </v-row>
    </v-card-item>
  </v-card>
</template>
