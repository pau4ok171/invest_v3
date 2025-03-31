<script setup lang="ts">
// Components
import SmallPriceChart from '@/components/charts/SmallPriceChart.vue'
import CompanyDetailHeaderAnalystsDialog from '@/components/company_detail/header/CompanyDetailHeaderAnalystsDialog.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'

const companyDetailStore = useCompanyDetailStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const loading = computed(() => companyDetailStore.fetchingCompany)

const totalIdeas = computed(() => company.value.analyst_ideas.length)

function humanize(val: number = 0, currencySymbol: string = ''): string {
  if (val === 0) return 'n/a'
  for (const unit of ['', 't', 'M', 'B', 'T']) {
    if (Math.abs(val) < 1000) return currencySymbol + val.toFixed(2) + unit
    val /= 1000
  }
  return currencySymbol + val.toFixed(2) + 'Q'
}
</script>

<template>
  <v-row
    no-gutters
    style="font-size: 0.75rem"
    class="mb-1"
    align-content="center"
  >
    <v-col cols="1" class="d-flex flex-column">
      <v-skeleton-loader v-if="loading" type="text" max-height="40" />
      <template v-else>
        <span class="text-uppercase opacity-70">Last Price</span>
        <span>{{
          `${company.formatting.primaryCurrencySymbol}${company.price_data.last_price?.toFixed(2)}`
        }}</span>
      </template>
    </v-col>
    <v-col cols="1" class="d-flex flex-column">
      <v-skeleton-loader v-if="loading" type="text" max-height="40" />
      <template v-else>
        <span class="text-uppercase opacity-70">Market cap</span>
        <span>{{
          humanize(
            company.price_data.capitalisation,
            company.formatting.primaryCurrencySymbol
          )
        }}</span>
      </template>
    </v-col>
    <v-col cols="1" class="d-flex flex-column">
      <v-skeleton-loader v-if="loading" type="text" max-height="40" />
      <template v-else>
        <span class="text-uppercase opacity-70">7D</span>
        <span
          :class="[
            company.return_7d && company.return_7d > 0
              ? 'text-success'
              : 'text-error',
          ]"
          >{{ `${company.return_7d?.toFixed(2)}%` }}</span
        >
      </template>
    </v-col>
    <v-col cols="1" class="d-flex flex-column">
      <v-skeleton-loader v-if="loading" type="text" max-height="40" />
      <template v-else>
        <span class="text-uppercase opacity-70">1Y</span>
        <span
          :class="[
            company.return_1y && company.return_1y > 0
              ? 'text-success'
              : 'text-error',
          ]"
          >{{ `${company.return_1y && company.return_1y.toFixed(2)}%` }}</span
        >
      </template>
    </v-col>
    <v-col class="d-flex justify-center">
      <v-progress-circular v-if="loading" indeterminate color="info" />
      <small-price-chart v-else />
    </v-col>
    <v-col cols="2" class="d-flex align-center">
      <span class="text-uppercase opacity-70 mr-1">Updated</span>
      <v-skeleton-loader
        v-if="loading"
        type="text"
        max-height="40"
        width="100"
      />
      <span v-else>
        <template v-if="company.reports.length">{{
          company.reports[0]?.updated
        }}</template>
        <template v-else>n/a</template>
      </span>
    </v-col>
    <v-col cols="2" class="d-flex align-center">
      <span class="text-uppercase opacity-70 mr-1">Data</span>
      <v-skeleton-loader
        v-if="loading"
        type="text"
        max-height="40"
        width="150"
      />
      <span v-else class="d-flex align-end">
        <span>Financials</span>
        <v-btn
          class="text-capitalize text-decoration-underline"
          style="margin-bottom: -1px; margin-left: -4px"
          variant="text"
          size="small"
          density="comfortable"
        >
          <company-detail-header-analysts-dialog v-if="totalIdeas > 0" />
          {{ `+ ${totalIdeas} Analysts` }}
        </v-btn>
      </span>
    </v-col>
  </v-row>
</template>
