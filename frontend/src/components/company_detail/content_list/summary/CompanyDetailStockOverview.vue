<script setup lang="ts">
// Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import SnowflakeChart from '@/components/charts/SnowflakeChart.vue'
import CompanyDetailRiskReward from '@/components/company_detail/content_list/summary/CompanyDetailRiskReward.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

// Types
import type { DetailCompany } from '@/types/invest'
import BaseCard from "@/apps/visagiste/components/BaseCard/BaseCard.vue";
import BaseCardTitle from "@/apps/visagiste/components/BaseCard/BaseCardTitle.vue";
import BaseContainer from "@/apps/visagiste/components/BaseGrid/BaseContainer.vue";
import BaseCol from "@/apps/visagiste/components/BaseGrid/BaseCol.vue";
import BaseRow from "@/apps/visagiste/components/BaseGrid/BaseRow.vue";
import BaseCardText from "@/apps/visagiste/components/BaseCard/BaseCardText.vue";
import BaseCardActions from "@/apps/visagiste/components/BaseCard/BaseCardActions.vue";

const companyDetailStore = useCompanyDetailStore()
const company = computed<DetailCompany>(() => companyDetailStore.company)
const snowflake = computed(() => companyDetailStore.snowflake)

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
  <base-card color="surface-light" class="mb-4">
    <base-container>
      <base-row>
        <base-col cols="7">
          <base-card-title>{{ company.ticker }} Stock Overview</base-card-title>
          <base-card-text>{{ company.short_description }}</base-card-text>
          <base-card-actions>
            <base-button
              prepend-icon="$iInfo"
              text="about the company"
              variant="plain"
              color="info"
              size="small"
              @click="onAboutCompanyClick"
            />
          </base-card-actions>
        </base-col>
        <base-col>
          <SnowflakeChart :chartData="snowflake as number[]" />
        </base-col>
      </base-row>
      <base-row>
        <base-col cols="12">
          <CompanyDetailRiskReward />
        </base-col>
      </base-row>
    </base-container>
  </base-card>
</template>
