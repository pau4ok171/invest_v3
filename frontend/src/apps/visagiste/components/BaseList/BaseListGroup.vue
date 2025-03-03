<script lang="ts">
// Components
import BaseDefaultsProvider from '@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue'

// Composables
import { useList } from './list'
import {
  useNestedGroupActivator,
  useNestedItem,
} from '@/apps/visagiste/composables/nested/nested'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useSsrBoot } from '@/apps/visagiste/composables/ssrBoot'
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useTagProps } from '@/apps/visagiste/composables/tag'

// Utilities
import { computed, toRef } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'
import MaybeTransition from '@/apps/visagiste/composablesV2/transition.vue'
import { BaseExpandTransition } from '@/apps/visagiste/components/transitions'

export type BaseListGroupSlots = {
  default: never
  activator: { isOpen: boolean; props: Record<string, unknown> }
}

const BaseListGroupActivator = defineComponent({
  name: 'BaseListGroupActivator',
  setup(_, { slots }) {
    useNestedGroupActivator()

    return () => slots.default?.()
  },
})

export const useBaseListGroupProps = propsFactory(
  {
    /* @deprecated */
    activeColor: String,
    baseColor: String,
    color: String,
    collapseIcon: {
      type: IconValue,
      default: '$collapse',
    },
    expandIcon: {
      type: IconValue,
      default: '$expand',
    },
    prependIcon: IconValue,
    appendIcon: IconValue,
    fluid: Boolean,
    subgroup: Boolean,
    title: String,
    value: null,

    ...useComponentProps(),
    ...useTagProps(),
  },
  'BaseListGroup'
)

export default defineComponent({
  name: 'BaseListGroup',
  components: {
    BaseListGroupActivator,
    BaseDefaultsProvider,
    MaybeTransition,
  },
  props: useBaseListGroupProps(),
  computed: {
    BaseExpandTransition() {
      return BaseExpandTransition
    },
  },
  setup(props) {
    const { isOpen, open, id: _id } = useNestedItem(toRef(props, 'value'), true)
    const id = computed(() => `base-list-group-${String(_id.value)}`)
    const list = useList()
    const { isBooted } = useSsrBoot()

    function onClick(e: Event) {
      e.stopPropagation()
      open(!isOpen.value, e)
    }

    const activatorProps = computed(() => ({
      onClick,
      class: 'base-list-group__header',
      id: id.value,
    }))

    const toggleIcon = computed(() =>
      isOpen.value ? props.collapseIcon : props.expandIcon
    )
    const activatorDefaults = computed(() => ({
      BaseListItem: {
        active: isOpen.value,
        activeColor: props.activeColor,
        baseColor: props.baseColor,
        color: props.color,
        prependIcon: props.prependIcon || (props.subgroup && toggleIcon.value),
        appendIcon: props.appendIcon || (!props.subgroup && toggleIcon.value),
        title: props.title,
        value: props.value,
      },
    }))

    return {
      id,
      activatorProps,
      activatorDefaults,
      list,
      isOpen,
      isBooted,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag"
    :class="[
      'base-list-group',
      {
        'base-list-group--prepend': list?.hasPrepend,
        'base-list-group--fluid': $props.fluid,
        'base-list-group--subgroup': $props.subgroup,
        'base-list-group--open': isOpen,
      },
      $props.class,
    ]"
    :style="$props.style"
  >
    <BaseDefaultsProvider v-if="$slots.activator" :defaults="activatorDefaults">
      <BaseListGroupActivator>
        <slot name="activator" v-bind="{ props: activatorProps, isOpen }" />
      </BaseListGroupActivator>
    </BaseDefaultsProvider>

    <MaybeTransition
      :transition="{ component: BaseExpandTransition }"
      :disabled="!isBooted"
    >
      <div
        class="base-list-group__items"
        role="group"
        :aria-labelledby="id"
        v-show="isOpen"
      >
        <slot />
      </div>
    </MaybeTransition>
  </component>
</template>
