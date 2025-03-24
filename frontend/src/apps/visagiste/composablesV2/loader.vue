<script lang="ts">
// Components
import { BaseProgressLinear } from '@/apps/visagiste/components/BaseProgressLinear'

// Utilities
import { computed } from 'vue'
import {
  defineComponent,
  getCurrentInstanceName,
  propsFactory,
} from '@/apps/visagiste/utils'

export interface LoaderSlotProps {
  color: string | undefined
  isActive: boolean
}

export interface LoaderProps {
  loading?: boolean | string
}

// Composables
export const useLoaderProps = propsFactory(
  {
    loading: [Boolean, String],
  },
  'loader'
)

export function useLoader(props: LoaderProps, name = getCurrentInstanceName()) {
  const loaderClasses = computed(() => ({
    [`${name}--loading`]: props.loading,
  }))

  return { loaderClasses }
}

export default defineComponent({
  name: 'LoaderSlot',
  components: {BaseProgressLinear},
  props: {
    absolute: Boolean,
    active: Boolean,
    name: String,
    color: String,
  },
})
</script>

<template>
  <div :class="`${$props.name}__loader`">
    <slot :color="$props.color" :isActive="$props.active">
      <BaseProgressLinear
        :absolute="$props.absolute"
        :active="$props.active"
        :color="$props.color"
        :height="2"
        indeterminate
      />
    </slot>
  </div>
</template>
