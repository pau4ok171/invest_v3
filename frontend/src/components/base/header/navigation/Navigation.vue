<script setup lang="ts">

import NavMenu from "@/components/base/header/navigation/NavMenu.vue";
import NavUser from "@/components/base/header/navigation/NavUser.vue";
import NavLang from "@/components/base/header/navigation/NavLang.vue";
import NavSearch from "@/components/base/header/navigation/NavSearch.vue";
import NavLogo from "@/components/base/header/navigation/NavLogo.vue";
</script>

<template>
  <nav class="navigation">
    <NavLogo/>
    <NavMenu/>
    <NavSearch/>
    <div class="navigation__group">
      <NavLang/>
      <NavUser/>
    </div>
  </nav>
</template>

<style scoped>
  .navigation {
    display: flex;
    justify-content: space-between;
    height: 100%;
    width: 100%;
    max-width: 1200px;
    position: relative;
    border-bottom: 1px solid rgba(255, 255, 255, .1);
  }
  .navigation__group {
    display: flex;
  }
</style>