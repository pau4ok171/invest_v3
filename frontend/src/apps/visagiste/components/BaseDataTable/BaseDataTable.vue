<script lang="ts">
// Styles
import './BaseDataTable.scss'

// Components
import {
  default as BaseDataTableFooter,
  useBaseDataTableFooterProps,
} from './BaseDataTableFooter.vue'
import {
  default as BaseDataTableHeaders,
  useBaseDataTableHeadersProps,
} from './BaseDataTableHeaders.vue'
import {
  default as BaseDataTableRows,
  useBaseDataTableRowsProps,
} from './BaseDataTableRows.vue'
import { BaseDivider } from '@/apps/visagiste/components/BaseDivider'
import {
  BaseTable,
  useBaseTableProps,
} from '@/apps/visagiste/components/BaseTable'

// Composables
import { useDataTableExpandProps, provideExpanded } from './composables/expand'
import {
  useDataTableGroupProps,
  provideGroupBy,
  createGroupBy,
  useGroupedItems,
} from './composables/group'
import { createHeaders, useDataTableHeaderProps } from './composables/headers'
import {
  useDataTableItems,
  useDataTableItemsProps,
} from '@/apps/visagiste/components/BaseDataTable/composables/items'
import { useOptions } from './composables/options'
import {
  useDataTablePaginateProps,
  providePagination,
  createPagination,
  usePaginatedItems,
} from './composables/paginate'
import { useDataTableSelectProps, provideSelection } from './composables/select'
import {
  useDataTableSortProps,
  provideSort,
  createSort,
  useSortedItems,
} from './composables/sort'
import { provideDefaults } from '@/apps/visagiste/composables/defaults'
import { useFilter, useFilterProps } from '@/apps/visagiste/composables/filter'

// Utilities
import { computed, toRef, toRefs } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { UnwrapRef } from 'vue'
import type { Group } from './composables/group'
import type { DataTableItem, InternalDataTableHeader } from './types'
import type { BaseDataTableHeadersSlots } from './BaseDataTableHeaders.vue'
import type { BaseDataTableRowsSlots } from './BaseDataTableRows.vue'

export type BaseDataTableSlotProps<T> = {
  page: number
  itemsPerPage: number
  sortBy: UnwrapRef<ReturnType<typeof provideSort>['sortBy']>
  pageCount: number
  toggleSort: ReturnType<typeof provideSort>['toggleSort']
  setItemPerPage: ReturnType<typeof providePagination>['setItemsPerPage']
  someSelected: boolean
  allSelected: boolean
  isSelected: ReturnType<typeof provideSelection>['isSelected']
  select: ReturnType<typeof provideSelection>['select']
  selectAll: ReturnType<typeof provideSelection>['selectAll']
  toggleSelect: ReturnType<typeof provideSelection>['toggleSelect']
  isExpand: ReturnType<typeof provideExpanded>['isExpanded']
  toggleExpand: ReturnType<typeof provideExpanded>['toggleExpand']
  isGroupOpen: ReturnType<typeof provideGroupBy>['isGroupOpen']
  toggleGroup: ReturnType<typeof provideGroupBy>['toggleGroup']
  items: readonly T[]
  internalItems: readonly DataTableItem[]
  groupedItems: readonly (DataTableItem<T> | Group<DataTableItem<T>>)[]
  columns: InternalDataTableHeader[]
  headers: InternalDataTableHeader[][]
}

export type BaseDataTableSlots<T> = BaseDataTableRowsSlots<T> &
  BaseDataTableHeadersSlots & {
    default: BaseDataTableSlotProps<T>
    colgroup: BaseDataTableSlotProps<T>
    top: BaseDataTableSlotProps<T>
    body: BaseDataTableSlotProps<T>
    tbody: BaseDataTableSlotProps<T>
    thead: BaseDataTableSlotProps<T>
    tfoot: BaseDataTableSlotProps<T>
    bottom: BaseDataTableSlotProps<T>
    'body.prepend': BaseDataTableSlotProps<T>
    'body.append': BaseDataTableSlotProps<T>
    'footer.prepend': never
  }

export const useDataTableProps = propsFactory(
  {
    ...useBaseDataTableRowsProps(),

    hideDefaultBody: Boolean,
    hideDefaultFooter: Boolean,
    hideDefaultHeader: Boolean,
    width: [String, Number],
    search: String,

    ...useDataTableExpandProps(),
    ...useDataTableGroupProps(),
    ...useDataTableHeaderProps(),
    ...useDataTableItemsProps(),
    ...useDataTableSelectProps(),
    ...useDataTableSortProps(),
    ...useBaseDataTableHeadersProps(),
    ...useBaseTableProps(),
  },
  'DataTable'
)

export const useBaseDataTableProps = propsFactory(
  {
    ...useDataTablePaginateProps(),
    ...useDataTableProps(),
    ...useFilterProps(),
    ...useBaseDataTableFooterProps(),
  },
  'BaseDataTable'
)

export default defineComponent({
  name: 'BaseDataTable',
  components: {
    BaseDataTableHeaders,
    BaseDataTableRows,
    BaseDataTableFooter,
    BaseDivider,
    BaseTable,
  },
  props: useBaseDataTableProps(),
  emits: {
    'update:modelValue': (value: any[]) => true,
    'update:page': (value: number) => true,
    'update:itemsPerPage': (value: number) => true,
    'update:sortBy': (value: any) => true,
    'update:options': (value: any) => true,
    'update:groupBy': (value: any) => true,
    'update:expanded': (value: any) => true,
    'update:currentItems': (value: any) => true,
  },
  setup(props) {
    const { groupBy } = createGroupBy(props)
    const { sortBy, multiSort, mustSort } = createSort(props)
    const { page, itemsPerPage } = createPagination(props)
    const { disableSort } = toRefs(props)

    const {
      columns,
      headers,
      sortFunctions,
      sortRawFunctions,
      filterFunctions,
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

    const { toggleSort } = provideSort({ sortBy, multiSort, mustSort, page })
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
    const itemsLength = computed(() => flatItems.value.length)

    const { startIndex, stopIndex, pageCount, setItemsPerPage } =
      providePagination({ page, itemsPerPage, itemsLength })
    const { paginatedItems } = usePaginatedItems({
      items: flatItems,
      startIndex,
      stopIndex,
      itemsPerPage,
    })

    const paginatedItemsWithoutGroups = computed(() =>
      extractRows(paginatedItems.value)
    )

    const {
      isSelected,
      select,
      selectAll,
      toggleSelect,
      someSelected,
      allSelected,
    } = provideSelection(props, {
      allItems: items,
      currentPage: paginatedItemsWithoutGroups,
    })

    const { isExpanded, toggleExpand } = provideExpanded(props)

    useOptions({
      page,
      itemsPerPage,
      sortBy,
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

    const slotProps = computed<BaseDataTableSlotProps<any>>(() => ({
      page: page.value,
      itemsPerPage: itemsPerPage.value,
      sortBy: sortBy.value,
      pageCount: pageCount.value,
      toggleSort,
      setItemsPerPage,
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
      items: paginatedItemsWithoutGroups.value.map((item) => item.raw),
      internalItems: paginatedItemsWithoutGroups.value,
      groupedItems: paginatedItems.value,
      columns: columns.value,
      headers: headers.value,
    }))

    const dataTableFooterProps = computed(() =>
      BaseDataTableFooter.filterProps(props)
    )
    const dataTableHeadersProps = computed(() =>
      BaseDataTableHeaders.filterProps(props)
    )
    const dataTableRowsProps = computed(() =>
      BaseDataTableRows.filterProps(props)
    )
    const tableProps = computed(() => BaseTable.filterProps(props))

    return {
      dataTableFooterProps,
      dataTableHeadersProps,
      dataTableRowsProps,
      paginatedItems,
      tableProps,
      slotProps,
    }
  },
})
</script>

<template>
  <BaseTable
    :class="[
      'base-data-table',
      {
        'base-data-table--show-select': $props.showSelect,
        'base-data-table--loading': $props.loading,
      },
      $props.class,
    ]"
    :style="$props.style"
    v-bind="tableProps"
    :fixedHeader="$props.fixedHeader"
  >
    <template #top><slot name="top" v-bind="slotProps" /></template>

    <template #default>
      <slot name="default" v-bind="slotProps">
        <slot name="colgroup" v-bind="slotProps" />

        <thead v-if="!$props.hideDefaultHeader">
          <BaseDataTableHeaders v-bind="dataTableHeadersProps">
            <template #headers="vSlotProps"
              ><slot name="headers" v-bind="vSlotProps"
            /></template>
          </BaseDataTableHeaders>
        </thead>

        <slot name="thead" v-bind="slotProps" />

        <tbody v-if="!$props.hideDefaultBody">
          <slot name="body.prepend" v-bind="slotProps" />

          <slot name="body" v-bind="slotProps">
            <BaseDataTableRows
              v-bind="{ ...$attrs, ...dataTableRowsProps }"
              :items="paginatedItems"
            >
              <template v-for="(_, name) in ($slots as {})" #[name]="slotData">
                <slot :name="name" v-bind="slotData || {}"/>
              </template>
            </BaseDataTableRows>
          </slot>

          <slot name="body.append" v-bind="slotProps" />
        </tbody>

        <slot name="tbody" v-bind="slotProps" />

        <slot name="tfoot" v-bind="slotProps" />
      </slot>
    </template>

    <template #bottom>
      <slot name="bottom" v-bind="slotProps">
        <template v-if="!$props.hideDefaultFooter">
          <BaseDivider />

          <BaseDataTableFooter v-bind="dataTableFooterProps">
            <template #prepend>
              <slot name="footer.prepend" />
            </template>
          </BaseDataTableFooter>
        </template>
      </slot>
    </template>
  </BaseTable>
</template>