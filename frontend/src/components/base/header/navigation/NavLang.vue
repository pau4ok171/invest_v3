<script setup lang="ts">
import BaseMenu from "@/apps/visagiste/components/BaseMenu/BaseMenu.vue";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import BaseList from "@/apps/visagiste/components/BaseList/BaseList.vue";
import {ref} from "vue";
import { useLocale } from "@/apps/visagiste/composables";

const { current } = useLocale()
const activeElement = ref({id: 'en', title: 'English'})
const setActiveElement = (newActiveElement: {id: string, title: string}) => {
  current.value = newActiveElement.id
  activeElement.value = newActiveElement
}
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
      :items="[
        {id: 'en', title: 'English'},
        {id: 'ru', title: 'Русский'},
        {id: 'fr', title: 'Français'},
        {id: 'es', title: 'Español'},
        {id: 'de', title: 'Deutsch'},
      ]"
      :active-item="activeElement"
      @setActiveItem="setActiveElement"
    />
  </template>
</base-menu>
</template>
