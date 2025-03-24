<script lang="ts">
// Components
import BaseDataTableColumn from './BaseDataTableColumn.vue'
import { BaseCheckboxButton } from '@/apps/visagiste/components/BaseCheckbox'
import { BaseChip } from '@/apps/visagiste/components/BaseChip'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'
import { BaseSelect } from '@/apps/visagiste/components/BaseSelect'

// Composables
import {
  useDisplay,
  useDisplayProps,
} from '@/apps/visagiste/composables/display'
import { IconValue } from '@/apps/visagiste/composables/icons'
import {
  default as LoaderSlot,
  useLoaderProps,
  useLoader,
} from '@/apps/visagiste/composablesV2/loader.vue'
import {
  provideSort,
  useSort,
} from '@/apps/visagiste/components/BaseDataTable/composables/sort'
import {
  provideSelection,
  useSelection,
} from '@/apps/visagiste/components/BaseDataTable/composables/select'
import { useHeaders } from '@/apps/visagiste/components/BaseDataTable/composables/headers'
import { useLocale } from '@/apps/visagiste/composables'
import { useBackgroundColor } from '@/apps/visagiste/composables/color'

// Utilities
import { computed, mergeProps } from 'vue'
import { convertToUnit, defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { CSSProperties, PropType, UnwrapRef, SlotsType } from 'vue'
import type { InternalDataTableHeader } from '@/apps/visagiste/components/BaseDataTable/types'
import type { LoaderSlotProps } from '@/apps/visagiste/composablesV2/loader.vue'
import type { ItemProps } from '@/apps/visagiste/composables/list-items'

export type HeadersSlotProps = {
  headers: InternalDataTableHeader[][]
  columns: InternalDataTableHeader[]
  sortBy: UnwrapRef<ReturnType<typeof provideSort>['sortBy']>
  someSelected: UnwrapRef<ReturnType<typeof provideSelection>['someSelected']>
  allSelected: UnwrapRef<ReturnType<typeof provideSelection>['allSelected']>
  toggleSort: ReturnType<typeof provideSort>['toggleSort']
  selectAll: ReturnType<typeof provideSelection>['selectAll']
  getSortIcon: (column: InternalDataTableHeader) => IconValue
  isSorted: ReturnType<typeof provideSort>['isSorted']
}

export type BaseDataTableHeaderCellColumnSlotProps = {
  column: InternalDataTableHeader
  selectAll: ReturnType<typeof provideSelection>['selectAll']
  isSorted: ReturnType<typeof provideSort>['isSorted']
  toggleSort: ReturnType<typeof provideSort>['toggleSort']
  sortBy: UnwrapRef<ReturnType<typeof provideSort>['sortBy']>
  someSelected: UnwrapRef<ReturnType<typeof provideSelection>['someSelected']>
  allSelected: UnwrapRef<ReturnType<typeof provideSelection>['allSelected']>
  getSortIcon: (column: InternalDataTableHeader) => IconValue
}

export type BaseDataTableHeadersSlots = {
  headers: HeadersSlotProps
  loader: LoaderSlotProps
  'header.data-table-select': BaseDataTableHeaderCellColumnSlotProps
  'header.data-table-expand': BaseDataTableHeaderCellColumnSlotProps
} & { [key: `header.${string}`]: BaseDataTableHeaderCellColumnSlotProps }

export const useBaseDataTableHeadersProps = propsFactory(
  {
    color: String,
    disableSort: Boolean,
    fixedHeader: Boolean,
    multiSort: Boolean,
    sortAscIcon: {
      type: IconValue,
      default: '$sortAsc',
    },
    sortDescIcon: {
      type: IconValue,
      default: '$sortDesc',
    },
    headerProps: {
      type: Object as PropType<Record<string, any>>,
    },

    ...useDisplayProps(),
    ...useLoaderProps(),
  },
  'BaseDataTableHeaders'
)

export default defineComponent({
  name: 'BaseDataTableHeaders',
  methods: { mergeProps, convertToUnit },
  components: {
    BaseCheckboxButton,
    BaseIcon,
    BaseChip,
    BaseSelect,
    BaseDataTableColumn,
    LoaderSlot,
  },
  props: useBaseDataTableHeadersProps(),
  slots: Object as SlotsType<BaseDataTableHeadersSlots>,
  setup(props) {
    const { t } = useLocale()
    const { toggleSort, sortBy, isSorted } = useSort()
    const { someSelected, allSelected, selectAll, showSelectAll } =
      useSelection()
    const { columns, headers } = useHeaders()
    const { loaderClasses } = useLoader(props)

    function getFixedStyles(
      column: InternalDataTableHeader,
      y: number
    ): CSSProperties | undefined {
      if (!props.fixedHeader && !column.fixed) return undefined

      return {
        position: 'sticky',
        left: column.fixed ? convertToUnit(column.fixedOffset) : undefined,
        top: props.fixedHeader
          ? `calc(var(--base-table-header-height) * ${y})`
          : undefined,
      }
    }

    function getSortIcon(column: InternalDataTableHeader) {
      const item = sortBy.value.find((item) => item.key === column.key)

      if (!item) return props.sortAscIcon

      return item.order === 'asc' ? props.sortAscIcon : props.sortDescIcon
    }

    const { backgroundColorClasses, backgroundColorStyles } =
      useBackgroundColor(props, 'color')

    const { displayClasses, mobile } = useDisplay(props)

    const slotProps = computed(
      () =>
        ({
          headers: headers.value,
          columns: columns.value,
          toggleSort,
          isSorted,
          sortBy: sortBy.value,
          someSelected: someSelected.value,
          allSelected: allSelected.value,
          selectAll,
          getSortIcon,
        }) satisfies HeadersSlotProps
    )

    const headerCellClasses = computed(() => [
      'base-data-table__th',
      {
        'base-table__th--sticky': props.fixedHeader,
      },
      displayClasses.value,
      loaderClasses.value,
    ])

    const headerMobileProps = computed(() =>
      mergeProps(props.headerProps ?? {} ?? {})
    )
    const displayItems = computed<ItemProps['items']>(() => {
      return columns.value.filter(
        (column) => column?.sortable && !props.disableSort
      )
    })
    const appendIcon = computed(() => {
      const showSelectColumn = columns.value.find(
        (column) => column.key === 'data-table-select'
      )

      if (showSelectColumn == null) return

      return allSelected.value
        ? '$checkboxOn'
        : someSelected.value
          ? '$checkboxIndeterminate'
          : '$checkboxOff'
    })

    return {
      mobile,
      headers,
      columns,
      slotProps,
      headerMobileProps,
      headerCellClasses,
      getFixedStyles,
      backgroundColorClasses,
      backgroundColorStyles,
      t,
      sortBy,
      toggleSort,
      isSorted,
      getSortIcon,
      selectAll,
      showSelectAll,
      allSelected,
      someSelected,
      appendIcon,
      displayItems,
    }
  },
})
</script>

<template>
  <template v-if="mobile">
    <tr>
      <BaseDataTableColumn
        tag="th"
        :class="[...headerCellClasses]"
        :colspan="headers.length + 1"
        v-bind="headerMobileProps"
      >
        <div class="base-data-table-header__content">
          <BaseSelect
            chips
            class="base-data-table__td-sort-select"
            clearable
            density="default"
            :items="displayItems"
            :label="t('$visagiste.dataTable.sortBy')"
            :multiple="$props.multiSort"
            variant="underlined"
            @click:clear="() => (sortBy = [])"
            :appendIcon="appendIcon"
            @click:append="() => selectAll(!allSelected)"
          >
            <template #chip="{ chipItem }">
              <BaseChip
                @click="
                  chipItem.raw?.sortable
                    ? () => toggleSort(chipItem.raw)
                    : undefined
                "
                @mousedown="
                  (e: MouseEvent) => {
                    e.preventDefault()
                    e.stopPropagation()
                  }
                "
              >
                {{ chipItem.title }}
                <BaseIcon
                  :class="[
                    'base-data-table__td-sort-icon',
                    isSorted(chipItem.raw) &&
                      'base-data-table__td-sort-icon-active',
                  ]"
                  :icon="getSortIcon(chipItem.raw)"
                  size="small"
                />
              </BaseChip>
            </template>
          </BaseSelect>
        </div>
      </BaseDataTableColumn>
    </tr>
  </template>

  <template v-else>
    <slot name="headers" v-bind="slotProps">
      <tr v-for="(row, y) in headers">
        <BaseDataTableColumn
          v-for="(column, x) in row"
          tag="th"
          :align="column.align"
          :class="[
            {
              'base-data-table__th--sortable':
                column.sortable && !$props.disableSort,
              'base-data-table__th--sorted': isSorted(column),
              'base-data-table__th--fixed': column.fixed,
            },
            ...headerCellClasses,
          ]"
          :style="{
            width: convertToUnit(column.width),
            minWidth: convertToUnit(column.width),
            maxWidth: convertToUnit(column.width),
            ...getFixedStyles(column, y),
          }"
          :colspan="column.colspan"
          :rowspan="column.rowspan"
          :onClick="column.sortable ? () => toggleSort(column) : undefined"
          :fixed="column.fixed"
          :nowrap="column.nowrap"
          :last-fixed="column.lastFixed"
          :no-padding="
            column.key === 'data-table-select' ||
            column.key === 'data-table-expand'
          "
          v-bind="
            mergeProps($props.headerProps ?? {}, column.headerProps ?? {})
          "
        >
          <template v-if="$slots[`header.${column.key}`]">
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
                getSortIcon,
              }"
            />
          </template>

          <template v-else-if="column.key === 'data-table-select'">
            <slot
              name="data-table-select"
              v-bind="{
                column,
                selectAll,
                isSorted,
                toggleSort,
                sortBy,
                someSelected,
                allSelected,
                getSortIcon,
              }"
            >
              <BaseCheckboxButton
                v-if="showSelectAll"
                v-model="allSelected"
                :indeterminate="someSelected && !allSelected"
                @update:modelValue="selectAll"
              />
            </slot>
          </template>

          <template v-else>
            <div class="base-data-table-header__content">
              <span>{{ column.title }}</span>
              <template v-if="column.sortable && !$props.disableSort">
                <BaseIcon
                  key="icon"
                  class="base-data-table-header__sort-icon"
                  :icon="getSortIcon(column)"
                />
                <div
                  v-if="$props.multiSort && isSorted(column)"
                  key="badge"
                  :class="[
                    'base-data-table-header__sort-badge',
                    ...backgroundColorClasses,
                  ]"
                  :style="backgroundColorStyles"
                >
                  {{ sortBy.findIndex((_x) => _x.key === column.key) + 1 }}
                </div>
              </template>
            </div>
          </template>
        </BaseDataTableColumn>
      </tr>

      <tr v-if="$props.loading" class="base-data-table-progress">
        <th :colspan="columns.length">
          <LoaderSlot
            name="base-data-table-progress"
            absolute
            active
            :color="typeof loading === 'boolean' ? undefined : loading"
            indeterminate
          >
            <slot name="loader" />
          </LoaderSlot>
        </th>
      </tr>
    </slot>
  </template>
</template>
