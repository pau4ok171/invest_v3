<script lang="ts">
// Components
import BaseDataTableColumn from './BaseDataTableColumn.vue'
import { BaseButton } from '@/apps/visagiste/components/BaseButton'
import { BaseCheckboxButton } from '@/apps/visagiste/components/BaseCheckbox'

// Composables
import { useExpanded } from './composables/expand'
import { useHeaders } from './composables/headers'
import { useSelection } from './composables/select'
import { useSort } from './composables/sort'
import { useDisplay, useDisplayProps } from '@/apps/visagiste/composables/display'

// Utilities
import { toDisplayString } from 'vue'
import {
  defineComponent,
  EventProp,
  getObjectValueByPath,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { CellProps, DataTableItem, ItemKeySlot } from './types'
import type { BaseDataTableHeaderCellColumnSlotProps } from './BaseDataTableHeaders.vue'
import type { PropType } from 'vue'

export type BaseDataTableRowSlots<T> = {
  'item.data-table-select': Omit<ItemKeySlot<T>, 'value'>
  'item.data-table-expand': Omit<ItemKeySlot<T>, 'value'>
  'header.data-table-select': BaseDataTableHeaderCellColumnSlotProps
  'header.data-table-expand': BaseDataTableHeaderCellColumnSlotProps
} & {
  [key: `item.${string}`]: ItemKeySlot<T>
  [key: `header.${string}`]: BaseDataTableHeaderCellColumnSlotProps
}

export const useBaseDataTableRowProps = propsFactory(
  {
    index: Number,
    item: Object as PropType<DataTableItem>,
    cellProps: [Object, Function] as PropType<CellProps<any>>,
    onClick: EventProp<[MouseEvent]>(),
    onContextmenu: EventProp<[MouseEvent]>(),
    onDblclick: EventProp<[MouseEvent]>(),

    ...useDisplayProps(),
  },
  'BaseDataTableRow'
)

export default defineComponent({
  name: 'BaseDataTableRow',
  methods: { toDisplayString, getObjectValueByPath },
  components: { BaseButton, BaseCheckboxButton, BaseDataTableColumn },
  props: useBaseDataTableRowProps(),
  setup(props) {
    const { displayClasses, mobile } = useDisplay(props, 'base-data-table__tr')
    const { isSelected, toggleSelect, someSelected, allSelected, selectAll } =
      useSelection()
    const { isExpanded, toggleExpand } = useExpanded()
    const { toggleSort, sortBy, isSorted } = useSort()
    const { columns } = useHeaders()

    return {
      columns,
      mobile,
      displayClasses,
      isSelected,
      toggleSelect,
      someSelected,
      allSelected,
      selectAll,
      isExpanded,
      toggleExpand,
      toggleSort,
      sortBy,
      isSorted,
    }
  },
})
</script>

<template>
  <tr
    :class="[
      'base-data-table__tr',
      {
        'base-data-table__tr--clickable': !!(
          $props.onClick ||
          $props.onContextmenu ||
          $props.onDblclick
        ),
      },
      displayClasses,
    ]"
    @click="$props.onClick"
    @contextmenu="$props.onContextmenu"
    @dblclick="$props.onDblclick"
  >
    <template v-if="$props.item">
      <BaseDataTableColumn
        v-for="(column, i) in columns"
        :align="column.align"
        :class="{
          'base-data-table__td--expanded-row':
            column.key === 'data-table-expand',
          'base-data-table__td--select-row': column.key === 'data-table-select',
        }"
        :fixed="column.fixed"
        :fixed-offset="column.fixedOffset"
        :last-fixed="column.lastFixed"
        :max-width="!mobile ? column.width : undefined"
        :no-padding="
          column.key === 'data-table-select' ||
          column.key === 'data-table-expand'
        "
        :nowrap="column.nowrap"
        :width="!mobile ? column.width : undefined"
        v-bind="{
          ...(typeof $props.cellProps === 'function'
            ? $props.cellProps({
                index: $props.index,
                item: $props.item.raw,
                internalItem: $props.item,
                value: getObjectValueByPath($props.item.columns, column.key),
                column,
              })
            : $props.cellProps),
          ...(typeof column.cellProps === 'function'
            ? column.cellProps({
                index: $props.index,
                item: $props.item.raw,
                internalItem: $props.item,
                value: getObjectValueByPath($props.item.columns, column.key),
              })
            : column.cellProps),
        }"
      >
        <template v-if="$slots[`item.${column.key}`] && !mobile">
          <slot
            :name="`item.${column.key}`"
            v-bind="{
              index: $props.index!,
              item: $props.item.raw,
              internalItem: $props.item,
              value: getObjectValueByPath($props.item.columns, column.key),
              column,
              isSelected,
              toggleSelect,
              isExpanded,
              toggleExpand,
            }"
          />
        </template>

        <template v-else-if="column.key === 'data-table-select'">
          <slot
            name="item.data-table-select"
            v-bind="{
              index: $props.index!,
              item: $props.item.raw,
              internalItem: $props.item,
              value: getObjectValueByPath($props.item.columns, column.key),
              column,
              isSelected,
              toggleSelect,
              isExpanded,
              toggleExpand,
            }"
          >
            <BaseCheckboxButton
              :disabled="!$props.item.selectable"
              :modelValue="isSelected([$props.item])"
              @click.stop="toggleSelect($props.item)"
            />
          </slot>
        </template>

        <template v-else-if="column.key === 'data-table-expand'">
          <slot
            name="item.data-table-expand"
            v-bind="{
              index: $props.index!,
              item: $props.item.raw,
              internalItem: $props.item,
              value: getObjectValueByPath($props.item.columns, column.key),
              column,
              isSelected,
              toggleSelect,
              isExpanded,
              toggleExpand,
            }"
          >
            <BaseButton
              :icon="isExpanded($props.item) ? '$collapse' : '$expand'"
              size="small"
              variant="text"
              @click.stop="toggleExpand($props.item)"
            />
          </slot>
        </template>

        <template v-else-if="!mobile">{{
          toDisplayString(getObjectValueByPath($props.item.columns, column.key))
        }}</template>

        <template v-else>
          <div class="base-data-table__td-title">
            <slot
              :name="`header.${column.key}`"
              v-bind="{
                column,
                selectAll,
                isSorted,
                toggleSort,
                sortBy,
                someSelected,
                allSelected,
                getSortIcon: () => '',
              }"
            >
              {{ column.title }}
            </slot>
          </div>
          <div class="base-data-table__td-value">
            <slot
              :name="`item.${column.key}`"
              v-bind="{
                index: $props.index!,
                item: $props.item.raw,
                internalItem: $props.item,
                value: getObjectValueByPath($props.item.columns, column.key),
                column,
                isSelected,
                toggleSelect,
                isExpanded,
                toggleExpand,
              }"
            >
              {{
                toDisplayString(
                  getObjectValueByPath($props.item.columns, column.key)
                )
              }}
            </slot>
          </div>
        </template>
      </BaseDataTableColumn>
    </template>
  </tr>
</template>
