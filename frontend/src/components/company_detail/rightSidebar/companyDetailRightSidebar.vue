<script setup lang="ts">
// Components
import CompanyDetailNotesLateralCard from '@/components/company_detail/content_list/summary/notes/CompanyDetailNotesLateralCard.vue'
import CompanyDetailNewsLateralCard from '@/components/company_detail/content_list/summary/news/CompanyDetailNewsLateralCard.vue'

// Composables
import { usePageStore } from '@/store/page'
import { useCompanyDetailStore } from '@/store/companyDetail'
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
  <transition type="animation" name="lateral-menu">
    <div class="notes-lateral-menu" v-if="store.extended">
      <component :is="componentIs" />
    </div>
  </transition>
</template>

<style scoped lang="scss">
.notes-lateral-menu {
  position: fixed;
  left: 1368px;
  top: 76px;
  right: 4px;
  overflow: hidden;
  height: calc(-88px + 100vh);
  width: 374px;
}
.lateral-menu-enter-active {
  animation: 600ms cubic-bezier(0.83, 0, 0.17, 1) 0s 1 normal none running
    lateral-menu;
}
.lateral-menu-leave-active {
  animation: 800ms cubic-bezier(0.83, 0, 0.17, 1) 0s 1 reverse none running
    lateral-menu;
}
@keyframes lateral-menu {
  0% {
    transform: scaleX(0);
    transform-origin: 100% 100%;
  }
  100% {
    transform: scaleX(1);
    transform-origin: 100% 100%;
  }
}
</style>
