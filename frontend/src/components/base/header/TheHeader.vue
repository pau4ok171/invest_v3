<script setup lang="ts">
import { BaseToolbar } from '@/apps/visagiste/components/BaseToolbar'
import NavTheme from '@/components/base/header/navigation/NavTheme.vue'
import NavMenu from '@/components/base/header/navigation/NavMenu.vue'
import NavSearch from '@/components/base/header/navigation/NavSearch.vue'
import NavLang from '@/components/base/header/navigation/NavLang.vue'
import NavUser from '@/components/base/header/navigation/NavUser.vue'
import NavLogo from '@/components/base/header/navigation/NavLogo.vue'
import BaseDivider from '@/apps/visagiste/components/BaseDivider/BaseDivider.vue'
</script>

<template>
  <base-toolbar class="header">
    <template #prepend>
      <NavLogo />
      <div class="px-1"></div>
      <NavSearch />
    </template>
    <template #append>
      <NavMenu />
      <base-divider vertical inset class="mx-2 my-auto" length="16" />
      <NavLang />
      <NavTheme />
      <base-divider vertical class="mx-2 my-auto" length="16" />
      <NavUser />
    </template>
  </base-toolbar>
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
