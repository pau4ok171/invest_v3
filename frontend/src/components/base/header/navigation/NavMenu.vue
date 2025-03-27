<script setup lang="ts">
import { RoutesHeaderEnum } from '@/router/routes.types'
</script>

<template>
  <div class="navigation__nav-menu">
    <v-btn
      v-for="routeName in RoutesHeaderEnum"
      :key="routeName"
      class="text-capitalize px-2"
      :text="routeName"
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
