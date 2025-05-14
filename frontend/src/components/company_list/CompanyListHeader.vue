<script setup lang="ts">
// Components
import CompanyListInfo from '@/components/company_list/CompanyListInfo.vue'
import CompanyListFilters from '@/components/company_list/CompanyListFilters.vue'
import CompanyListOptions from '@/components/company_list/CompanyListOptions.vue'
</script>

<template>
  <v-card>
    <v-card-item>
      <company-list-filters />
      <company-list-info />
      <company-list-options />
      <v-divider class="my-2" />
    </v-card-item>
  </v-card>
</template>
