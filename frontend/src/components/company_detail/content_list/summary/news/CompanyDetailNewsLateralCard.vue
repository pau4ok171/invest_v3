<script setup lang="ts">
// Components
import CompanyDetailNewsItem from '@/components/company_detail/content_list/summary/news/CompanyDetailNewsItem.vue'

// Composables
import { usePageStore } from '@/store/page'
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

const pageStore = usePageStore()
const store = useCompanyDetailStore()
const news = computed(() => store.company.company_news)
</script>

<template>
  <v-card height="100%">
    <v-toolbar title="Recent News and Updates" color="surface">
      <template #append>
        <v-btn
          icon="$close"
          size="small"
          density="comfortable"
          rounded="lg"
          @click="pageStore.extended = false"
        />
      </template>
    </v-toolbar>
    <div style="overflow-y: auto; height: calc(100% - 88px)">
      <v-card-item v-for="n in news" :key="`lateral-news-${n.id}`">
        <company-detail-news-item :item="n" />
      </v-card-item>
    </div>
  </v-card>
</template>
