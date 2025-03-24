<script lang="ts">
// Styles
import './BaseMessages.scss'

// Components
import { BaseSlideYTransition } from '@/apps/visagiste/components/transitions'

// Composables
import { useTextColor } from '@/apps/visagiste/composables/color'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import MaybeTransition, {
  useTransitionProps,
} from '@/apps/visagiste/composablesV2/transition.vue'

// Utilities
import { computed } from 'vue'
import {
  defineComponent,
  propsFactory,
  wrapInArray,
} from '@/apps/visagiste/utils'

// Types
import type { Component, PropType } from 'vue'

export type BaseMessageSlot = {
  message: string
}

export type BaseMessagesSlots = {
  message: BaseMessageSlot
}

export const useBaseMessagesProps = propsFactory(
  {
    active: Boolean,
    color: String,
    messages: {
      type: [Array, String] as PropType<string | readonly string[]>,
      default: () => [],
    },

    ...useComponentProps(),
    ...useTransitionProps({
      transition: {
        component: BaseSlideYTransition as Component,
        leaveAbsolute: true,
        group: true,
      },
    }),
  },
  'BaseMessages'
)

export default defineComponent({
  name: 'BaseMessages',
  props: useBaseMessagesProps(),
  components: {
    MaybeTransition,
  },
  setup(props) {
    const messages = computed(() => wrapInArray(props.messages))
    const { textColorClasses, textColorStyles } = useTextColor(
      computed(() => props.color)
    )

    return {
      messages,
      textColorClasses,
      textColorStyles,
    }
  },
})
</script>

<template>
  <MaybeTransition
    :transition="$props.transition"
    tag="div"
    :class="['base-messages', textColorClasses, $props.class]"
    :style="[textColorStyles, $props.style]"
  >
    <template v-if="$props.active">
      <div
        v-for="(message, index) in messages"
        class="base-messages__message"
        :key="`${index}-${messages}`"
      >
        <slot name="message" v-bind="message">
          {{ message }}
        </slot>
      </div>
    </template>
  </MaybeTransition>
</template>
