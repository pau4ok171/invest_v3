<script setup lang="ts">
// Components
import CompanyDetailRiskReward from '@/components/company_detail/content_list/summary/overview/CompanyDetailRiskReward.vue'
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'
import { useTranslations } from '@/composables/translations'

// Utilities
import { computed } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'

const companyDetailStore = useCompanyDetailStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const snowflake = computed(() => companyDetailStore.snowflake)
const { t } = useI18n()
const { getTranslation } = useTranslations()

function onAboutCompanyClick() {
  const goTo = (document as Document)
    ?.querySelector('#about-company-section')
    ?.getBoundingClientRect()

  if (!goTo) return

  const windowScroll = document.documentElement.scrollTop
  const scrollTop = goTo.top + windowScroll - 80
  window.scrollTo({ top: scrollTop, behavior: 'smooth' })
}
</script>

<template>
  <v-card color="surface-light" class="mb-4">
    <v-container>
      <v-row>
        <v-col md="7" cols="12">
          <v-card-title>
            {{
              `${company.ticker} ${t('companyDetail.overview.stockOverview.header')}`
            }}
          </v-card-title>
          <v-card-text>{{
            getTranslation(company.translations, 'short_description')
          }}</v-card-text>
          <v-card-actions>
            <v-btn
              prepend-icon="$iInfo"
              :text="t('buttons.aboutTheCompany')"
              variant="plain"
              color="info"
              size="small"
              @click="onAboutCompanyClick"
            />
          </v-card-actions>
        </v-col>
        <v-col>
          <snowflake-chart :data="snowflake" size="280" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <company-detail-risk-reward />
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>
