<script setup lang="ts">
// Components
import CompanyDetailSidebar from '@/components/company_detail/sidebar/CompanyDetailSidebar.vue'
import CompanyDetailContentList from '@/components/company_detail/content_list/CompanyDetailContentList.vue'

// Composables
import { useDisplay } from 'vuetify'

const { lgAndUp } = useDisplay()
</script>

<template>
  <div class="detail__content">
    <CompanyDetailSidebar v-if="lgAndUp" />

    <CompanyDetailContentList />
  </div>
</template>

<style scoped>
.detail__content {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
</style>
