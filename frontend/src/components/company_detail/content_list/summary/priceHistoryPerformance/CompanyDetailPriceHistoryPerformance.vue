<script setup lang="ts">
// Components
import PriceChart from '@/components/charts/PriceChart.vue'
import CompanyDetailNewsItem from '@/components/company_detail/content_list/summary/news/CompanyDetailNewsItem.vue'
import CompanyDetailShareholderReturnsTable from '@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsTable.vue'
import CompanyDetailStatement from '@/components/company_detail/base/CompanyDetailStatement.vue'
import PriceVolatilityChart from '@/components/charts/PriceVolatilityChart.vue'
import CompanyDetailShareholderReturnsDialog from '@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsDialog.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { usePageStore } from '@/store/page'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'

const companyDetailStore = useCompanyDetailStore()
const pageStore = usePageStore()
const company = computed(() => companyDetailStore.company)
const { t } = useI18n()

function onOpenLateral() {
  companyDetailStore.lateralMenuComponentName = 'news'
  pageStore.extended = true
}
</script>

<template>
  <v-card color="surface-light" class="mb-4 pa-4">
    <v-card-title>History Chart & Performance</v-card-title>
    <v-card-item><price-chart /></v-card-item>

    <v-card-title>Recent News & Updates</v-card-title>
    <v-card-item>
      <v-row>
        <v-col
          v-for="item in company.company_news.slice(0, 6)"
          :key="item.id"
          md="6"
          cols="12"
        >
          <company-detail-news-item :item />
        </v-col>
      </v-row>

      <v-card-actions>
        <v-btn
          color="info"
          block
          variant="tonal"
          @click="onOpenLateral"
          :disabled="pageStore.extended"
        >
          {{ t('buttons.seeMoreUpdates') }}
        </v-btn>
      </v-card-actions>
    </v-card-item>

    <v-card-item>
      <v-row>
        <v-col md="6" cols="12">
          <v-card-title>Shareholder Returns</v-card-title>
          <company-detail-shareholder-returns-table />
          <v-btn color="info" block variant="tonal">
            <company-detail-shareholder-returns-dialog />

            {{ t('buttons.seeFullShareholderReturns') }}
          </v-btn>
          <company-detail-statement name="Is1YearReturnInLineOrAboveIndustry" />
          <company-detail-statement name="Is1YearReturnInLineOrAboveMarket" />
        </v-col>
        <v-col md="6" cols="12">
          <v-card-title>Price Volatility</v-card-title>
          <price-volatility-chart />
          <company-detail-statement name="HasPriceStability" />
          <company-detail-statement
            name="HasReturnsVolatilityImprovedOverPastYear"
          />
        </v-col>
      </v-row>
    </v-card-item>
  </v-card>
</template>
