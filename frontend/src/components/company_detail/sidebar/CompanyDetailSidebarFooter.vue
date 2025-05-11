<script setup lang="ts">
// Composables
import { useSectionContext } from '@/composables/sectionObserver'

// Utilities
import { SECTIONS } from '@/assets/static/companyDetail'

const { activeSection, changeSection } = useSectionContext()
</script>

<template>
  <v-list
    :selected="[activeSection]"
    @update:selected="changeSection"
    :items="SECTIONS"
    density="compact"
    bg-color="background"
  />
</template>
