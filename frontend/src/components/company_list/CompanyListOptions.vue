<script setup lang="ts">
// Composables
import { useAuthStore } from '@/store/auth'
import { useCompanyListStore } from '@/store/companyList/companyList'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref } from 'vue'

const authStore = useAuthStore()
const store = useCompanyListStore()
const { t } = useI18n()

const localStockView = ref(
  authStore.profile?.stockView || localStorage.getItem('stock_view') || 'table'
)

const setStockView = async (newValue: string) => {
  localStockView.value = newValue
  localStorage.setItem('stock_view', newValue)

  try {
    if (authStore.isAuthenticated && authStore.profile) {
      await authStore.patchProfile({ stock_view: newValue })
    }
  } catch (error) {
    console.error('Failed to change stock view:', error)
    localStockView.value =
      authStore.profile?.stockView ||
      localStorage.getItem('stock_view') ||
      'table'
  }
}

const currentStockView = computed({
  get: () => localStockView.value,
  set: (newValue) => setStockView(newValue),
})
</script>

<template>
  <v-row no-gutters>
    <v-col cols="3"></v-col>

    <v-col
      class="d-flex align-center justify-center text-caption text-medium-emphasis"
    >
      <v-skeleton-loader
        v-if="store.fetching"
        loading
        type="text"
        width="150"
      />
      <p v-else>{{ t('companyList.header.companies', store.totalCompanyLength) }}</p>
    </v-col>

    <v-col cols="3" class="d-flex justify-end">
      <v-btn-toggle v-model="currentStockView" mandatory variant="text">
        <v-btn icon="$iTableMode" value="table" />
        <v-btn icon="$iTileMode" value="tile" />
      </v-btn-toggle>
    </v-col>
  </v-row>
</template>
