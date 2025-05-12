<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'
import { useDisplay } from 'vuetify'

// Utilities
import { computed } from 'vue'

const store = usePageStore()
const { lg, xl, lgAndUp } = useDisplay()
const extended = computed(() => store.extended)

const maxWidth = computed(() => {
  if (extended.value && lgAndUp.value) {
    return xl.value ? '1630px' : lg.value ? '1200px' : '100%'
  }
  return xl.value ? '1200px' : '100%'
})
</script>

<template>
  <v-main class="main">
    <div class="main__inner" :style="{ maxWidth }">
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
  display: flex;
  flex-direction: row;
  width: 100%;
  padding: 0 16px;
  transition: 0.6s cubic-bezier(0.83, 0, 0.17, 1);
}
</style>
