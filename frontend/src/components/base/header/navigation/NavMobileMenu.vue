<script setup lang="ts">
// Utilities
import { RoutesHeaderEnum } from '@/router/routes.types'
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
          <div class="text-capitalize">{{ routeName }}</div>
        </template>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
