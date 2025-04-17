<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'
import CompanyDetailCheck from "@/components/company_detail/base/CompanyDetailCheck.vue";

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
      title="4 Balance Sheet Health"
      :subtitle="`${company.ticker} has a total shareholder equity of $79.3B and total debt of $8.5B, which brings its debt-to-equity ratio to 10.7%. Its total assets and total liabilities are $111.6B and $32.3B respectively. ${company.ticker}'s EBIT is $81.5B making its interest coverage ratio -52.9. It has cash and short-term investments of $43.2B.`"
    >
      <v-row>
        <v-col cols="6">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>Financial Health Score {{ passed }}/6</v-card-text>
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
      title="4.1 Financial Position Analysis"
      class="pt-8 px-8"
    >
      <div
        style="
          height: 500px;
          display: flex;
          justify-content: center;
          align-items: center;
        "
      >
        [Financial Position Analysis CHART]
      </div>

      <company-detail-check name="AreShortTermLiabilitiesCovered" />
      <company-detail-check name="AreLongTermLiabilitiesCovered" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      title="4.2 Debt to Equity History and Analysis"
      class="pt-8 px-8"
    >
      <div
        style="
          height: 500px;
          display: flex;
          justify-content: center;
          align-items: center;
        "
      >
        [Debt to Equity History and Analysis CHART]
      </div>

      <company-detail-check name="IsDebtLevelAppropriate" />
      <company-detail-check name="HasDebtReducedOverTime" />
      <company-detail-check name="IsDebtCoveredByCashflow" />
      <company-detail-check name="IsInterestCoveredByProfit" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item
      title="4.3 Balance Sheet"
      class="pt-8 px-8"
    >
      <div
        style="
          height: 500px;
          display: flex;
          justify-content: center;
          align-items: center;
        "
      >
        [Balance Sheet CHART]
      </div>
    </v-card-item>
  </v-card>
</template>

<style scoped lang="scss"></style>
