<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'

// Utilities
import { computed } from 'vue'

const store = usePageStore()
const extended = computed(() => store.extended)
</script>

<template>
  <v-main class="main">
    <div :class="['main__inner', { 'main__inner--extended': extended }]">
      <slot />
    </div>
  </v-main>
</template>

<style lang="scss">
.main {
  display: flex;
  position: relative;
  flex-wrap: wrap;
  max-width: 100%;
  flex: 1 0 auto;
  justify-content: center;
  transition: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.main__inner {
  position: relative;
  max-width: 1200px;
  display: flex;
  flex-direction: row;
  gap: 16px;
  width: 100%;
  transition: 0.6s cubic-bezier(0.83, 0, 0.17, 1);

  &--extended {
    max-width: 1590px;
  }
}
</style>
