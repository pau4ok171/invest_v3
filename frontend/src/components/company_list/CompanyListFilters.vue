<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'

// Utilities
import { shallowRef } from 'vue'

// Types
import type { CountryState, DependentState } from '@/store/companyList/types'

const store = useCompanyListStore()

const dialog = shallowRef(false)

async function onUpdateCountry(modelValue: CountryState) {
  if (store.countryState.key === modelValue.key) return

  store.countryState = modelValue
  store.resetSectorState()

  if (store.sectorState.key === 'any') {
    await store.fetchCompanies({ done: (status: string) => status }, true)
  }
}

async function onUpdateSector(modelValue: DependentState) {
  if (store.sectorState.key === modelValue.key) return

  store.sectorState = modelValue
  await store.fetchCompanies({ done: (status: string) => status }, true)
}
</script>

<template>
  <section class="company-list__filters">
    <div class="company-list__basic-filters">
      <v-select
        :model-value="store.countryState"
        @update:model-value="onUpdateCountry"
        :items="store.countries"
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
        :model-value="store.sectorState"
        @update:model-value="onUpdateSector"
        :items="store.filteredSectors"
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
          text="advanced filters"
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
  </section>
</template>

<style scoped>
.company-list__filters {
  display: grid;
  grid-template-columns: auto auto;
  grid-template-rows: 40px;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}
.company-list__basic-filters {
  display: grid;
  column-gap: 8px;
  grid-template-columns: auto auto;
}
</style>
