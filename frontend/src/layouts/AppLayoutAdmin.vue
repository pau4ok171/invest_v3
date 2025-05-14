<script setup lang="ts">
// Components
import TheHeader from '@/components/base/header/TheHeader.vue'
import TheMain from '@/components/base/main/TheMain.vue'
import TheFooter from "@/components/base/footer/TheFooter.vue";

// Utilities
import { reactive } from 'vue'

const headers = reactive([
  {
    title: 'Dashboard',
    props: { to: { name: 'adminDashboard' }, prependIcon: '$iDashboard' },
  },
  {
    title: 'Models',
    props: { to: { name: 'adminModels' }, prependIcon: '$iDatabase' },
  },
  {
    title: 'Staff',
    props: { to: { name: 'adminStaff' }, prependIcon: '$iAccountTie' },
  },
  {
    title: 'Settings',
    props: { to: { name: 'adminSettings' }, prependIcon: '$iCog' },
  },
])
</script>

<template>
  <the-header />

  <v-navigation-drawer>
    <v-list :items="headers" nav />
  </v-navigation-drawer>

  <the-main><slot /></the-main>

  <the-footer />
</template>
