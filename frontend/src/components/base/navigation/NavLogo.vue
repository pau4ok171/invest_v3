<script setup lang="ts">

import {RouteNamesEnum} from "@/router/routes.types";
</script>

<template>
  <div class="default-logo navigation__logo">
    <RouterLink
      :key="`home`"
      :to="{ name: `home` }"
    >
      Finargo
    </RouterLink>
  </div>
</template>

<style scoped>
  .navigation__logo {
    position: absolute;
    left: 24px;
    top: 8px;
  }
</style>