<template>
  <div class="navigation__nav-menu">
    <RouterLink
        v-for="routeName in RouteNamesEnum"
        :key="routeName"
        class="nav-menu__item"
        :to="{ name: routeName }"
    >
      {{ routeName }}
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
  import { RouteNamesEnum } from "@/router/routes.types";
</script>

<style scoped>
  .navigation__nav-menu {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-left: 215px;
    margin-right: auto;
  }

  .nav-menu__item {
    font-size: 1.4rem;
    padding: 0 8px;
    display: inline-block;
    text-transform: capitalize;
    height: 64px;
    line-height: 64px;
  }
</style>