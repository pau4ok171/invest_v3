<script setup lang="ts">
// Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { BaseDialog } from '@/apps/visagiste/components/BaseDialog'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseSelect from '@/apps/visagiste/components/BaseSelect/BaseSelect.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
import BaseToolbar from '@/apps/visagiste/components/BaseToolbar/BaseToolbar.vue'

// Composables
import { useCompanyListStore } from '@/store/companyList'

// Utilities
import { ref, shallowRef, watch } from 'vue'

const companyListStore = useCompanyListStore()

const dialog = shallowRef(false)
const country = ref({ slug: 'global', title: 'Global' })
const sector = ref({ slug: 'any', title: 'Any' })

watch(country, async (newVal) => {
  await companyListStore.changeFilter({ filterName: 'country', item: newVal })
  country.value = companyListStore.activeFilters.country
  sector.value = companyListStore.activeFilters.sector
}, { deep: true })
watch(sector, async (newVal) => {
  await companyListStore.changeFilter({ filterName: 'sector', item: newVal })
  country.value = companyListStore.activeFilters.country
  sector.value = companyListStore.activeFilters.sector
}, { deep: true })
</script>

<template>
  <section class="company-list__filters">
    <div class="company-list__basic-filters">
      <base-select
        v-model="country"
        :items="companyListStore.filters.country"
        :loading="companyListStore.fetching"
        variant="solo-filled"
        density="compact"
        single-line
        item-title="title"
        item-value="slug"
        return-object
        hide-details
      />

      <base-select
        v-model="sector"
        :items="companyListStore.filters.sector"
        :loading="companyListStore.fetching"
        variant="solo-filled"
        density="compact"
        single-line
        item-value="slug"
        return-object
        hide-details
      />
    </div>

    <base-dialog v-model="dialog" max-width="500">
      <template #activator="{ props: activatorProps }">
        <base-button
          v-bind="activatorProps"
          text="advanced filters"
          append-icon="$iFilter"
          variant="text"
        />
      </template>

      <template #default>
        <base-card>
          <base-toolbar title="Advanced filters">
            <base-button variant="text" icon="$close" @click="dialog = false" />
          </base-toolbar>
          <base-card-text>TO BE ADDED</base-card-text>
        </base-card>
      </template>
    </base-dialog>
  </section>
</template>

<style>
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
