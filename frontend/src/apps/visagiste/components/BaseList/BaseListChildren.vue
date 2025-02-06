<script lang="ts">
// Components
import BaseListGroup from "./BaseListGroup.vue";
import BaseListItem from "./BaseListItem.vue";
import BaseListItemSubheader from "./BaseListItemSubheader.vue";
import BaseDivider from "../BaseDivider/BaseDivider.vue";

// Utilities
import {h} from "vue";
import { createList } from "./list";
import {defineComponent, propsFactory} from '@/apps/visagiste/utils';

// Types
import type {PropType} from "vue";
import type {InternalListItem} from "./BaseList.vue";
import type {BaseListItemSlots} from "./BaseListItem.vue";

export type BaseListChildrenSlots<T> = {
  [K in keyof Omit<BaseListItemSlots, 'default'>]: BaseListItemSlots[K] & { item: T }
} & {
  default: never
  item: { props: InternalListItem['props'] }
  divider: { props: InternalListItem['props'] }
  subheader: { props: InternalListItem['props'] }
  header: { props: InternalListItem['props'] }
}

export const useBaseListChildrenProps = propsFactory({
  items: Array as PropType<readonly InternalListItem[]>,
  returnObject: Boolean,
}, 'BaseListChildren')

export default defineComponent({
  name: "BaseListChildren",
  components: {
    BaseListItem,
    BaseListGroup,
    BaseListItemSubheader,
    BaseDivider,
  },
  props: useBaseListChildrenProps(),
  setup (props, { slots }) {
    createList()

    return () => {
      // TODO: refactor slots
      if (slots.default?.()[0].children.length) {
        return slots.default()
      } else {
        return props.items?.map(({children, props: itemsProps, type, raw: item}) => {
          console.log('[BaseListChildren] items ', props.items)
          if (type === 'divider') {
            return slots.divider?.({props: itemsProps}) ?? h(BaseDivider, {...itemsProps})
          }

          if (type === 'subheader') {
            return slots.subheader?.({props: itemsProps}) ?? h(BaseListItemSubheader, {...itemsProps})
          }

          const slotsWithItem = {
            subtitle: slots.subtitle ? (slotProps: any) => slots.subtitle?.({...slotProps, item}) : undefined,
            prepend: slots.prepend ? (slotProps: any) => slots.prepend?.({...slotProps, item}) : undefined,
            append: slots.append ? (slotProps: any) => slots.append?.({...slotProps, item}) : undefined,
            title: slots.title ? (slotProps: any) => slots.title?.({...slotProps, item}) : undefined,
          }

          const listGroupProps = BaseListGroup.filterProps(itemsProps)

          return children
            ? h(BaseListGroup, {value: itemsProps?.value, ...listGroupProps}, {
              activator: ({props: activatorProps}) => {
                const listItemProps = {
                  ...itemsProps,
                  ...activatorProps,
                  value: props.returnObject ? item : itemsProps.value,
                }

                return slots.header
                  ? slots.header({props: listItemProps})
                  : h(BaseListItem, {...listItemProps}, slotsWithItem)
              },
              default: () => h(BaseListChildren, {items: children, returnObject: props.returnObject}, slots)
            })
            : slots.item ? slots.item({props: itemsProps}) : h(BaseListItem, {
              ...itemsProps,
              value: props.returnObject ? item : itemsProps.value,
            }, slotsWithItem)
        })
      }
    }
  }
})
</script>
