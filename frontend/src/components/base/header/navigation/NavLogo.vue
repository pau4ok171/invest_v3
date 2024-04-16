<script setup lang="ts">

import {RoutesHeaderEnum} from "@/router/routes.types";
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
    display: flex;
    align-items: center;
    justify-content: flex-start;
    font-size: 30px;
    font-weight: 900;
    user-select: none;
  }
</style>