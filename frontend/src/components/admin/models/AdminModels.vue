<script setup lang="ts">
const items = [
  { title: 'Models', type: 'subheader' },
  { title: 'Companies', props: { to: { name: 'adminModelsCompanies' } } },
]
</script>

<template>
  <v-navigation-drawer floating color="background">
    <v-list :items nav />
  </v-navigation-drawer>

  <router-view />
</template>
