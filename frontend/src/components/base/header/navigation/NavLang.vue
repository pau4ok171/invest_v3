<script setup lang="ts">
// Components
import { BaseFlag } from '@/components/UI/BaseFlag'

// Composables
import { ref, watch } from 'vue'
import { useLocale } from 'vuetify'
import { useI18n } from 'vue-i18n'

const langs = [
  { id: 'en', title: 'English', iso: 'gb' },
  { id: 'ru', title: 'Русский', iso: 'ru' },
  { id: 'fr', title: 'Français', iso: 'fr' },
  { id: 'es', title: 'Español', iso: 'es' },
  { id: 'de', title: 'Deutsch', iso: 'de' },
]

const selected = ref(['ru'])
const { current } = useLocale()
const { locale, t } = useI18n()

current.value = selected.value[0]
locale.value = selected.value[0]

watch(selected, () => {
  current.value = selected.value[0]
  locale.value = selected.value[0]
})
</script>

<template>
  <v-menu>
    <template #activator="{ props }">
      <v-btn v-bind="props" icon="$iLang" variant="text" rounded="lg" />
    </template>
    <template #default>
      <v-card>
        <v-list
          v-model:selected="selected"
          slim
          nav
          density="compact"
          mandatory
        >
          <v-list-subheader
            class="text-high-emphasis text-uppercase font-weight-black"
          >
            {{ t('header.translations') }}
          </v-list-subheader>
          <v-list-item
            v-for="item in langs"
            :key="item.id"
            :title="item.title"
            :value="item.id"
            rounded
          >
            <template #prepend>
              <base-flag :code="item.iso" />
            </template>
          </v-list-item>
        </v-list>
      </v-card>
    </template>
  </v-menu>
</template>
