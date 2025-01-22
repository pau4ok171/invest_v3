// Composables
import { useProxiedModel } from "@/apps/visagiste/composables/proxiedModel";

// Utilities
import { inject, provide, toRef } from "vue";

// Types
import type { InjectionKey, PropType, Ref } from "vue";
import type { DataTableItem } from "../types";

export const dataTableExpandProps = {
  expandOnClick: Boolean,
  showExpand: Boolean,
  expanded: {
    type: Array as PropType<readonly string[]>,
    default: () => ([]),
  },
}

export const BaseDataTableExpandedKey: InjectionKey<{
  expand: (item: DataTableItem, value: boolean) => void
  expanded: Ref<Set<string>>
  expandOnClick: Ref<boolean | undefined>
  isExpanded: (item: DataTableItem) => boolean
  toggleExpand: (item: DataTableItem) => void
}> = Symbol.for('visagiste:data-table-expanded')

type ExpandProps = {
  expandOnClick: boolean
  expanded: readonly string[]
  'onUpdate:expanded': ((value: any[]) => void) | undefined
}

export function provideExpanded (props: ExpandProps) {
  const expandOnClick = toRef(props, 'expandOnClick')
  const expanded = useProxiedModel(props, 'expanded', props.expanded, v => {
    return new Set(v)
  }, v => {
    return [...v.values()]
  })

  function expand (item: DataTableItem, value: boolean) {
    const newExpanded = new Set(expanded.value)

    if (!value) {
      newExpanded.delete(item.value)
    } else {
      newExpanded.add(item.value)
    }

    expanded.value = newExpanded
  }

  function isExpanded (item: DataTableItem) {
    return expanded.value.has(item.value)
  }

  function toggleExpand (item: DataTableItem) {
    expand(item, !isExpanded(item))
  }

  const data = { expand, expanded, expandOnClick, isExpanded, toggleExpand }

  provide(BaseDataTableExpandedKey, data)

  return data
}

export function useExpanded () {
  const data = inject(BaseDataTableExpandedKey)

  if (!data) throw Error('Missing expand!')

  return data
}