<script setup lang="ts">
import BaseMenu from "@/apps/visagiste/components/BaseMenu/BaseMenu.vue";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import BaseList from "@/apps/visagiste/components/BaseList/BaseList.vue";
</script>

<template>
<div class="navigation__nav-lang">
  <base-menu>
    <template #activator>
      <base-button
        text="RU"
        variant="text"
      />
    </template>
    <template #list>
      <base-list
        :items="[{id: 'ru', title: 'Russian'}, {id: 'fr', title: 'French'}, {id: 'de', title: 'German'}]"
        :active-item="{id: 'ru', title: 'Russian'}"
      />
    </template>
  </base-menu>
</div>
</template>

<style scoped>
.navigation__nav-lang {
  position: relative;
  display: flex;
  align-items: center;
  padding: 0 16px;
}
</style>
