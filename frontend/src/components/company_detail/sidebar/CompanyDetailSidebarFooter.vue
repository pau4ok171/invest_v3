<script setup lang="ts">
// Components
import BaseList from '@/apps/visagiste/components/BaseList/BaseList.vue'

// Utilities
import { onMounted, ref } from 'vue'

const sections = ref([
  { value: 'overview', title: 'Company Overview' },
  { value: 'value', title: '1 Valuation' },
  { value: 'future', title: '2 Future Growth' },
  { value: 'past', title: '3 Past Performance' },
  { value: 'health', title: '4 Financial Health' },
  { value: 'dividend', title: '5 Dividend' },
  { value: 'management', title: '6 Management' },
  { value: 'owners', title: '7 Ownership' },
  { value: 'other', title: 'Other Information' },
])
const activeSection = ref(['overview'])
const prevSection = ref('other')
const nextSection = ref('value')

function changeSection(section: unknown) {
  if (!Array.isArray(section)) return

  activeSection.value[0] = section[0]
  prevSection.value = section[0]
  nextSection.value = section[0]
  const goTo = (document as any)
    .querySelector(`#${section[0]}`)
    .getBoundingClientRect()
  const windowScroll = document.documentElement.scrollTop
  const scrollTop = goTo.top + windowScroll - 80
  window.scrollTo({ top: scrollTop })
}

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    const entry = entries[0]
    if (entry.intersectionRatio > 0) {
      prevSection.value =
        entry.boundingClientRect.top >= 0
          ? activeSection.value[0]
          : prevSection.value
      activeSection.value[0] = entry.target.getAttribute('id') as string
      prevSection.value =
        entry.boundingClientRect.top < 0
          ? activeSection.value[0]
          : prevSection.value
      nextSection.value =
        entry.boundingClientRect.top >= 0
          ? activeSection.value[0]
          : nextSection.value
    } else {
      if (entry.boundingClientRect.top < 0) {
        activeSection.value[0] = nextSection.value
      } else {
        activeSection.value[0] = prevSection.value
      }
    }
  })

  document.querySelectorAll('.section_observer').forEach(
    (section) => {
      observer.observe(section)
    },
    {
      rootMargin: '-50% 0px -50% 0px',
      threshold: [0.1],
    }
  )
})
</script>

<template>
  <base-list
    :items="sections"
    v-model:selected="activeSection"
    @update:selected="changeSection"
    density="compact"
  />
</template>
