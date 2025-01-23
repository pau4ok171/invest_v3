import type { Ref } from "vue";
import type { SortItem } from "./sort";
import {deepEqual, getCurrentInstance} from "@/apps/visagiste/utils";
import {computed, watch} from "vue";

export function useOptions ({
  page,
  itemsPerPage,
  sortBy,
  groupBy,
  search,
}: {
  page: Ref<number>
  itemsPerPage: Ref<number>
  sortBy: Ref<readonly SortItem[]>
  groupBy: Ref<readonly SortItem[]>
  search: Ref<string | undefined>
}) {
  const vm = getCurrentInstance('BaseDataTable')

  const options = computed(() => ({
    page: page.value,
    itemsPerPage: itemsPerPage.value,
    sortBy: sortBy.value,
    groupBy: groupBy.value,
    search: search.value,
  }))

  let oldOptions: typeof options.value | null = null
  watch(options, () => {
    if (deepEqual(oldOptions, options.value)) return

    // Reset page when searching
    if (oldOptions && oldOptions.search !== options.value.search) {
      page.value = 1
    }

    vm.emit('update:options', options.value)
    oldOptions = options.value
  }, { deep: true, immediate: true })
}