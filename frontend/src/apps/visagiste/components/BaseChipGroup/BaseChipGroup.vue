<script lang="ts">
// Styles
import './BaseChipGroup.scss'

// Components
import BaseSlideGroup, {useBaseSlideGroupProps} from "../BaseSlideGroup/BaseSlideGroup.vue";

// Composables
import {useComponentProps} from "@/apps/visagiste/composables/component";
import {provideDefaults} from "@/apps/visagiste/composables/defaults";
import {useGroup, useGroupProps} from "@/apps/visagiste/composables/group";
import {useTagProps} from "@/apps/visagiste/composables/tag";
import {provideTheme, useThemeProps} from "@/apps/visagiste/composables/theme";
import {useVariantProps} from "@/apps/visagiste/composables/variant";

// Utilities
import {computed, toRef} from "vue";
import {deepEqual, defineComponent, propsFactory} from '@/apps/visagiste/utils';

// Types
import type {PropType} from "vue";

export const BaseChipGroupSymbol = Symbol.for('visagiste:base-chip-group')

export const useBaseChipGroupProps = propsFactory({
  column: Boolean,
  filter: Boolean,
  valueComparator: {
    type: Function as PropType<typeof deepEqual>,
    default: deepEqual,
  },

  ...useBaseSlideGroupProps(),
  ...useComponentProps(),
  ...useGroupProps({ selectedClass: 'base-chip--selected' }),
  ...useTagProps(),
  ...useThemeProps(),
  ...useVariantProps({ variant: 'tonal' } as const),
}, 'BaseChipGroup')

type BaseChipGroupSlot = {
  default: {
    isSelected: (id: number) => boolean,
    select: (id: number, value: boolean) => void,
    next: () => void,
    prev: () => void,
    selected: readonly number[]
  }
}

export default defineComponent({
  name: "BaseChipGroup",
  components: {BaseSlideGroup},
  props: useBaseChipGroupProps(),
  emits: {
    'update:modelValue': (value: any) => true,
  },
  setup (props) {
    const { themeClasses } = provideTheme(props)
    const { isSelected, select, next, prev, selected } = useGroup(props, BaseChipGroupSymbol)

    provideDefaults({
      BaseChip: {
        color: toRef(props, 'color'),
        disabled: toRef(props, 'disabled'),
        filter: toRef(props, 'filter'),
        variant: toRef(props, 'variant'),
      }
    })

    const slideGroupProps = computed(() => BaseSlideGroup.filterProps(props))

    return {
      slideGroupProps,
      themeClasses,
      isSelected,
      select,
      next,
      prev,
      selected,
    }
  }
})
</script>

<template>
<BaseSlideGroup
  v-bind="{...slideGroupProps}"
  :class="[
    'base-chip-group',
    {
      'base-chip-group--column': $props.column,
    },
    themeClasses,
    $props.class,
  ]"
  :style="$props.style"
>

  <slot v-bind="{
    isSelected,
    select,
    next,
    prev,
    selected,
  }"/>

</BaseSlideGroup>
</template>
