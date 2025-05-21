<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'
import { useDisplay } from 'vuetify'
import { useI18n } from 'vue-i18n'
import { useTitle } from '@/composables/documentTitle'

// Utilities
import { computed, onMounted, ref } from 'vue'
import { onBeforeRouteUpdate } from 'vue-router'

const store = usePageStore()
const { t } = useI18n()
const { setTitle } = useTitle()
setTitle('pageTitles.admin.models')
const { mdAndDown } = useDisplay()

const items = computed(() => [
  { title: t('admin.models'), value: 'models', type: 'subheader' },
  {
    title: 'Companies',
    value: 'companies',
    props: { to: { name: 'adminModelsCompanies' } },
  },
])
const selected = ref<string>('')

onBeforeRouteUpdate((to, from, next) => {
  if (to.name === 'adminModels') selected.value = ''
  next()
})

onMounted(() => {
  store.loading = false
})
</script>

<template>
  <v-navigation-drawer v-if="!mdAndDown" floating color="background">
    <v-list v-model="selected" :items nav />
  </v-navigation-drawer>
  <v-app-bar v-else>
    <v-tabs
      v-model="selected"
      :mandatory="false"
      selected-class="text-info"
      center-active
      show-arrows
    >
      <v-tab
        v-for="item in items"
        :key="`model-tab-${item.value}`"
        :disabled="item.type === 'subheader'"
        :readonly="selected === item.value"
        class="text-body-2 text-capitalize"
        :text="item.title"
        :value="item.value"
        :to="item.props?.to"
      />
    </v-tabs>
  </v-app-bar>

  <router-view />
</template>
