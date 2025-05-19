<script setup lang="ts">
// Composables
import { useSectionContext } from '@/composables/sectionObserver'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed } from 'vue'
import { SECTIONS } from '@/assets/static/companyDetail'

const { activeSection, changeSection } = useSectionContext()
const { t } = useI18n()
const sections = computed(() =>
  SECTIONS.map((s) => ({
    ...s,
    title: `${s.numeric} ` + t(`companyDetail.sections.${s.value}`),
  }))
)
</script>

<template>
  <v-list
    :selected="[activeSection]"
    @update:selected="changeSection"
    :items="sections"
    density="compact"
    bg-color="background"
  />
</template>
