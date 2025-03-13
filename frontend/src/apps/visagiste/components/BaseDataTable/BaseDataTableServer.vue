<script lang="ts">
// Components
import { BaseTable } from '@/apps/visagiste/components/BaseTable'
import { useDataTableProps } from './BaseDataTable.vue'
import BaseDataTableHeaders from './BaseDataTableHeaders.vue'
import BaseDataTableRows from './BaseDataTableRows.vue'
import BaseDataTableFooter, {
  useBaseDataTableFooterProps,
} from './BaseDataTableFooter.vue'
import BaseDivider from '@/apps/visagiste/components/BaseDivider/BaseDivider.vue'

// Composables
import { createHeaders } from '@/apps/visagiste/components/BaseDataTable/composables/headers'
import { useDataTableItems } from '@/apps/visagiste/components/BaseDataTable/composables/items'
import { provideSelection } from '@/apps/visagiste/components/BaseDataTable/composables/select'
import { provideExpanded } from '@/apps/visagiste/components/BaseDataTable/composables/expand'
import { useOptions } from '@/apps/visagiste/components/BaseDataTable/composables/options'
import { provideDefaults } from '@/apps/visagiste/composables/defaults'
import {
  createPagination,
  providePagination,
  useDataTablePaginateProps,
} from './composables/paginate'
import {
  createGroupBy,
  provideGroupBy,
  useGroupedItems,
} from '@/apps/visagiste/components/BaseDataTable/composables/group'
import {
  createSort,
  provideSort,
} from '@/apps/visagiste/components/BaseDataTable/composables/sort'

// Utilities
import { computed, provide, toRef, toRefs } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { BaseDataTableSlotProps } from './BaseDataTable.vue'

export const useBaseDataTableServerProps = propsFactory(
  {
    itemsLength: {
      type: [Number, String],
      required: true,
    },

    ...useDataTablePaginateProps(),
    ...useDataTableProps(),
    ...useBaseDataTableFooterProps(),
  },
  'BaseDataTableServer'
)

export default defineComponent({
  name: 'BaseDataTableServer',
  components: {
    BaseDataTableFooter,
    BaseDivider,
    BaseDataTableRows,
    BaseDataTableHeaders,
    BaseTable,
  },
  props: useBaseDataTableServerProps(),
  emits: {
    'update:modelValue': (value: any[]) => true,
    'update:page': (value: number) => true,
    'update:itemsPerPage': (value: number) => true,
    'update:sortBy': (value: any) => true,
    'update:options': (value: any) => true,
    'update:groupBy': (value: any) => true,
    'update:expanded': (value: any) => true,
  },
  setup(props) {
    const { groupBy } = createGroupBy(props)
    const { sortBy, multiSort, mustSort } = createSort(props)
    const { page, itemsPerPage } = createPagination(props)
    const { disableSort } = toRefs(props)
    const itemsLength = computed(() =>
      parseInt(props.itemsLength as string, 10)
    )

    const { columns, headers } = createHeaders(props, {
      groupBy,
      showSelect: toRef(props, 'showSelect'),
      showExpand: toRef(props, 'showExpand'),
    })

    const { items } = useDataTableItems(props, columns)

    const { toggleSort } = provideSort({ sortBy, multiSort, mustSort, page })

    const { opened, isGroupOpen, toggleGroup, extractRows } = provideGroupBy({
      groupBy,
      sortBy,
      disableSort,
    })

    const { pageCount, setItemsPerPage } = providePagination({
      page,
      itemsPerPage,
      itemsLength,
    })

    const { flatItems } = useGroupedItems(items, groupBy, opened)

    const {
      isSelected,
      select,
      selectAll,
      toggleSelect,
      someSelected,
      allSelected,
    } = provideSelection(props, {
      allItems: items,
      currentPage: items,
    })

    const { isExpanded, toggleExpand } = provideExpanded(props)

    const itemsWithoutGroups = computed(() => extractRows(items.value))

    useOptions({
      page,
      itemsPerPage,
      sortBy,
      groupBy,
      search: toRef(props, 'search'),
    })

    provide('base-data-table', {
      toggleSort,
      sortBy,
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
      items: itemsWithoutGroups.value.map((item) => item.raw),
      internalItems: itemsWithoutGroups.value,
      groupedItems: flatItems.value,
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
      tableProps,
      dataTableFooterProps,
      dataTableHeadersProps,
      dataTableRowsProps,
      slotProps,
      flatItems,
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

    <template #default>
      <slot name="default" v-bind="slotProps">
        <slot name="colgroup" v-bind="slotProps" />

        <thead
          v-if="!$props.hideDefaultHeader"
          key="thead"
          class="base-data-table__thead"
          role="rowgroup"
        >
          <BaseDataTableHeaders v-bind="dataTableHeadersProps">
            <template #headers="vSlotProps"><slot name="headers" v-bind="vSlotProps" /></template>
            <template #data-table-select>
              <slot name="data-table-select"/>
            </template>
          </BaseDataTableHeaders>
        </thead>

        <slot name="thead" v-bind="slotProps" />

        <tbody
          v-if="!$props.hideDefaultBody"
          class="base-data-table__tbody"
          role="rowgroup"
        >
          <slot name="body.prepend" v-bind="slotProps" />

          <slot name="body" v-bind="slotProps">
            <BaseDataTableRows
              v-bind="{ ...$attrs, ...dataTableRowsProps }"
              :items="flatItems"
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
