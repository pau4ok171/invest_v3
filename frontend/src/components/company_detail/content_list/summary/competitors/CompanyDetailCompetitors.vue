<script setup lang="ts">
// Components
import BaseContainer from '@/apps/visagiste/components/BaseGrid/BaseContainer.vue'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseRow from '@/apps/visagiste/components/BaseGrid/BaseRow.vue'
import BaseCol from '@/apps/visagiste/components/BaseGrid/BaseCol.vue'
import BaseCardItem from '@/apps/visagiste/components/BaseCard/BaseCardItem.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
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
  <base-card
    color="surface-light"
    class="mb-4"
    :title="`${company.ticker} Competitors`"
  >
    <base-card-item>
      <base-container>
        <base-row>
          <base-col v-for="c in competitors" :key="c.id" cols="3">
            <base-card variant="text" :to="c.to">
              <base-card-item>
                <SnowflakeChart
                  :key="`competitor-snowflake-${c.id}`"
                  :chart-data="c.snowflake"
                  small
                />
              </base-card-item>
              <base-card-text class="competitor__title">{{
                c.title
              }}</base-card-text>
              <base-card-text class="competitor__subtitle"
                >{{ c.market.title }}:{{ c.ticker }}</base-card-text
              >
              <base-card-text class="competitor__cap">{{
                humanizeFinancial(
                  c.priceData.capitalisation,
                  c.formatting.primaryCurrencySymbol
                )
              }}</base-card-text>
            </base-card>
          </base-col>
        </base-row>
      </base-container>
    </base-card-item>
  </base-card>
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
