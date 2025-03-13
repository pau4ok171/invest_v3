<script setup lang="ts">
// Components
import CompanyListHeader from '@/components/company_list/CompanyListHeader.vue'
import CompanyListContent from '@/components/company_list/CompanyListContent.vue'

// Composables
import { useCompanyListStore } from '@/store/companyList'

// Utilities
import { onMounted } from 'vue'

const companyListStore = useCompanyListStore()

onMounted(async () => {
  document.title = 'Stocks'
  await companyListStore.fetchFilters()
})
</script>

<template>
  <section>
    <CompanyListHeader />

    <CompanyListContent />
  </section>
</template>
