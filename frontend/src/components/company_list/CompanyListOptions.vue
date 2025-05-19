<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'
import { useI18n } from 'vue-i18n'

const store = useCompanyListStore()
const { t } = useI18n()
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
      <v-btn-toggle v-model="store.contentMode" mandatory variant="text">
        <v-btn icon="$iTableMode" value="table" />
        <v-btn icon="$iTileMode" value="tile" />
      </v-btn-toggle>
    </v-col>
  </v-row>
</template>
