<script setup lang="ts">
// Components
import SmallPriceChart from '@/components/charts/SmallPriceChart.vue'
import CompanyDetailHeaderInfoItem from '@/components/company_detail/header/CompanyDetailHeaderInfoItem.vue'
import CompanyDetailHeaderAnalystsButtonModalMenuContainer from '@/components/company_detail/header/CompanyDetailHeaderAnalystModalMenuContainer.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'
import type { DetailCompany } from '@/types/invest'

const companyDetailStore = useCompanyDetailStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const loading = computed(() => companyDetailStore.fetchingCompany)

const totalIdeas = computed(() => company.value.analyst_ideas.length)

function humanizeFinancial(
  val: number = 0,
  currencySymbol: string = ''
): string {
  if (val === 0) return 'n/a'
  for (const unit of ['', 't', 'M', 'B', 'T']) {
    if (Math.abs(val) < 1000) return currencySymbol + val.toFixed(2) + unit
    val /= 1000
  }
  return currencySymbol + val.toFixed(2) + 'Q'
}
</script>

<template>
  <div class="detail-header__info-panel" v-if="company.price_data">
    <v-skeleton-loader
      v-if="loading"
      type="text"
      width="100"
      max-height="44"
    />
    <CompanyDetailHeaderInfoItem v-else key="info-price">
      <template v-slot:title><p>Last price</p></template>
      <template v-slot:value>
        <span>
          {{ company.formatting.primaryCurrencySymbol
          }}{{ company.price_data.last_price?.toFixed(2) }}
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <v-skeleton-loader
      v-if="loading"
      type="text"
      width="100"
      max-height="44"
    />
    <CompanyDetailHeaderInfoItem v-else key="info-cap">
      <template v-slot:title><p>Market cap</p></template>
      <template v-slot:value>
        <span>
          {{
            humanizeFinancial(
              company.price_data.capitalisation,
              company.formatting.primaryCurrencySymbol
            )
          }}
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <v-skeleton-loader
      v-if="loading"
      type="text"
      width="100"
      max-height="44"
    />
    <CompanyDetailHeaderInfoItem v-else key="info-7D">
      <template v-slot:title><p>7D</p></template>
      <template v-slot:value>
        <span
          :class="[
            company.return_7d && company.return_7d > 0
              ? 'detail-header__success-color'
              : 'detail-header__error-color',
          ]"
        >
          {{ company.return_7d?.toFixed(2) }}%
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <v-skeleton-loader
      v-if="loading"
      type="text"
      width="100"
      max-height="44"
    />
    <CompanyDetailHeaderInfoItem v-else key="info-1Y">
      <template v-slot:title><p>1Y</p></template>
      <template v-slot:value>
        <span
          :class="[
            company.return_1y && company.return_1y > 0
              ? 'detail-header__success-color'
              : 'detail-header__error-color',
          ]"
        >
          {{ company.return_1y && company.return_1y.toFixed(2) }}%
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <CompanyDetailHeaderInfoItem key="info-chart">
      <div
        v-if="loading"
        class="w-100 d-flex justify-center align-center bg-surface"
        style="height: 44px"
      >
        <v-progress-circular indeterminate />
      </div>
      <SmallPriceChart v-else />
    </CompanyDetailHeaderInfoItem>

    <CompanyDetailHeaderInfoItem nowrap small key="info-updated">
      <template v-slot:title><p>Updated</p></template>
      <template v-slot:value>
        <v-skeleton-loader v-if="loading" type="text" />
        <span v-else>
          <template v-if="company.reports.length">{{
            company.reports[0]?.updated
          }}</template>
          <template v-else>n/a</template>
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>

    <CompanyDetailHeaderInfoItem nowrap on-row small key="info-data">
      <template v-slot:title><p>Data</p></template>
      <template v-slot:value>
        <v-skeleton-loader v-if="loading" type="text" width="150" />
        <span v-else class="detail-header__info-panel-total-ideas d-flex">
          <span>Financials</span>
          <template v-if="totalIdeas > 0">
            <span class="mx-1">+</span>
            <CompanyDetailHeaderAnalystsButtonModalMenuContainer />
          </template>
        </span>
      </template>
    </CompanyDetailHeaderInfoItem>
  </div>
</template>

<style lang="scss" scoped>
.detail-header__info-panel {
  display: grid;
  grid-template: 44px / repeat(4, min-content) 2fr 1fr 1fr;
  gap: 16px;
}
.detail-header__info-panel-total-ideas {
  align-items: flex-end;
}
.detail-header__error-color {
  color: rgb(var(--v-theme-success));
}
.detail-header__success-color {
  color: rgb(var(--v-theme-error));
}
</style>
