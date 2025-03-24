<script lang="ts">
// Components
import BaseListGroup from './BaseListGroup.vue'
import BaseListItem from './BaseListItem.vue'
import BaseListItemSubheader from './BaseListSubheader.vue'
import BaseDivider from '../BaseDivider/BaseDivider.vue'

// Utilities
import { createList } from './list'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { InternalListItem } from './BaseList.vue'
import type { BaseListItemSlots } from './BaseListItem.vue'
import {BaseListGroup} from "@/apps/visagiste/components/BaseList/index";

export type BaseListChildrenSlots<T> = {
  [K in keyof Omit<BaseListItemSlots, 'default'>]: BaseListItemSlots[K] & {
    item: T
  }
} & {
  default: never
  item: { props: InternalListItem['props'] }
  divider: { props: InternalListItem['props'] }
  subheader: { props: InternalListItem['props'] }
  header: { props: InternalListItem['props'] }
}

export const useBaseListChildrenProps = propsFactory(
  {
    items: Array as PropType<readonly InternalListItem[]>,
    returnObject: Boolean,
  },
  'BaseListChildren'
)

export default defineComponent({
  name: 'BaseListChildren',
  computed: {
    BaseListGroup() {
      return BaseListGroup
    }
  },
  components: {
    BaseListItem,
    BaseListGroup,
    BaseListItemSubheader,
    BaseDivider,
  },
  props: useBaseListChildrenProps(),
  setup() {
    createList()
  },
})
</script>

<template>
  <slot name="default">
    <template
      v-for="{ children, props: itemProps, type, raw: item } in $props.items"
    >
      <template v-if="type === 'divider'">
        <slot name="divider" v-bind="{ props: itemProps }">
          <BaseDivider v-bind="itemProps" />
        </slot>
      </template>

      <template v-else-if="type === 'subheader'">
        <slot name="subheader" v-bind="{ props: itemProps }">
          <BaseListItemSubheader v-bind="itemProps" />
        </slot>
      </template>

      <template v-else-if="children">
        <BaseListGroup
          v-bind="{
            value: itemProps?.value,
            ...BaseListGroup.filterProps(itemProps),
          }"
        >
          <template #activator="{ props: activatorProps }">
            <slot
              name="header"
              v-bind="{
                props: {
                  ...itemProps,
                  ...activatorProps,
                  value: $props.returnObject ? item : itemProps.value,
                },
              }"
            >
              <BaseListItem
                v-bind="{
                  ...itemProps,
                  ...activatorProps,
                  value: $props.returnObject ? item : itemProps.value,
                }"
              >
                <template #subtitle="slotProps"
                  ><slot name="subtitle" v-bind="{ ...slotProps, item }"
                /></template>
                <template #prepend="slotProps"
                  ><slot name="prepend" v-bind="{ ...slotProps, item }"
                /></template>
                <template #append="slotProps"
                  ><slot name="append" v-bind="{ ...slotProps, item }"
                /></template>
                <template #title="slotProps"
                  ><slot name="title" v-bind="{ ...slotProps, item }"
                /></template>
              </BaseListItem>
            </slot>
          </template>
          <template #default>
            <BaseListChildren
              :items="children"
              :returnObject="$props.returnObject"
            >
              <template v-for="(_, name) in $slots" #[name]="data">
                <slot :name="name" v-bind="data" />
              </template>
            </BaseListChildren>
          </template>
        </BaseListGroup>
      </template>

      <template v-else>
        <slot name="item" v-bind="{ props: itemProps }">
          <BaseListItem
            v-bind="{
              ...itemProps,
              value: $props.returnObject ? item : itemProps.value,
            }"
          >
            <template #subtitle="slotProps">
              <slot name="subtitle" v-bind="{ ...slotProps, item }" />
            </template>
            <template #prepend="slotProps">
              <slot name="prepend" v-bind="{ ...slotProps, item }" />
            </template>
            <template #append="slotProps">
              <slot name="append" v-bind="{ ...slotProps, item }" />
            </template>
            <template #title="slotProps">
              <slot name="title" v-bind="{ ...slotProps, item }" />
            </template>
          </BaseListItem>
        </slot>
      </template>
    </template>
  </slot>
</template>
