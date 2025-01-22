// Composables
import {useProxiedModel} from "@/apps/visagiste/composables/proxiedModel";

// Utilities
import {clamp} from "@/apps/visagiste/utils";
import {computed, inject, provide, watch} from "vue";


// Types
import type {InjectionKey, Ref} from "vue";
import type {EventProp} from "@/apps/visagiste/utils";

export const dataTablePaginateProps = {
  page: {
    type: [Number, String],
    default: 1
  },
  itemsPerPage: {
    type: [Number, String],
    default: 10
  },
}

const BaseDataTablePaginationSymbol: InjectionKey<{
  page: Ref<number>
  itemsPerPage: Ref<number>
  startIndex: Ref<number>
  stopIndex: Ref<number>
  pageCount: Ref<number>
  itemsLength: Ref<number>
  prevPage: () => void
  nextPage: () => void
  setPage: (value: number) => void
  setItemsPerPage: (value: number) => void
}> = Symbol.for('visagiste:data-table-pagination')

type PaginationProps = {
  page: number | string
  'onUpdate:page': EventProp | undefined
  itemsPerPage: number | string
  'onUpdate:itemsPerPage': EventProp | undefined
  itemsLength?: number | string
}

export function createPagination (props: PaginationProps) {
  const page = useProxiedModel(props, 'page',undefined, value => +(value ?? 1))
  const itemsPerPage = useProxiedModel(props, 'itemsPerPage', undefined, value => +(value ?? 10))

  return { page, itemsPerPage }
}

export function providePagination (options: {
  page: Ref<number>
  itemsPerPage: Ref<number>
  itemsLength: Ref<number>
}) {
  const { page, itemsPerPage, itemsLength } = options
  const startIndex = computed(() => {
    if (itemsPerPage.value === -1) return 0

    return itemsPerPage.value * (page.value - 1)
  })
  const stopIndex = computed(() => {
    if (itemsPerPage.value === -1) return itemsLength.value

    return Math.min(itemsLength.value, startIndex.value + itemsPerPage.value)
  })

  const pageCount = computed(() => {
    if (itemsPerPage.value === -1 || itemsLength.value === 0) return 1

    return Math.ceil(itemsLength.value / itemsPerPage.value)
  })

  // Don't run immediately, items may not have been loaded yet
  watch([page, pageCount], () => {
    if (page.value > pageCount.value) {
      page.value = pageCount.value
    }
  })

  function setItemsPerPage (value: number) {
    itemsPerPage.value = value
    page.value = 1
  }

  function nextPage () {
    page.value = clamp(page.value + 1, 1, pageCount.value)
  }

    function prevPage () {
    page.value = clamp(page.value - 1, 1, pageCount.value)
  }

  function setPage (value: number) {
    page.value = clamp(value, 1, pageCount.value)
  }

  const data = { page, itemsPerPage, startIndex, stopIndex, pageCount, itemsLength, nextPage, prevPage, setPage, setItemsPerPage }

  provide(BaseDataTablePaginationSymbol, data)

  return data
}

export function usePagination () {
  const data =inject(BaseDataTablePaginationSymbol)

  if (!data) throw new Error('Missing pagination!')

  return data
}