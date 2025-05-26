<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, shallowRef } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type { PropType } from 'vue'
import type { News } from '@/types/invest'

const props = defineProps({
  item: {
    type: Object as PropType<News>,
    required: true,
  },
})

const dialog = shallowRef(false)
const { locale } = useI18n()

const publishedAt = computed(() =>
  DateTime.fromISO(props.item.date).toFormat('DD', { locale: locale.value })
)
</script>

<template>
  <v-dialog max-width="700" v-model="dialog">
    <template #activator="{ props: activatorProps }">
      <v-card variant="text" v-bind="activatorProps">
        <v-card-item>
          <template #prepend>
            <v-avatar variant="tonal">
              <v-icon icon="$iMegaphone" />
            </v-avatar>
          </template>

          <v-card-text class="py-0">{{ item.title }}</v-card-text>
          <v-card-text class="py-0 opacity-50" style="font-size: 0.75rem">
            {{ publishedAt }}
          </v-card-text>
        </v-card-item>
      </v-card>
    </template>

    <v-card>
      <template #append>
        <v-btn
          icon="$close"
          density="compact"
          variant="text"
          @click="dialog = false"
        />
      </template>
      <v-card-title>{{ props.item.title }}</v-card-title>
      <v-divider />
      <v-card-text>{{ props.item.content }}</v-card-text>
    </v-card>
  </v-dialog>
</template>
