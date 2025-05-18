<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { RoutesHeaderEnum } from '@/router/routes.types'

const { t } = useI18n()
</script>

<template>
  <div class="navigation__nav-menu">
    <v-btn
      v-for="routeName in RoutesHeaderEnum"
      :key="routeName"
      class="text-capitalize px-2"
      :text="t(`header.${routeName}`)"
      :to="{ name: routeName }"
      variant="text"
    />
  </div>
</template>

<style>
.navigation__nav-menu {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
