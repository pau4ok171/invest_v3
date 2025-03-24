<script setup lang="ts">
// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

const companyDetailStore = useCompanyDetailStore()
const company = computed(() => companyDetailStore.company)
</script>

<template>
  <div class="detail-sidebar__header">
    <div class="detail-sidebar__logo">
      <img :src="company.logo_url" :alt="company.slug" />
    </div>
  </div>
</template>

<style scoped>
.detail-sidebar__header {
  display: flex;
  justify-content: flex-start;
  padding-bottom: 8px;
  opacity: 0;
}
.detail-sidebar__logo {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 160px;
  height: 160px;
  background-color: #fff;
  border-radius: 8px;
}
.detail-sidebar__logo img {
  width: 100px;
  height: 100px;
}
</style>
