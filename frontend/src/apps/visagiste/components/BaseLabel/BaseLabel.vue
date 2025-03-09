<script lang="ts">
// Styles
import './BaseLabel.scss'

// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useThemeProps } from '@/apps/visagiste/composables/theme'

// Utilities
import {
  defineComponent,
  EventProp,
  propsFactory,
} from '@/apps/visagiste/utils'

export const useBaseLabelProps = propsFactory(
  {
    text: String,
    onClick: EventProp<[MouseEvent]>(),

    ...useComponentProps(),
    ...useThemeProps(),
  },
  'BaseLabel'
)

export default defineComponent({
  name: 'BaseLabel',
  props: useBaseLabelProps(),
})
</script>

<template>
  <label
    :class="[
      'base-label',
      {
        'base-label--clickable': !!$props.onClick,
      },
      $props.class,
    ]"
    :style="$props.style"
    @click="$props.onClick"
  >
    {{ $props.text }}

    <slot />
  </label>
</template>
