<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { RoutesHeaderEnum } from '@/router/routes.types'

const { t } = useI18n()
</script>

<template>
  <v-menu>
    <template #activator="{ props }">
      <v-app-bar-nav-icon v-bind="props" />
    </template>

    <v-list>
      <v-list-item
        v-for="routeName in RoutesHeaderEnum"
        :key="routeName"
        :to="{ name: routeName }"
        variant="text"
      >
        <template #title>
          <div class="text-capitalize">{{ t(`header.${routeName}`) }}</div>
        </template>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
