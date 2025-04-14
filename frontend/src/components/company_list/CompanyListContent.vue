<script setup lang="ts">
// Components
import CompanyListContentTableMode from '@/components/company_list/CompanyListContentTableMode.vue'
import CompanyListContentTileMode from '@/components/company_list/CompanyListContentTileMode.vue'

// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'
import { useAuthStore } from '@/store/auth'

// Utilities
import { computed } from 'vue'

// Types
import type { CompanyItem } from '@/store/companyList/types'

const store = useCompanyListStore()
const authStore = useAuthStore()

const items = computed<CompanyItem[]>(
  () =>
    store.companies.map((c) => ({
      companyLogo: c.logo_url,
      companyName: c.title,
      lastPrice: `${c.formatting.primaryCurrencySymbol}${c.price_data.last_price?.toFixed(2)}`,
      return7D: `${c.return_1y.toFixed(2)}%`,
      return1Y: `${c.return_7d.toFixed(2)}%`,
      marketCap: humanize(
        c.price_data.capitalisation,
        c.formatting.primaryCurrencySymbol
      ),
      consensus: 'TBA',
      fairValue: 'TBA',
      growth: 'TBA',
      dividendYield: 'TBA',
      sector: c.sector.title,
      ticker: c.ticker,
      to: c.absolute_url,
      uid: c.uid,
      watchlisted: c.is_watchlisted,
    })) as CompanyItem[]
)

function humanize(val: number = 0, currencyUnit: string = '') {
  if (val === 0) return 'n/a'
  for (const unit of ['', 't', 'M', 'B', 'T']) {
    if (Math.abs(val) < 1000) return currencyUnit + val.toFixed(2) + unit
    val /= 1000
  }
  return currencyUnit + val.toFixed(2) + 'Q'
}
</script>

<template>
  <v-infinite-scroll
    @load="store.fetchCompanies"
    empty-text=""
    class="overflow-y-hidden"
  >
    <company-list-content-table-mode
      v-if="store.contentMode === 'table'"
      :items
    />
    <company-list-content-tile-mode v-else :items />
  </v-infinite-scroll>
</template>

<style lang="scss"></style>
