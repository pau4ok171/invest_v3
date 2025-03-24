<script setup lang="ts">
// Components
import BaseIcon from '@/apps/visagiste/components/BaseIcon/BaseIcon.vue'
import BaseCard from '@/apps/visagiste/components/BaseCard/BaseCard.vue'
import BaseDialog from '@/apps/visagiste/components/BaseDialog/BaseDialog.vue'
import BaseAvatar from '@/apps/visagiste/components/BaseAvatar/BaseAvatar.vue'
import BaseCardText from '@/apps/visagiste/components/BaseCard/BaseCardText.vue'
import BaseCardItem from '@/apps/visagiste/components/BaseCard/BaseCardItem.vue'
import BaseDivider from '@/apps/visagiste/components/BaseDivider/BaseDivider.vue'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import BaseCardTitle from '@/apps/visagiste/components/BaseCard/BaseCardTitle.vue'

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

const publishedAt = computed(() =>
  DateTime.fromISO(props.item.date).toFormat('LLL dd')
)
</script>

<template>
  <base-dialog max-width="700" v-model="dialog">
    <template #activator="{ props: activatorProps }">
      <base-card variant="text" v-bind="activatorProps">
        <base-card-item>
          <template #prepend>
            <base-avatar variant="tonal">
              <base-icon icon="$iMegaphone" />
            </base-avatar>
          </template>

          <base-card-text class="py-0">{{ item.title }}</base-card-text>
          <base-card-text class="py-0 opacity-50" style="font-size: 0.75rem">
            {{ publishedAt }}
          </base-card-text>
        </base-card-item>
      </base-card>
    </template>

    <base-card>
      <template #append>
        <base-button
          icon="$close"
          density="compact"
          variant="text"
          @click="dialog = false"
        />
      </template>
      <base-card-title>{{ props.item.title }}</base-card-title>
      <base-divider />
      <base-card-text>{{ props.item.content }}</base-card-text>
    </base-card>
  </base-dialog>
</template>
