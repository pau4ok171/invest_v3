<script setup lang="ts">
// Components
import SmallPriceChart from '@/components/charts/SmallPriceChart.vue'
import CompanyDetailHeaderAnalystsDialog from '@/components/company_detail/header/CompanyDetailHeaderAnalystsDialog.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, inject } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'
import type { ActiveAnimations } from '@/composables/priceUpdater'

const companyDetailStore = useCompanyDetailStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const loading = computed(() => companyDetailStore.fetchingCompany)
const { t } = useI18n()

const totalIdeas = computed(() => company.value.analyst_ideas.length)

const activeAnimations = inject<ActiveAnimations>('activeAnimations') || {}

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
    style="font-size: 0.75rem"
    class="company-detail-header__info mb-1"
    align-content="center"
  >
    <v-col lg="auto" cols="2" class="d-flex flex-column">
      <v-skeleton-loader v-if="loading" type="text" max-height="40" />
      <template v-else>
        <span class="text-uppercase opacity-70">{{
          t('companyDetail.header.lastPrice')
        }}</span>
        <span
          :class="[
            'price',
            {
              'price-positive': activeAnimations[company.slug] === 'up',
              'price-negative': activeAnimations[company.slug] === 'down',
            },
          ]"
          >{{
            `${company.formatting.primaryCurrencySymbol}${company.price_data.last_price?.toFixed(2)}`
          }}</span
        >
      </template>
    </v-col>
    <v-col lg="auto" cols="2" class="d-flex flex-column">
      <v-skeleton-loader v-if="loading" type="text" max-height="40" />
      <template v-else>
        <span class="text-uppercase opacity-70">{{
          t('companyDetail.header.marketCap')
        }}</span>
        <span>{{
          humanize(
            company.price_data.capitalisation,
            company.formatting.primaryCurrencySymbol
          )
        }}</span>
      </template>
    </v-col>
    <v-col lg="auto" cols="2" class="d-flex flex-column">
      <v-skeleton-loader v-if="loading" type="text" max-height="40" />
      <template v-else>
        <span class="text-uppercase opacity-70">{{
          t('companyDetail.header.return7d')
        }}</span>
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
    <v-col lg="auto" cols="2" class="d-flex flex-column">
      <v-skeleton-loader v-if="loading" type="text" max-height="40" />
      <template v-else>
        <span class="text-uppercase opacity-70">{{
          t('companyDetail.header.return1y')
        }}</span>
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
    <v-col lg="auto" cols="12" class="d-flex justify-lg-center">
      <div v-if="loading" class="d-flex justify-center" style="width: 300px">
        <v-progress-circular indeterminate color="info" />
      </div>
      <small-price-chart style="width: 200px" v-else />
    </v-col>
    <v-col lg="2" cols="3" class="d-flex align-center">
      <span class="text-uppercase opacity-70 mr-1">{{
        t('common.updated')
      }}</span>
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
    <v-col lg="auto" cols="auto" class="d-flex align-center">
      <span class="text-uppercase opacity-70 mr-1">
        {{ t('companyDetail.header.data') }}
      </span>
      <v-skeleton-loader
        v-if="loading"
        type="text"
        max-height="40"
        width="150"
      />
      <span v-else class="d-flex align-end">
        <span>{{ t('companyDetail.header.companyFinancials') }}</span>
        <v-btn
          v-if="totalIdeas > 0"
          class="text-capitalize text-decoration-underline"
          style="margin-bottom: -1px; margin-left: -4px"
          variant="text"
          size="small"
          density="comfortable"
        >
          <company-detail-header-analysts-dialog />
          {{ `+ ${t('buttons.analysts', { n: totalIdeas })}` }}
        </v-btn>
      </span>
    </v-col>
  </v-row>
</template>

<style lang="scss">
.company-detail-header__info {
  .price {
    padding: 4px;
    border-radius: 4px;
    color: inherit;
    transition: color 0.4s ease-in-out;
  }
  .price-positive {
    color: rgb(var(--v-theme-success));
  }
  .price-negative {
    color: rgb(var(--v-theme-error));
  }
}
</style>
