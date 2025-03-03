<script lang="ts">
// Components
import BaseDataTableColumn from '@/apps/visagiste/components/BaseDataTable/BaseDataTableColumn.vue'
import BaseCheckboxButton from '@/apps/visagiste/components/BaseCheckbox/BaseCheckboxButton.vue'
import BaseButton from '@/apps/visagiste/components/BaseButton/BaseButton.vue'

// Composables
import { useGroupBy } from './composables/group'
import { useSelection } from './composables/select'
import { useHeaders } from './composables/headers'

// Utilities
import { computed } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { Group } from './composables/group'

export type BaseDataTableGroupHeaderRowSlots = {
  'data-table-group': {
    item: Group
    count: number
    props: Record<string, unknown>
  }
  'data-table-select': { props: Record<string, unknown> }
}

export const useBaseDataTableGroupHeaderRowProps = propsFactory(
  {
    item: {
      type: Object as PropType<Group>,
      required: true,
    },
  },
  'BaseDataTableGroupHeaderRow'
)

export default defineComponent({
  name: 'BaseDataTableGroupHeaderRow',
  components: { BaseCheckboxButton, BaseButton, BaseDataTableColumn },
  props: useBaseDataTableGroupHeaderRowProps(),
  setup(props) {
    const { isGroupOpen, toggleGroup, extractRows } = useGroupBy()
    const { isSelected, isSomeSelected, select } = useSelection()
    const { columns } = useHeaders()

    const rows = computed(() => {
      return extractRows([props.item])
    })

    const icon = computed(() => (isGroupOpen(props.item) ? '$expand' : '$next'))
    const modelValue = computed(() => isSelected(rows.value))
    const indeterminate = computed(
      () => isSomeSelected(rows.value) && !modelValue
    )

    function onClick() {
      toggleGroup(props.item)
    }

    function selectGroup(v: boolean) {
      select(rows.value, v)
    }

    return {
      rows,
      columns,
      isSelected,
      isSomeSelected,
      select,
      icon,
      modelValue,
      indeterminate,
      onClick,
      selectGroup,
    }
  },
})
</script>

<template>
  <tr
    class="base-data-table-group-header-row"
    :style="{
      '--base-data-table-group-header-row-depth': $props.item?.depth,
    }"
  >
    <template v-for="column in columns">
      <template v-if="column.key === 'data-table-group'">
        <slot
          name="data-table-group"
          v-bind="{
            item: $props.item,
            count: rows.length,
            props: { icon, onClick },
          }"
        >
          <BaseDataTableColumn class="base-data-table-group-header-row__column">
            <BaseButton
              size="small"
              variant="text"
              :icon="icon"
              @click="onClick"
            />
            <span>{{ $props.item?.value }}</span>
            <span>{{ rows.length }}</span>
          </BaseDataTableColumn>
        </slot>
      </template>

      <template v-else-if="column.key === 'data-table-select'">
        <slot
          name="data-table-select"
          v-bind="{
            props: {
              modelValue,
              indeterminate,
              'onUpdate:modelValue': selectGroup,
            },
          }"
        >
          <td>
            <BaseCheckboxButton
              :modelValue="modelValue"
              :indeterminate="indeterminate"
              @update:modelValue="selectGroup"
            />
          </td>
        </slot>
      </template>

      <template v-else>
        <td />
      </template>
    </template>
  </tr>
</template>
