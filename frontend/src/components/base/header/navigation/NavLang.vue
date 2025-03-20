<script setup lang="ts">
import { BaseMenu } from '@/apps/visagiste/components/BaseMenu'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { BaseList } from '@/apps/visagiste/components/BaseList'
import { ref, watch } from 'vue'
import { useLocale } from '@/apps/visagiste/composables'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseListItem from '@/apps/visagiste/components/BaseList/BaseListItem.vue'
import { BaseFlag } from '@/apps/visagiste/components/BaseFlag'
import BaseListItemSubheader from '@/apps/visagiste/components/BaseList/BaseListSubheader.vue'

const langs = [
  { id: 'en', title: 'English', iso: 'gb' },
  { id: 'ru', title: 'Русский', iso: 'ru' },
  { id: 'fr', title: 'Français', iso: 'fr' },
  { id: 'es', title: 'Español', iso: 'es' },
  { id: 'de', title: 'Deutsch', iso: 'de' },
]

const selected = ref(['ru'])
const { current } = useLocale()

watch(selected, () => {
  current.value = selected.value[0]
})
</script>

<template>
  <base-menu>
    <template #activator="{ props }">
      <base-button v-bind="props" icon="$iLang" variant="text" rounded="lg" />
    </template>
    <template #default>
      <base-card>
        <base-list v-model:selected="selected" slim nav density="compact">
          <base-list-item-subheader
            class="text-high-emphasis text-uppercase font-weight-black"
            >Translations</base-list-item-subheader
          >
          <base-list-item
            v-for="item in langs"
            :key="item.id"
            :title="item.title"
            :value="item.id"
            active-class="text-primary"
            rounded
          >
            <template #prepend>
              <base-flag :code="item.iso" />
            </template>
          </base-list-item>
        </base-list>
      </base-card>
    </template>
  </base-menu>
</template>
