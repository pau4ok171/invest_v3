<script lang="ts">
// Styles
import './BaseCounter.scss';

// Components
import {BaseSlideYTransition} from "@/apps/visagiste/components/transitions";

// Composables
import {useComponentProps} from "@/apps/visagiste/composables/component";
import MaybeTransition, {useTransitionProps} from "@/apps/visagiste/composablesV2/transition.vue";

// Utilities
import {defineComponent, propsFactory} from "@/apps/visagiste/utils";

// Types
import type {Component, SlotsType} from "vue";
import {computed} from "vue";

export const useBaseCounterProps = propsFactory({
  active: Boolean,
  disabled: Boolean,
  max: [Number, String],
  value: {
    type: [Number, String],
    default: 0,
  },

  ...useComponentProps(),
  ...useTransitionProps({
    transition: {component: BaseSlideYTransition as Component},
  }),
}, 'BaseCounter')

export type BaseCounterSlot = {
  counter: string
  max: string | number | undefined
  value: string | number | undefined
}

type BaseCounterSlots = {
  default: BaseCounterSlot
}

export default defineComponent({
  name: "BaseCounter",
  components: {MaybeTransition},
  props: useBaseCounterProps(),
  slots: Object as SlotsType<BaseCounterSlots>,
  setup (props) {
    const counter = computed(() => {
      return props.max ? `${props.max}` : String(props.value)
    })

    return {
      counter
    }
  }
})
</script>

<template>
<MaybeTransition :transition="$props.transition">
  <div
    v-show="$props.active"
    :class="[
      'base-counter',
      {
        'text-error': $props.max && !$props.disabled && parseFloat($props.value) > parseFloat($props.max),
      },
      $props.class,
    ]"
    :style="$props.style"
  >
    <slot v-bind="{
      counter: counter,
      max: $props.max,
      value: $props.value
    }">
      {{ counter }}
    </slot>
  </div>
</MaybeTransition>
</template>
