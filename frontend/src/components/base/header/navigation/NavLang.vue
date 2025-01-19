<script setup lang="ts">
import BaseMenu from "@/apps/visagiste/components/BaseMenu/BaseMenu.vue";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import BaseList from "@/apps/visagiste/components/BaseList/BaseList.vue";
</script>

<template>
<base-menu>
  <template #activator>
    <base-button
      icon="LangIcon"
      variant="text"
      rounded="x-small"
    />
  </template>
  <template #list>
    <base-list
      :items="[{id: 'ru', title: 'Russian'}, {id: 'fr', title: 'French'}, {id: 'de', title: 'German'}]"
      :active-item="{id: 'ru', title: 'Russian'}"
    />
  </template>
</base-menu>
</template>
