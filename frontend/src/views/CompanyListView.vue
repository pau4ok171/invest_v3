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
  <section class="d-flex justify-center w-100 h-100 flex-column">
    <CompanyListHeader />

    <CompanyListContent />
  </section>
</template>
