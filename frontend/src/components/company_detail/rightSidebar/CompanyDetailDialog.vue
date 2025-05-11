<script setup lang="ts">
// Components
import CompanyDetailNotesLateralCard from '@/components/company_detail/content_list/summary/notes/CompanyDetailNotesLateralCard.vue'
import CompanyDetailNewsLateralCard from '@/components/company_detail/content_list/summary/news/CompanyDetailNewsLateralCard.vue'

// Composables
import { usePageStore } from '@/store/page'
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed } from 'vue'

// Types
import type { ComputedRef } from 'vue'

type LateralMenuComponentName = 'news' | 'notes' | null

type LateralMenuComponents = {
  notes: typeof CompanyDetailNotesLateralCard
  news: typeof CompanyDetailNewsLateralCard
}

type LateralMenuComponent =
  | typeof CompanyDetailNotesLateralCard
  | typeof CompanyDetailNewsLateralCard

const store = usePageStore()
const detailStore = useCompanyDetailStore()
const componentName: ComputedRef<LateralMenuComponentName> = computed(
  () => detailStore.lateralMenuComponentName
)

const components: LateralMenuComponents = {
  notes: CompanyDetailNotesLateralCard,
  news: CompanyDetailNewsLateralCard,
}

const componentIs: ComputedRef<NonNullable<LateralMenuComponent>> = computed(
  () => {
    const name = componentName.value
    if (!name) throw new Error('Component name is null')
    return components[name]
  }
)
</script>

<template>
  <v-dialog v-model="store.extended" max-width="700">
    <component :is="componentIs" />
  </v-dialog>
</template>
