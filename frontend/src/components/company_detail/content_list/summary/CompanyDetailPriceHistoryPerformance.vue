<script setup lang="ts">
// Components
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseCardTitle from '@/apps/visagiste/components/BaseCard/BaseCardTitle.vue'
import BaseCardItem from '@/apps/visagiste/components/BaseCard/BaseCardItem.vue'
import PriceChart from '@/components/charts/PriceChart.vue'
import BaseRow from '@/apps/visagiste/components/BaseGrid/BaseRow.vue'
import BaseCol from '@/apps/visagiste/components/BaseGrid/BaseCol.vue'
import CompanyDetailNewsItem from '@/components/company_detail/content_list/summary/news/CompanyDetailNewsItem.vue'
import BaseCardActions from '@/apps/visagiste/components/BaseCard/BaseCardActions.vue'
import BaseButton from '@/apps/visagiste/components/BaseButton/BaseButton.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'
import CompanyDetailShareholderReturnsTable
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsTable.vue";
import CompanyDetailStatement from "@/components/company_detail/content_list/CompanyDetailStatement.vue";
import PriceVolatilityChart from "@/components/charts/PriceVolatilityChart.vue";
import BaseDialog from "@/apps/visagiste/components/BaseDialog/BaseDialog.vue";
import CompanyDetailShareholderReturnsDialog
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsDialog.vue";

const companyDetailStore = useCompanyDetailStore()
const company = computed(() => companyDetailStore.company)
</script>

<template>
  <base-card color="surface-light" class="mb-4">
    <base-card-title>History Chart & Performance</base-card-title>
    <base-card-item><PriceChart /></base-card-item>

    <base-card-title>Recent News & Updates</base-card-title>
    <base-card-item>
        <base-row>
          <base-col
            v-for="item in company.company_news.slice(0, 6)"
            :key="item.id"
            cols="6"
          >
            <company-detail-news-item :item />
          </base-col>
        </base-row>

        <base-card-actions>
          <!-- TODO: Create Dialog for news on CompanyDetailPriceHistoryPerformance -->
          <base-button color="info" block variant="tonal">
            see more updates
          </base-button>
        </base-card-actions>
    </base-card-item>

    <base-card-item>
      <base-row>
        <base-col cols="6">
          <base-card-title>Shareholder Returns</base-card-title>
          <company-detail-shareholder-returns-table />
          <base-button color="info" block variant="tonal" >
            <company-detail-shareholder-returns-dialog/>

            See full shareholder returns
          </base-button>
          <company-detail-statement name="Is1YearReturnInLineOrAboveIndustry" />
          <company-detail-statement name="Is1YearReturnInLineOrAboveMarket" />
        </base-col>
        <base-col cols="6">
          <base-card-title>Price Volatility</base-card-title>
          <price-volatility-chart/>
          <company-detail-statement name="HasPriceStability" />
          <company-detail-statement name="HasReturnsVolatilityImprovedOverPastYear" />
        </base-col>
      </base-row>
    </base-card-item>
  </base-card>
</template>
