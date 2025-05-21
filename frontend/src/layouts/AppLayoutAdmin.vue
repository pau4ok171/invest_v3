<script setup lang="ts">
// Components
import TheHeader from '@/components/base/header/TheHeader.vue'
import TheMain from '@/components/base/main/TheMain.vue'
import TheFooter from '@/components/base/footer/TheFooter.vue'

// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref } from 'vue'

const { t } = useI18n()

const headers = computed(() => [
  {
    title: t('admin.dashboard'),
    props: { to: { name: 'adminDashboard' }, prependIcon: '$iDashboard' },
  },
  {
    title: t('admin.models'),
    props: { to: { name: 'adminModels' }, prependIcon: '$iDatabase' },
  },
  {
    title: t('admin.staff'),
    props: { to: { name: 'adminStaff' }, prependIcon: '$iAccountTie' },
  },
  {
    title: t('admin.settings'),
    props: { to: { name: 'adminSettings' }, prependIcon: '$iCog' },
  },
])

const rail = ref(true)
</script>

<template>
  <the-header />

  <v-navigation-drawer permanent :rail="rail" @click="rail = !rail">
    <v-list :items="headers" nav @click.stop />
  </v-navigation-drawer>

  <the-main><slot /></the-main>

  <the-footer style="z-index: 5000" />
</template>
