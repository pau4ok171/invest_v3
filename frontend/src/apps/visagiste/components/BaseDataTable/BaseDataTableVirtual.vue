<script lang="ts">
// Components
import { BaseTable } from '@/apps/visagiste/components/BaseTable'
import { useDataTableProps } from './BaseDataTable.vue'
import BaseDataTableHeaders from './BaseDataTableHeaders.vue'
import BaseDataTableRows from './BaseDataTableRows.vue'
import BaseVirtualScrollItem from '@/apps/visagiste/components/BaseVirtualScroll/BaseVirtualScrollItem.vue'
import BaseDataTableRow from '@/apps/visagiste/components/BaseDataTable/BaseDataTableRow.vue'

// Composables
import { createHeaders } from '@/apps/visagiste/components/BaseDataTable/composables/headers'
import { useDataTableItems } from '@/apps/visagiste/components/BaseDataTable/composables/items'
import { provideSelection } from '@/apps/visagiste/components/BaseDataTable/composables/select'
import { provideExpanded } from '@/apps/visagiste/components/BaseDataTable/composables/expand'
import { useOptions } from '@/apps/visagiste/components/BaseDataTable/composables/options'
import { provideDefaults } from '@/apps/visagiste/composables/defaults'
import {
  createGroupBy,
  provideGroupBy,
  useDataTableGroupProps,
  useGroupedItems,
} from '@/apps/visagiste/components/BaseDataTable/composables/group'
import {
  createSort,
  provideSort,
  useSortedItems,
} from '@/apps/visagiste/components/BaseDataTable/composables/sort'
import {
  useVirtual,
  useVirtualProps,
} from '@/apps/visagiste/composables/virtual'
import { useFilter, useFilterProps } from '@/apps/visagiste/composables/filter'

// Utilities
import { computed, shallowRef, toRef, toRefs } from 'vue'
import {
  convertToUnit,
  defineComponent,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { BaseDataTableSlotProps } from './BaseDataTable.vue'
import type { BaseDataTableRowsSlots } from './BaseDataTableRows.vue'
import type { BaseDataTableHeadersSlots } from './BaseDataTableHeaders.vue'
import type { TemplateRef } from '@/apps/visagiste/utils'

type BaseDataTableVirtualSlotProps<T> = Omit<
  BaseDataTableSlotProps<T>,
  'setItemsPerPage' | 'page' | 'pageCount' | 'itemsPerPage'
>

export type BaseDataTableVirtualSlots<T> = BaseDataTableRowsSlots<T> &
  BaseDataTableHeadersSlots & {
    colgroup: BaseDataTableVirtualSlotProps<T>
    top: BaseDataTableVirtualSlotProps<T>
    headers: BaseDataTableHeadersSlots['headers']
    bottom: BaseDataTableVirtualSlotProps<T>
    'body.prepend': BaseDataTableVirtualSlotProps<T>
    'body.append': BaseDataTableVirtualSlotProps<T>
    item: {
      itemRef: TemplateRef
    }
  }

export const useBaseDataTableVirtualProps = propsFactory(
  {
    ...useDataTableProps(),
    ...useDataTableGroupProps(),
    ...useVirtualProps(),
    ...useFilterProps(),
  },
  'BaseDataTableVirtual'
)

export default defineComponent({
  name: 'BaseDataTableVirtual',
  methods: { convertToUnit },
  components: {
    BaseDataTableRow,
    BaseVirtualScrollItem,
    BaseDataTableRows,
    BaseDataTableHeaders,
    BaseTable,
  },
  props: useBaseDataTableVirtualProps(),
  emits: {
    'update:modelValue': (value: any[]) => true,
    'update:sortBy': (value: any) => true,
    'update:options': (value: any) => true,
    'update:groupBy': (value: any) => true,
    'update:expanded': (value: any) => true,
  },
  setup(props) {
    const { groupBy } = createGroupBy(props)
    const { sortBy, multiSort, mustSort } = createSort(props)
    const { disableSort } = toRefs(props)

    const {
      columns,
      headers,
      filterFunctions,
      sortFunctions,
      sortRawFunctions,
    } = createHeaders(props, {
      groupBy,
      showSelect: toRef(props, 'showSelect'),
      showExpand: toRef(props, 'showExpand'),
    })
    const { items } = useDataTableItems(props, columns)

    const search = toRef(props, 'search')
    const { filteredItems } = useFilter(props, items, search, {
      transform: (item) => item.columns,
      customKeyFilter: filterFunctions,
    })

    const { toggleSort } = provideSort({ sortBy, multiSort, mustSort })
    const { sortByWithGroups, opened, extractRows, isGroupOpen, toggleGroup } =
      provideGroupBy({ groupBy, sortBy, disableSort })

    const { sortedItems } = useSortedItems(
      props,
      filteredItems,
      sortByWithGroups,
      {
        transform: (item) => ({ ...item.raw, ...item.columns }),
        sortFunctions,
        sortRawFunctions,
      }
    )
    const { flatItems } = useGroupedItems(sortedItems, groupBy, opened)

    const allItems = computed(() => extractRows(flatItems.value))

    const {
      isSelected,
      select,
      selectAll,
      toggleSelect,
      someSelected,
      allSelected,
    } = provideSelection(props, {
      allItems,
      currentPage: allItems,
    })
    const { isExpanded, toggleExpand } = provideExpanded(props)

    const {
      containerRef,
      markerRef,
      paddingTop,
      paddingBottom,
      computedItems,
      handleItemResize,
      handleScroll,
      handleScrollend,
    } = useVirtual(props, flatItems)
    const displayItems = computed(() =>
      computedItems.value.map((item) => item.raw)
    )

    useOptions({
      sortBy,
      page: shallowRef(1),
      itemsPerPage: shallowRef(-1),
      groupBy,
      search,
    })

    provideDefaults({
      BaseDataTableRows: {
        hideNoData: toRef(props, 'hideNoData'),
        noDataText: toRef(props, 'noDataText'),
        loading: toRef(props, 'loading'),
        loadingText: toRef(props, 'loadingText'),
      },
    })

    const slotProps = computed(() => ({
      sortBy: sortBy.value,
      toggleSort,
      someSelected: someSelected.value,
      allSelected: allSelected.value,
      isSelected,
      select,
      selectAll,
      toggleSelect,
      isExpanded,
      toggleExpand,
      isGroupOpen,
      toggleGroup,
      items: allItems.value.map((item) => item.raw),
      internalItems: allItems.value,
      groupedItems: flatItems.value,
      columns: columns.value,
      headers: headers.value,
    }))

    const dataTableHeadersProps = computed(() =>
      BaseDataTableHeaders.filterProps(props)
    )
    const dataTableRowsProps = computed(() =>
      BaseDataTableRows.filterProps(props)
    )
    const tableProps = computed(() => BaseTable.filterProps(props))

    return {
      dataTableHeadersProps,
      dataTableRowsProps,
      tableProps,
      slotProps,
      containerRef,
      markerRef,
      handleScroll,
      handleScrollend,
      handleItemResize,
      paddingTop,
      paddingBottom,
      columns,
      displayItems,
    }
  },
})
</script>

<template>
  <BaseTable
    :class="[
      'base-data-table',
      {
        'base-data-table--loading': $props.loading,
      },
      $props.class,
    ]"
    :style="$props.style"
    :fixedHeader="$props.fixedHeader"
    v-bind="tableProps"
  >
    <template #top><slot name="top" v-bind="slotProps" /></template>
    <template #wrapper>
      <div
        ref="containerRef"
        @scroll.passive="handleScroll"
        @scrollend="handleScrollend"
        class="base-table__wrapper"
        :style="{ height: convertToUnit($props.height) }"
      >
        <table>
          <slot name="colgroup" v-bind="slotProps" />

          <thead v-if="!$props.hideDefaultHeader" key="thead">
            <BaseDataTableHeaders v-bind="dataTableHeadersProps">
              <template #headers><slot name="headers" /></template>
              <template #data-table-select
                ><slot name="data-table-select"
              /></template>
            </BaseDataTableHeaders>
          </thead>

          <tbody v-if="!$props.hideDefaultBody">
            <tr
              ref="markerRef"
              :style="{ height: convertToUnit(paddingTop), border: 0 }"
            >
              <td :colspan="columns.length" :style="{ height: 0, border: 0 }" />
            </tr>

            <slot name="body.prepend" v-bind="slotProps" />

            <BaseDataTableRows
              v-bind="{ ...$attrs, ...dataTableRowsProps }"
              :items="displayItems"
            >
              <template #item="itemSlotProps">
                <BaseVirtualScrollItem
                  :key="itemSlotProps.internalItem.index"
                  renderless
                  @update:height="
                    (height) =>
                      handleItemResize(
                        itemSlotProps.internalItem.index,
                        height
                      )
                  "
                >
                  <template #default="{ itemRef }">
                    <slot name="item" v-bind="{ ...itemSlotProps, itemRef }">
                      <BaseDataTableRow
                        v-bind="itemSlotProps.props"
                        ref="itemRef"
                        :key="itemSlotProps.internalItem.index"
                        :index="itemSlotProps.internalItem.index"
                      >
                        <template
                          v-for="(_, name) in $slots"
                          #[name]="vSlotProps"
                        >
                          <slot :name="name" v-bind="vSlotProps || {}" />
                        </template>
                      </BaseDataTableRow>
                    </slot>
                  </template>
                </BaseVirtualScrollItem>
              </template>

              <template v-for="(_, name) in ($slots as {})" #[name]="slotData">
                <slot :name="name" v-bind="slotData || {}"/>
              </template>

            </BaseDataTableRows>

            <slot name="body.append" v-bind="slotProps" />

            <tr :style="{ height: convertToUnit(paddingBottom), border: 0 }">
              <td :colspan="columns.length" :style="{ height: 0, border: 0 }" />
            </tr>
          </tbody>
        </table>
      </div>
    </template>
    <template #bottom><slot name="bottom" v-bind="slotProps" /></template>
  </BaseTable>
</template>
