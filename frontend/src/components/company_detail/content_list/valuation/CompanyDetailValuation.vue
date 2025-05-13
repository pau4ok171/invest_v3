<script setup lang="ts">
// Components
import CompanyDetailCheck from '@/components/company_detail/base/CompanyDetailCheck.vue'
import DCFChart from '@/components/charts/DCFChart.vue'
import KeyValuationMetricChart from '@/components/charts/KeyValuationMetricChart.vue'
import KeyValuationMetricTable from '@/components/company_detail/content_list/valuation/KeyValuationMetricTable.vue'
import KeyValuationMetricTabList from '@/components/company_detail/content_list/valuation/KeyValuationMetricTabList.vue'
import MultiplierVsPeersChart from '@/components/charts/MultiplierVsPeersChart.vue'
import HistoricalMultiplierChart from '@/components/charts/HistoricalMultiplierChart.vue'
import MultiplierVsIndustryChart from '@/components/charts/MultiplierVsIndustryChart.vue'
import MultiplierVsFairChart from '@/components/charts/MultiplierVsFairChart.vue'
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, ref } from 'vue'

// Types
import type { Statement } from '@/types/statements'
import type { DetailCompany } from '@/types/invest'
import AnalystPriceTargetsChart from "@/components/charts/AnalystPriceTargetsChart.vue";

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
const fairValueTabs = computed<FairValueTab[]>(() => {
  const ticker = company.value.ticker || 'Company'
  return [
    {
      name: 'PE',
      id: 'pe',
      value: 1,
      metric: `As ${ticker} is profitable we use its Price-To-Earnings Ratio for relative valuation analysis`,
    },
    {
      name: 'PB',
      id: 'pb',
      value: 2,
      metric: `For ${ticker} we can also use its Price-To-Book Ratio for relative valuation analysis`,
    },
    {
      name: 'PS',
      id: 'ps',
      value: 3,
      metric: `As ${ticker} is a bank we don’t use its Price-To-Sales Ratio as the key metric for relative valuation analysis`,
    },
    {
      name: 'Others',
      id: 'others',
      value: 0,
      metric:
        'Other financial metrics that can be useful for relative valuation',
    },
  ]
})
const fairValueSelected = ref(fairValueTabs.value[0])

const multiplierTabs: MultiplierTab[] = [
  {
    name: 'Price to Earnings',
    shortName: 'PE',
    id: 'pe',
    value: 1,
  },
  {
    name: 'Price to Book',
    shortName: 'PB',
    id: 'pb',
    value: 2,
  },
  {
    name: 'Price to Sales',
    shortName: 'PS',
    id: 'ps',
    value: 3,
  },
]
const peersSelected = ref<MultiplierTab>(multiplierTabs[0])
const historicalSelected = ref<MultiplierTab>(multiplierTabs[0])
const historicalTabSelected = ref([0])
const industrySelected = ref<MultiplierTab>(multiplierTabs[0])

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
      title="1 Valuation"
      :subtitle="`Is ${company.ticker || 'Company'} undervalued compared to its fair value, analyst forecasts and its price relative to the market?`"
    >
      <v-row>
        <v-col md="6" cols="12">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>Valuation Score {{ passed }}/6</v-card-text>
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

        <v-col md="6" sm="12">
          <snowflake-chart
            :data="store.snowflake"
            size="200"
            :interactive="false"
          />
        </v-col>
      </v-row>
    </v-card-item>

    <v-card-item
      title="1.1 Share Price vs Fair Value"
      :subtitle="`What is the Fair Price of ${company.ticker || 'Company'} when looking at its future cash flows? For this estimate we use a Discounted Cash Flow model.`"
      class="pt-8 px-8"
    >
      <d-c-f-chart />
      <company-detail-check name="IsUndervaluedBasedOnDCF" />
      <company-detail-check name="IsHighlyUndervaluedBasedOnDCF" />

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      title="1.2 Key Valuation Metric"
      :subtitle="`Which metric is best to use when looking at relative valuation for ${company.ticker}?`"
      class="px-8"
    >
      <v-row>
        <v-col md="6" cols="12">
          <key-valuation-metric-tab-list
            :tabs="fairValueTabs"
            v-model:selected="fairValueSelected"
          />
        </v-col>
        <v-col md="6" cols="12">
          <key-valuation-metric-chart
            v-if="fairValueSelected.id !== 'others'"
            :tabs="fairValueTabs"
            :selected="fairValueSelected"
          />
          <key-valuation-metric-table v-else />
        </v-col>
      </v-row>

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      :title="`1.3 ${peersSelected.name} Ratio vs Peers`"
      :subtitle="`How does ${company.ticker}'s ${peersSelected.shortName} Ratio compare to its peers?`"
      class="px-8"
    >
      <div style="display: flex; justify-self: flex-start">
        <v-select
          class="my-4"
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

      <multiplier-vs-peers-chart :tabs="multiplierTabs" :activeTab="peersSelected" />

      <company-detail-check
        name="IsGoodValueComparingPriceToEarningsToPeersAverageValue"
      />

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item title="1.4 Historical Price to Earnings Ratio" class="px-8">
      <template #subtitle>
        <span style="white-space: normal">
          Historical Price to Earnings Ratio compares a stock's price to its
          earnings over time. Higher ratios indicate that investors are willing
          to pay more for the stock.
        </span>
      </template>
      <v-row class="mb-0">
        <v-col>
          <v-select
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
        </v-col>

        <v-col>
          <div class="company-detail-valuation__tabs">
            <v-btn-toggle
              variant="outlined"
              v-model="historicalTabSelected"
              density="comfortable"
              mandatory
              selected-class="text-info"
            >
              <v-btn text="3M" />
              <v-btn text="1Y" />
              <v-btn text="3Y" />
              <v-btn text="5Y" />
            </v-btn-toggle>
          </div>
        </v-col>
      </v-row>

      <historical-multiplier-chart />

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      title="1.5 Price to Earnings Ratio vs Industry"
      :subtitle="`How does ${company.ticker}'s PE Ratio compare vs other companies in the European Banks Industry?`"
      class="px-8"
    >
      <v-select
        class="mb-4"
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

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item title="1.6 Price to Earnings Ratio vs Fair Ratio" class="px-8">
      <template #subtitle>
        <span style="white-space: normal">
          {{
            `What is ${company.ticker}'s PE Ratio compared to its Fair PE Ratio? This is the expected PE Ratio taking into account the company's forecast earnings growth, profit margins and other risk factors.`
          }}
        </span>
      </template>
      <multiplier-vs-fair-chart />

      <company-detail-check name="IsGoodValueComparingRatioToFairRatio" />

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      title="1.7 Analyst Price Targets"
      subtitle="What is the analyst 12-month forecast and do we have any statistical confidence in the consensus price target?"
      class="px-8"
    >
      <analyst-price-targets-chart />

      <company-detail-check name="IsAnalystForecastTrustworthy" />
    </v-card-item>
  </v-card>
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
