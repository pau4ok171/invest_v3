<script setup lang="ts">
// Components
import Logo from '@/components/icons/Logo.vue'

// Composables
import { usePageStore } from '@/store/page'

// Utilities
import { computed } from 'vue'
import { debouncedRef } from '@vueuse/core'

const props = defineProps({
  title: String,
  progress: {
    type: Number,
    default: null,
    validator: (value: number | null) =>
      value === null || (value >= 0 && value <= 100),
  },
})

const store = usePageStore()
const isLoading = debouncedRef(
  computed(() => store.loading),
  300
)
</script>

<template>
  <v-dialog v-model="isLoading" persistent width="400">
    <v-card class="loading-dialog" rounded="lg">
      <v-card-text class="text-center pa-6">
        <div class="mb-4"><logo style="height: 40px" /></div>

        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
          width="6"
          class="mb-4"
        />

        <h3 class="text-h5 font-weight-medium mb-2">
          {{ title || 'Загрузка данных...' }}
        </h3>

        <div v-if="progress != null" class="mt-4">
          <v-progress-linear
            :model-value="progress"
            height="8"
            color="primary"
            rounded
            striped
          />
          <span class="text-caption text-medium-emphasis">
            {{ progress }}% завершено
          </span>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">
.loading-dialog {
  backdrop-filter: blur(8px);
  border: 1px solid rgba(0, 0, 0, 0.12);

  .v-progress-circular {
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  }
  .v-progress-linear {
    border-radius: 4px;
  }
}
</style>
