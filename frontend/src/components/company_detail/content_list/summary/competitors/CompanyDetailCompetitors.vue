<script setup lang="ts">
// Components
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'

const companyDetailStore = useCompanyDetailStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const competitors = computed(() =>
  companyDetailStore.competitors.map((c) => ({
    id: c.id,
    to: c.absolute_url,
    title: c.title,
    ticker: c.ticker,
    market: c.market,
    priceData: c.price_data,
    formatting: c.formatting,
    snowflake: Object.values(c.snowflake),
  }))
)

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
  <v-card
    color="surface-light"
    class="mb-4"
    :title="`${company.ticker} Competitors`"
  >
    <v-card-item>
      <v-container>
        <v-row>
          <v-col v-for="c in competitors" :key="c.id" cols="3">
            <v-card variant="text" :to="c.to">
              <v-card-item>
                <SnowflakeChart
                  :key="`competitor-snowflake-${c.id}`"
                  :chart-data="c.snowflake"
                  small
                />
              </v-card-item>
              <v-card-text class="competitor__title">{{
                c.title
              }}</v-card-text>
              <v-card-text class="competitor__subtitle"
                >{{ c.market.title }}:{{ c.ticker }}</v-card-text
              >
              <v-card-text class="competitor__cap">{{
                humanizeFinancial(
                  c.priceData.capitalisation,
                  c.formatting.primaryCurrencySymbol
                )
              }}</v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-card-item>
  </v-card>
</template>

<style lang="scss" scoped>
.competitor__title,
.competitor__subtitle,
.competitor__cap {
  padding-top: 0;
  padding-bottom: 0.5rem;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}
.competitor__subtitle {
  font-size: 0.85rem;
}
.competitor__cap {
  opacity: 0.5;
}
</style>
