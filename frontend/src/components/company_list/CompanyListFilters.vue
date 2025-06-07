<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'
import { useI18n } from 'vue-i18n'
import { useTranslations } from '@/composables/translations'

// Utilities
import { computed, shallowRef } from 'vue'

// Types
import type { CountryState, SectorState } from '@/store/companyList/types'

const store = useCompanyListStore()
const dialog = shallowRef(false)
const { t } = useI18n()
const { getTranslation } = useTranslations()

const countries = computed(() =>
  store.countries
    .map((obj) => {
      const title =
        obj.key === 'global'
          ? t('companyList.header.global')
          : getTranslation(obj.translations, 'name')

      return {
        ...obj,
        title,
      }
    })
    .sort((a, b) => {
      if (a.key === 'global') return -1
      if (b.key === 'global') return 1
      return a.title.localeCompare(b.title)
    })
)

const selectedCountry = computed(() => {
  const title =
    store.countryState.key === 'global'
      ? t('companyList.header.global')
      : getTranslation(store.countryState.translations, 'name')

  return {
    ...store.countryState,
    title,
  }
})

const sectors = computed(() =>
  store.filteredSectors
    .map((obj) => {
      const title =
        obj.key === 'any'
          ? t('companyList.header.any')
          : getTranslation(obj.translations, 'title')

      return {
        ...obj,
        title,
      }
    })
    .sort((a, b) => {
      if (a.key === 'any') return -1
      if (b.key === 'any') return 1
      return a.title.localeCompare(b.title)
    })
)

const selectedSector = computed(() => {
  const title =
    store.sectorState.key === 'any'
      ? t('companyList.header.any')
      : getTranslation(store.sectorState.translations, 'title')
  return {
    ...store.sectorState,
    title,
  }
})

const onUpdateCountry = async (modelValue: CountryState) => {
  if (store.countryState.key === modelValue.key) return

  store.countryState = modelValue
  store.resetSectorState()

  if (store.sectorState.key === 'any') {
    await store.fetchCompanies({ done: (status: string) => status }, true)
  }
}

const onUpdateSector = async (modelValue: SectorState) => {
  if (store.sectorState.key === modelValue.key) return

  store.sectorState = modelValue
  await store.fetchCompanies({ done: (status: string) => status }, true)
}
</script>

<template>
  <div class="d-flex align-center justify-space-between mt-2">
    <div class="d-flex ga-2">
      <v-select
        :model-value="selectedCountry"
        @update:model-value="onUpdateCountry"
        :items="countries"
        :loading="store.fetching"
        variant="solo-filled"
        density="compact"
        single-line
        item-title="title"
        item-value="key"
        return-object
        hide-details
      />

      <v-select
        :model-value="selectedSector"
        @update:model-value="onUpdateSector"
        :items="sectors"
        :loading="store.fetching"
        variant="solo-filled"
        density="compact"
        single-line
        item-title="title"
        item-value="key"
        return-object
        hide-details
      />
    </div>

    <v-dialog v-model="dialog" max-width="500">
      <template #activator="{ props: activatorProps }">
        <v-btn
          v-bind="activatorProps"
          :text="t('buttons.advancedFilters')"
          append-icon="$iFilter"
          variant="text"
        />
      </template>

      <template #default>
        <v-card>
          <v-toolbar title="Advanced filters">
            <v-btn variant="text" icon="$close" @click="dialog = false" />
          </v-toolbar>
          <v-card-text>TO BE ADDED</v-card-text>
        </v-card>
      </template>
    </v-dialog>
  </div>
</template>
