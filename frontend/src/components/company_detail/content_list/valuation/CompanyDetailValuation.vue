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
import AnalystPriceTargetsChart from '@/components/charts/AnalystPriceTargetsChart.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref, watch } from 'vue'

// Types
import type { Statement } from '@/types/statements'
import type { DetailCompany } from '@/types/invest'

export interface FairValueTab {
  name: string
  id: string
  value: number
}

export interface MultiplierTab {
  name: string
  shortName: string
  id: string
  value: number
}

const store = useCompanyDetailStore()
const company = computed<DetailCompany>(() => store.company)
const { t, locale } = useI18n()
const statements = computed<Statement[]>(() =>
  Object.values(store.statements).filter(
    (s) => s.area === 'VALUE' && s.outcome === 1002
  )
)
const fairValueTabs = computed<FairValueTab[]>(() => {
  return [
    {
      name: 'PE',
      id: 'pe',
      value: 1,
    },
    {
      name: 'PB',
      id: 'pb',
      value: 2,
    },
    {
      name: 'PS',
      id: 'ps',
      value: 3,
    },
    {
      name: t('buttons.others'),
      id: 'other',
      value: 0,
    },
  ]
})
const fairValueSelected = ref(fairValueTabs.value[0])

const multiplierTabs = computed<MultiplierTab[]>(() => [
  {
    name: t('finance.pe'),
    shortName: 'PE',
    id: 'pe',
    value: 1,
  },
  {
    name: t('finance.pb'),
    shortName: 'PB',
    id: 'pb',
    value: 2,
  },
  {
    name: t('finance.ps'),
    shortName: 'PS',
    id: 'ps',
    value: 3,
  },
])
const peersSelected = ref<MultiplierTab>(multiplierTabs.value[0])
const historicalSelected = ref<MultiplierTab>(multiplierTabs.value[0])
const historicalTabSelected = ref([0])
const industrySelected = ref<MultiplierTab>(multiplierTabs.value[0])

const passed = computed(() =>
  statements.value.reduce((acc, s) => {
    if (s.status === 'PASS') {
      acc += 1
    }
    return acc
  }, 0)
)

watch(locale, () => {
  peersSelected.value.name = t(`finance.${peersSelected.value.id}`)
  historicalSelected.value.name = t(`finance.${historicalSelected.value.id}`)
  industrySelected.value.name = t(`finance.${industrySelected.value.id}`)
})
</script>

<template>
  <v-card color="surface-light" class="mb-4">
    <v-card-item
      class="bg-surface pt-8 px-8"
      :title="`1 ${t('companyDetail.valuation.title')}`"
      :subtitle="
        t('companyDetail.valuation.subtitle', { ticker: company.ticker })
      "
    >
      <v-row>
        <v-col md="6" cols="12">
          <v-card color="surface-bright" width="100%" class="mt-4" flat>
            <v-card-text>{{
              `${t('companyDetail.valuation.score')} ${passed}/6`
            }}</v-card-text>
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
      :title="`1.1 ${t('companyDetail.valuation.shareFairValue.title')}`"
      :subtitle="
        t('companyDetail.valuation.shareFairValue.subtitle', {
          ticker: company.ticker,
        })
      "
      class="pt-8 px-8"
    >
      <d-c-f-chart />
      <company-detail-check name="IsUndervaluedBasedOnDCF" />
      <company-detail-check name="IsHighlyUndervaluedBasedOnDCF" />

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      :title="`1.2 ${t('companyDetail.valuation.keyValuationMetric.title')}`"
      :subtitle="
        t('companyDetail.valuation.keyValuationMetric.subtitle', {
          ticker: company.ticker,
        })
      "
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
            v-if="fairValueSelected.id !== 'other'"
            :tabs="fairValueTabs"
            :selected="fairValueSelected"
          />
          <key-valuation-metric-table v-else />
        </v-col>
      </v-row>

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      :title="`1.3 ${t('companyDetail.valuation.peVsPeers.title', { selected: peersSelected.name })}`"
      :subtitle="`${t('companyDetail.valuation.peVsPeers.subtitle', { ticker: company.ticker, selected: peersSelected.shortName })}`"
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
          max-width="fit-content"
          density="compact"
          hide-details
        />
      </div>

      <multiplier-vs-peers-chart
        :tabs="multiplierTabs"
        :activeTab="peersSelected"
      />

      <company-detail-check
        name="IsGoodValueComparingPriceToEarningsToPeersAverageValue"
      />

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      :title="`1.4 ${t('companyDetail.valuation.historicalPE.title')}`"
      :subtitle="t('companyDetail.valuation.historicalPE.subtitle')"
      class="px-8"
    >
      <v-row class="mb-0 mt-4">
        <v-col>
          <v-select
            :items="multiplierTabs"
            v-model="historicalSelected"
            return-object
            item-value="id"
            item-title="name"
            variant="outlined"
            rounded="xl"
            max-width="fit-content"
            density="compact"
            hide-details
          />
        </v-col>

        <v-col>
          <div class="d-flex justify-start justify-sm-end">
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
      :title="`1.5 ${t('companyDetail.valuation.peVsIndustry.title')}`"
      :subtitle="`${t('companyDetail.valuation.peVsIndustry.subtitle', { ticker: company.ticker, sector: '[SECTOR]' })}`"
      class="px-8"
    >
      <v-select
        class="my-4"
        :items="multiplierTabs"
        v-model="industrySelected"
        return-object
        item-value="id"
        item-title="name"
        variant="outlined"
        rounded="xl"
        max-width="fit-content"
        density="compact"
        hide-details
      />

      <multiplier-vs-industry-chart />

      <company-detail-check
        name="IsGoodValueComparingPriceToEarningsToIndustry"
      />

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      :title="`1.6 ${t('companyDetail.valuation.peVsFair.title')}`"
      :subtitle="
        t('companyDetail.valuation.peVsFair.subtitle', {
          ticker: company.ticker,
        })
      "
      class="px-8"
    >
      <multiplier-vs-fair-chart />

      <company-detail-check name="IsGoodValueComparingRatioToFairRatio" />

      <v-divider class="my-4" />
    </v-card-item>

    <v-card-item
      :title="`1.7 ${t('companyDetail.valuation.analystsPriceTargets.title')}`"
      :subtitle="t('companyDetail.valuation.analystsPriceTargets.subtitle')"
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
</style>
