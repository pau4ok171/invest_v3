<script setup lang="ts">
// Components
import PriceChart from '@/components/charts/PriceChart.vue'
import CompanyDetailNewsItem from '@/components/company_detail/content_list/summary/news/CompanyDetailNewsItem.vue'
import CompanyDetailShareholderReturnsTable
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsTable.vue";
import CompanyDetailStatement from "@/components/company_detail/base/CompanyDetailStatement.vue";
import PriceVolatilityChart from "@/components/charts/PriceVolatilityChart.vue";
import CompanyDetailShareholderReturnsDialog
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsDialog.vue";

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

const companyDetailStore = useCompanyDetailStore()
const company = computed(() => companyDetailStore.company)
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
            cols="6"
          >
            <company-detail-news-item :item />
          </v-col>
        </v-row>

        <v-card-actions>
          <!-- TODO: Create Dialog for news on CompanyDetailPriceHistoryPerformance -->
          <v-btn color="info" block variant="tonal">
            see more updates
          </v-btn>
        </v-card-actions>
    </v-card-item>

    <v-card-item>
      <v-row>
        <v-col cols="6">
          <v-card-title>Shareholder Returns</v-card-title>
          <company-detail-shareholder-returns-table />
          <v-btn color="info" block variant="tonal" >
            <company-detail-shareholder-returns-dialog/>

            See full shareholder returns
          </v-btn>
          <company-detail-statement name="Is1YearReturnInLineOrAboveIndustry" />
          <company-detail-statement name="Is1YearReturnInLineOrAboveMarket" />
        </v-col>
        <v-col cols="6">
          <v-card-title>Price Volatility</v-card-title>
          <price-volatility-chart/>
          <company-detail-statement name="HasPriceStability" />
          <company-detail-statement name="HasReturnsVolatilityImprovedOverPastYear" />
        </v-col>
      </v-row>
    </v-card-item>
  </v-card>
</template>
