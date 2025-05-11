<script setup lang="ts">
// Components
import NavTheme from '@/components/base/header/navigation/NavTheme.vue'
import NavMenu from '@/components/base/header/navigation/NavMenu.vue'
import NavSearch from '@/components/base/header/navigation/NavSearch.vue'
import NavLang from '@/components/base/header/navigation/NavLang.vue'
import NavUser from '@/components/base/header/navigation/NavUser.vue'
import NavLogo from '@/components/base/header/navigation/NavLogo.vue'
</script>

<template>
  <v-app-bar class="header px-md-3" color="background" flat :extended="false">
    <template #prepend>
      <nav-logo />
      <div class="px-1"></div>
      <nav-search />
    </template>
    <template #append>
      <nav-menu />
      <v-divider vertical inset class="mx-2 my-auto" length="16" />
      <nav-lang />
      <nav-theme />
      <v-divider vertical class="mx-2 my-auto" length="16" />
      <nav-user />
    </template>
  </v-app-bar>
</template>

<style lang="scss">
.header {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1010;
  transform: translateY(0);
  padding: 0 12px;
}
</style>
