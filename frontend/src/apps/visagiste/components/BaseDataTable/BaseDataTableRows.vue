<script lang="ts">
// Components
import BaseDataTableGroupHeaderRow from './BaseDataTableGroupHeaderRow.vue'
import BaseDataTableRow from './BaseDataTableRow.vue'

// Composables
import { useExpanded } from './composables/expand'
import { useGroupBy } from './composables/group'
import { useHeaders } from './composables/headers'
import { useSelection } from './composables/select'
import {
  useDisplayProps,
  useDisplay,
} from '@/apps/visagiste/composables/display'
import { useLocale } from '@/apps/visagiste/composables'

// Utilities
import { mergeProps } from 'vue'
import {
  getPrefixedEventHandlers,
  defineComponent,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { Group } from './composables/group'
import type {
  CellProps,
  DataTableItem,
  GroupHeaderSlot,
  ItemSlot,
  RowProps,
} from './types'
import type { BaseDataTableGroupHeaderRowSlots } from './BaseDataTableGroupHeaderRow.vue'
import type { BaseDataTableRowSlots } from './BaseDataTableRow.vue'

export type BaseDataTableRowsSlots<T> = BaseDataTableGroupHeaderRowSlots &
  BaseDataTableRowSlots<T> & {
    item: ItemSlot<T> & { props: Record<string, any> }
    loading: never
    'group-header': GroupHeaderSlot
    'no-data': never
    'expanded-row': ItemSlot<T>
  }

export const useBaseDataTableRowsProps = propsFactory(
  {
    loading: [Boolean, String],
    loadingText: {
      type: String,
      default: '$visagiste.dataIterator.loadingText',
    },
    hideNoData: Boolean,
    items: {
      type: Array as PropType<readonly (DataTableItem | Group)[]>,
      default: () => [],
    },
    noDataText: {
      type: String,
      default: '$visagiste.noDataText',
    },
    rowProps: [Object, Function] as PropType<RowProps<any>>,
    cellProps: [Object, Function] as PropType<CellProps<any>>,

    ...useDisplayProps(),
  },
  'BaseDataTableRows'
)

export default defineComponent({
  name: 'BaseDataTableRows',
  methods: { mergeProps, getPrefixedEventHandlers },
  components: { BaseDataTableRow, BaseDataTableGroupHeaderRow },
  inheritAttrs: false,
  props: useBaseDataTableRowsProps(),
  setup(props) {
    const { columns } = useHeaders()
    const { expandOnClick, toggleExpand, isExpanded } = useExpanded()
    const { isSelected, toggleSelect } = useSelection()
    const { toggleGroup, isGroupOpen } = useGroupBy()
    const { t } = useLocale()
    const { mobile } = useDisplay(props)

    return {
      columns,
      t,
      isExpanded,
      toggleExpand,
      isSelected,
      toggleSelect,
      toggleGroup,
      isGroupOpen,
      expandOnClick,
      mobile,
    }
  },
})
</script>

<template>
  <template v-if="$props.loading && (!$props.items!.length || $slots.loading)">
    <tr class="base-data-table-rows-loading" key="loading">
      <td :colspan="columns.length">
        <slot name="loading">{{ t($props.loadingText as string) }}</slot>
      </td>
    </tr>
  </template>

  <template
    v-else-if="!$props.loading && !$props.items!.length && !$props.hideNoData"
  >
    <tr class="base-data-table-rows-no-data" key="no-data">
      <td :colspan="columns.length">
        <slot name="no-data">{{ t($props.noDataText as string) }}</slot>
      </td>
    </tr>
  </template>

  <template v-else>
    <template v-for="(item, index) in items" :key="item.key ?? item.index">
      <template v-if="item.type === 'group'">
        <slot
          name="group-header"
          v-bind="{
            index,
            item,
            columns,
            isExpanded,
            toggleExpand,
            isSelected,
            toggleSelect,
            toggleGroup,
            isGroupOpen,
          }"
        >
          <BaseDataTableGroupHeaderRow
            :key="`group-header_${item.id}`"
            :item="item"
            v-bind="
              getPrefixedEventHandlers($attrs, ':group-header', () => ({
                index,
                item,
                columns,
                isExpanded,
                toggleExpand,
                isSelected,
                toggleSelect,
                toggleGroup,
                isGroupOpen,
              }))
            "
          >
            <template #data-table-group="slotProps">
              <slot name="data-table-group" v-bind="slotProps" />
            </template>
            <template #data-table-select="slotProps">
              <slot name="data-table-select" v-bind="slotProps" />
            </template>
          </BaseDataTableGroupHeaderRow>
        </slot>
      </template>

      <template v-else :key="`item_${item.key ?? item.index}`">
        <slot
          name="item"
          v-bind="{
            index,
            item: item.raw,
            internalItem: item,
            columns,
            isExpanded,
            toggleExpand,
            isSelected,
            toggleSelect,
            props: mergeProps(
              {
                key: `item_${item.key ?? item.index}`,
                onClick: expandOnClick
                  ? () => {
                      toggleExpand(item)
                    }
                  : undefined,
                index,
                item,
                cellProps: $props.cellProps,
                mobile,
              },
              getPrefixedEventHandlers($attrs, ':row', () => ({
                index,
                item: item.raw,
                internalItem: item,
                columns,
                isExpanded,
                toggleExpand,
                isSelected,
                toggleSelect,
              })),
              typeof $props.rowProps === 'function'
                ? $props.rowProps({
                    item: item.raw,
                    index,
                    internalItem: item,
                  })
                : $props.rowProps
            ),
          }"
        >
          <BaseDataTableRow
            v-bind="
              mergeProps(
                {
                  key: `item_${item.key ?? item.index}`,
                  onClick: expandOnClick
                    ? () => {
                        toggleExpand(item)
                      }
                    : undefined,
                  index,
                  item,
                  cellProps: $props.cellProps,
                  mobile,
                },
                getPrefixedEventHandlers($attrs, ':row', () => ({
                  index,
                  item: item.raw,
                  internalItem: item,
                  columns,
                  isExpanded,
                  toggleExpand,
                  isSelected,
                  toggleSelect,
                })),
                typeof $props.rowProps === 'function'
                  ? $props.rowProps({
                      item: item.raw,
                      index,
                      internalItem: item,
                    })
                  : $props.rowProps
              )
            "
          >
            <template #item.data-table-select="slotProps">
              <slot name="item.data-table-select" v-bind="slotProps" />
            </template>

            <template #item.data-table-expand="slotProps">
              <slot name="item.data-table-expand" v-bind="slotProps" />
            </template>
          </BaseDataTableRow>
        </slot>

        <slot
          v-if="isExpanded(item)"
          name="expanded-row"
          v-bind="{
            index,
            item: item.raw,
            internalItem: item,
            columns,
            isExpanded,
            toggleExpand,
            isSelected,
            toggleSelect,
          }"
        />
      </template>
    </template>
  </template>
</template>
