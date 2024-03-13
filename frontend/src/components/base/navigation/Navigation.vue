<script setup lang="ts">

import NavMenu from "@/components/base/navigation/NavMenu.vue";
import NavUser from "@/components/base/navigation/NavUser.vue";
import NavLang from "@/components/base/navigation/NavLang.vue";
import NavSearch from "@/components/base/navigation/NavSearch.vue";
import NavLogo from "@/components/base/navigation/NavLogo.vue";
</script>

<template>
  <nav class="navigation">
    <NavLogo/>
    <NavMenu/>
    <NavSearch/>
    <NavLang/>
    <NavUser/>
  </nav>
</template>

<style scoped>
  .navigation {
    display: flex;
    justify-content: center;
    height: 100%;
    width: 100%;
    max-width: 1200px;
    position: relative;
  }
</style>