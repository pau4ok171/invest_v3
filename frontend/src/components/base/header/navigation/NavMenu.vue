<script setup lang="ts">
import { RoutesHeaderEnum } from '@/router/routes.types'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
</script>

<template>
  <div class="navigation__nav-menu">
    <RouterLink
      v-for="routeName in RoutesHeaderEnum"
      :key="routeName"
      :to="{ name: routeName }"
    >
      <base-button
        :text="routeName"
        variant="text"
        style="text-transform: capitalize; padding-inline: 8px"
      />
    </RouterLink>
  </div>
</template>

<style>
.navigation__nav-menu {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
