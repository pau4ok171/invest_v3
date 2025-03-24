<script setup lang="ts">
// Components
import CompanyDetailSidebar from '@/components/company_detail/sidebar/CompanyDetailSidebar.vue'
import CompanyDetailContentList from '@/components/company_detail/content_list/CompanyDetailContentList.vue'
</script>

<template>
  <div class="detail__content">
    <CompanyDetailSidebar />

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
