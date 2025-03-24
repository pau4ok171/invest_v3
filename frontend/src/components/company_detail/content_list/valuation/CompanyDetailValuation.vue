<script setup lang="ts">
// Components
import BaseButton from '@/apps/visagiste/components/BaseButton/BaseButton.vue'
import BaseButtonToggle from '@/apps/visagiste/components/BaseButtonToggle/BaseButtonToggle.vue'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseCardItem from '@/apps/visagiste/components/BaseCard/BaseCardItem.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
import BaseCardTitle from '@/apps/visagiste/components/BaseCard/BaseCardTitle.vue'
import BaseCardSubtitle from '@/apps/visagiste/components/BaseCard/BaseCardSubtitle.vue'
import BaseCol from '@/apps/visagiste/components/BaseGrid/BaseCol.vue'
import BaseDivider from '@/apps/visagiste/components/BaseDivider/BaseDivider.vue'
import BaseIcon from '@/apps/visagiste/components/BaseIcon/BaseIcon.vue'
import BaseList from '@/apps/visagiste/components/BaseList/BaseList.vue'
import BaseListItem from '@/apps/visagiste/components/BaseList/BaseListItem.vue'
import BaseRow from '@/apps/visagiste/components/BaseGrid/BaseRow.vue'
import BaseSelect from '@/apps/visagiste/components/BaseSelect/BaseSelect.vue'
import CompanyDetailCheck from '@/components/company_detail/base/CompanyDetailCheck.vue'
import DCFChart from '@/components/charts/DCFChart.vue'
import KeyValuationMetricChart from '@/components/charts/KeyValuationMetricChart.vue'
import KeyValuationMetricTable from '@/components/company_detail/content_list/valuation/KeyValuationMetricTable.vue'
import KeyValuationMetricTabList from '@/components/company_detail/content_list/valuation/KeyValuationMetricTabList.vue'

import MultiplierVsPeersChart from '@/components/charts/MultiplierVsPeersChart.vue'
import HistoricalMultiplierChart from '@/components/charts/HistoricalMultiplierChart.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, ref } from 'vue'

// Types
import type { Statement } from '@/types/statements'
import type { DetailCompany } from '@/types/invest'
import MultiplierVsIndustryChart from '@/components/charts/MultiplierVsIndustryChart.vue'
import MultiplierVsFairChart from '@/components/charts/MultiplierVsFairChart.vue'

export interface FairValueTab {
  name: string
  id: string
  value: number
  metric: string
}

export interface MultiplierTab {
  name: string
  shortName: string
  id: string
  value: number
}

const store = useCompanyDetailStore()
const company = computed<DetailCompany>(() => store.company)
const statements = computed<Statement[]>(() =>
  Object.values(store.statements).filter(
    (s) => s.area === 'VALUE' && s.outcome === 1002
  )
)
const fairValueTabs = computed<Record<string, FairValueTab>>(() => {
  const ticker = company.value.ticker || 'Company'
  return {
    pe: {
      name: 'PE',
      id: 'pe',
      value: 1,
      metric: `As ${ticker} is profitable we use its Price-To-Earnings Ratio for relative valuation analysis`,
    },
    pb: {
      name: 'PB',
      id: 'pb',
      value: 2,
      metric: `For ${ticker} we can also use its Price-To-Book Ratio for relative valuation analysis`,
    },
    ps: {
      name: 'PS',
      id: 'ps',
      value: 3,
      metric: `As ${ticker} is a bank we don’t use its Price-To-Sales Ratio as the key metric for relative valuation analysis`,
    },
    others: {
      name: 'Others',
      id: 'others',
      value: 0,
      metric:
        'Other financial metrics that can be useful for relative valuation',
    },
  }
})
const fairValueSelected = ref(fairValueTabs.value['pe'])

const multiplierTabs = [
  {
    name: 'Price to Earnings',
    shortName: 'PE',
    id: 'price_to_earnings',
    value: 1,
  },
  {
    name: 'Price to Book',
    shortName: 'PB',
    id: 'price_to_book',
    value: 2,
  },
  {
    name: 'Price to Sales',
    shortName: 'PS',
    id: 'price_to_sales',
    value: 3,
  },
]
const peersSelected = ref(multiplierTabs[0])
const historicalSelected = ref(multiplierTabs[0])
const historicalTabSelected = ref([0])
const industrySelected = ref(multiplierTabs[0])

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
  <base-card color="surface" class="mb-4">
    <base-card-item
      class="bg-surface-light"
      title="1 Valuation"
      :subtitle="`Is ${company.ticker || 'Company'} undervalued compared to its fair value, analyst forecasts and its price relative to the market?`"
    >
      <base-card color="surface-bright" width="50%" class="mt-4" flat>
        <base-card-text>Valuation Score {{ passed }}/6</base-card-text>
        <base-card-item>
          <base-list bg-color="surface-bright">
            <base-list-item
              v-for="s in statements"
              :key="s.id"
              density="compact"
              link
              nav
            >
              <template #prepend>
                <base-icon
                  :icon="s.status === 'PASS' ? '$iCheck' : '$iCross'"
                  :color="s.status === 'PASS' ? 'success' : 'error'"
                  class="fill-rule-evenodd"
                />
              </template>
              {{ s.title }}
              <template #append>
                <base-icon icon="$dropdown" />
              </template>
            </base-list-item>
          </base-list>
        </base-card-item>
      </base-card>
    </base-card-item>

    <base-card-item
      title="1.1 Share Price vs Fair Value"
      :subtitle="`What is the Fair Price of ${company.ticker || 'Company'} when looking at its future cash flows? For this estimate we use a Discounted Cash Flow model.`"
    >
      <d-c-f-chart />
      <company-detail-check name="IsUndervaluedBasedOnDCF" />
      <company-detail-check name="IsHighlyUndervaluedBasedOnDCF" />

      <base-divider class="my-4" />
    </base-card-item>

    <base-card-title>1.2 Key Valuation Metric</base-card-title>
    <base-card-subtitle>{{
      `Which metric is best to use when looking at relative valuation for ${company.ticker}?`
    }}</base-card-subtitle>
    <base-card-item>
      <base-row>
        <base-col cols="6">
          <key-valuation-metric-tab-list
            :tabs="fairValueTabs"
            v-model:selected="fairValueSelected"
          />
        </base-col>
        <base-col cols="6">
          <key-valuation-metric-chart
            v-if="fairValueSelected.id !== 'others'"
            :tabs="fairValueTabs"
            :selected="fairValueSelected"
          />
          <key-valuation-metric-table v-else />
        </base-col>
      </base-row>

      <base-divider class="my-4" />
    </base-card-item>

    <base-card-title>{{
      `1.3 ${peersSelected.name} Ratio vs Peers`
    }}</base-card-title>
    <base-card-subtitle>{{
      `How does ${company.ticker}'s ${peersSelected.shortName} Ratio compare to its peers?`
    }}</base-card-subtitle>
    <base-card-item>
      <div style="display: flex; justify-self: flex-end">
        <base-select
          :items="multiplierTabs"
          v-model="peersSelected"
          return-object
          item-value="id"
          item-title="name"
          variant="outlined"
          rounded="xl"
          width="200"
          density="compact"
          hide-details
        />
      </div>

      <multiplier-vs-peers-chart :tabs="multiplierTabs" />

      <company-detail-check
        name="IsGoodValueComparingPriceToEarningsToPeersAverageValue"
      />

      <base-divider class="my-4" />
    </base-card-item>

    <base-card-title>1.4 Historical Price to Earnings Ratio</base-card-title>
    <base-card-subtitle style="white-space: normal">
      Historical Price to Earnings Ratio compares a stock's price to its
      earnings over time. Higher ratios indicate that investors are willing to
      pay more for the stock.
    </base-card-subtitle>

    <base-card-item>
      <base-row>
        <base-col>
          <base-select
            :items="multiplierTabs"
            v-model="historicalSelected"
            return-object
            item-value="id"
            item-title="name"
            variant="outlined"
            rounded="xl"
            width="200"
            density="compact"
            hide-details
          />
        </base-col>

        <base-col>
          <div class="company-detail-valuation__tabs">
            <base-button-toggle
              variant="outlined"
              v-model="historicalTabSelected"
            >
              <base-button text="3M" />
              <base-button text="1Y" />
              <base-button text="3Y" />
              <base-button text="5Y" />
            </base-button-toggle>
          </div>
        </base-col>
      </base-row>

      <historical-multiplier-chart />

      <base-divider class="my-4" />
    </base-card-item>

    <base-card-title>1.5 Price to Earnings Ratio vs Industry</base-card-title>
    <base-card-subtitle>{{
      `How does ${company.ticker}'s PE Ratio compare vs other companies in the European Banks Industry?`
    }}</base-card-subtitle>
    <base-card-item>
      <base-select
        :items="multiplierTabs"
        v-model="industrySelected"
        return-object
        item-value="id"
        item-title="name"
        variant="outlined"
        rounded="xl"
        width="200"
        density="compact"
        hide-details
      />

      <multiplier-vs-industry-chart />

      <company-detail-check
        name="IsGoodValueComparingPriceToEarningsToIndustry"
      />

      <base-divider class="my-4" />
    </base-card-item>

    <base-card-title>1.6 Price to Earnings Ratio vs Fair Ratio</base-card-title>
    <base-card-subtitle style="white-space: normal">{{
      `What is ${company.ticker}'s PE Ratio compared to its Fair PE Ratio? This is the expected PE Ratio taking into account the company's forecast earnings growth, profit margins and other risk factors.`
    }}</base-card-subtitle>
    <base-card-item>
      <multiplier-vs-fair-chart />

      <company-detail-check name="IsGoodValueComparingRatioToFairRatio" />

      <base-divider class="my-4" />
    </base-card-item>

    <base-card-title>1.7 Analyst Price Targets</base-card-title>
    <base-card-subtitle
      >What is the analyst 12-month forecast and do we have any statistical
      confidence in the consensus price target?</base-card-subtitle
    >
    <base-card-item>
      <div
        style="
          height: 500px;
          display: flex;
          justify-content: center;
          align-items: center;
        "
      >
        [ANALYST PRICE TARGETS CHART]
      </div>
    </base-card-item>
  </base-card>
</template>

<style lang="scss">
.fill-rule-evenodd {
  > svg > path {
    fill-rule: evenodd;
  }
}
.company-detail-valuation__tabs {
  display: flex;
  justify-content: flex-end;
}
</style>
