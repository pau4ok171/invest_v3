<script setup lang="ts">
// Components
import CompanyDetailHeader from '@/components/company_detail/header/CompanyDetailHeader.vue'
import CompanyDetailContent from '@/components/company_detail/CompanyDetailContent.vue'
import CompanyDetailRightSidebar from '@/components/company_detail/rightSidebar/companyDetailRightSidebar.vue'
import NotesEditor from '@/components/company_detail/content_list/summary/notes/NotesEditor.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { usePageStore } from '@/store/page'
import { useRoute } from 'vue-router'

// Utilities
import { onMounted, watch } from 'vue'
import { RouteNamesEnum } from '@/router/routes.types'

const route = useRoute()
const pageStore = usePageStore()
const companyDetailStore = useCompanyDetailStore()

async function init() {
  const companySlug = route.params?.companySlug as string

  pageStore.loading = true

  await companyDetailStore.fetchCompany(companySlug)
  await companyDetailStore.fetchPriceData(companySlug)

  pageStore.loading = false

  document.title = `${companyDetailStore.company.title} (${companyDetailStore.company.market.title}:${companyDetailStore.company.ticker}) - Обзор компании, Новости, Аналитика - Finargo`
}

watch(route, (to) => {
  if (to.name === RouteNamesEnum.company_detail) {
    init()
  }
})

onMounted(async () => {
  await init()
})
</script>

<template>
  <section style="max-width: 1200px">
    <company-detail-header />
    <company-detail-content />
  </section>
  <company-detail-right-sidebar />
  <notes-editor />
</template>
