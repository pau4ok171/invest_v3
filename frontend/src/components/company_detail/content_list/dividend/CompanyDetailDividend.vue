<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'
import CompanyDetailCheck from '@/components/company_detail/base/CompanyDetailCheck.vue'
import UpcomingDividendPaymentChart from "@/components/charts/UpcomingDividendPaymentChart.vue";

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
        <v-col cols="6">
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

        <v-col cols="6">
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
      <div
        style="
          height: 500px;
          display: flex;
          justify-content: center;
          align-items: center;
        "
      >
        [Stability and Growth of Payments CHART]
      </div>

      <company-detail-check name="IsDividendStable" />
      <company-detail-check name="IsDividendGrowing" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-card-item title="5.2 Dividend Yield vs Market" class="pt-8 px-8">
      <div
        style="
          height: 500px;
          display: flex;
          justify-content: center;
          align-items: center;
        "
      >
        [Dividend Yield vs Market CHART]
      </div>

      <company-detail-check name="IsDividendSignificant" />
      <company-detail-check name="IsDividendYieldTopTier" />
    </v-card-item>

    <v-divider class="my-4" />

    <v-row>
      <v-col cols="6">
        <v-card-item
          title="5.3 Earnings Payout to Shareholders"
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
            [Earnings Payout to Shareholders CHART]
          </div>

          <company-detail-check name="IsDividendCovered" />
        </v-card-item>
      </v-col>
      <v-col cols="6">
        <v-card-item title="5.4 Cash Payout to Shareholders" class="pt-8 px-8">
          <div
            style="
              height: 500px;
              display: flex;
              justify-content: center;
              align-items: center;
            "
          >
            [Cash Payout to Shareholders CHART]
          </div>

          <company-detail-check name="IsDividendCoveredByFreeCashFlow" />
        </v-card-item>
      </v-col>
    </v-row>
  </v-card>
</template>

<style scoped lang="scss"></style>
