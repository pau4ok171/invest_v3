<script setup lang="ts">
// Utilities
import { BaseSlideGroupSymbol } from './BaseSlideGroup.vue'
import { useGroupItem, useGroupProps } from '@/apps/visagiste/composables/group'

// Types
import type { UnwrapRef } from 'vue'
import type { GroupItemProvide } from '@/apps/visagiste/composables/group'

type BaseSlideGroupItemSlots = {
  default: {
    isSelected: UnwrapRef<GroupItemProvide['isSelected']>
    select: GroupItemProvide['select']
    toggle: GroupItemProvide['toggle']
    selectedClass: UnwrapRef<GroupItemProvide['selectedClass']>
  }
}

const props = defineProps({
  ...useGroupProps(),
})

const emits = defineEmits<{
  'group:selected': (val: { value: boolean }) => true
}>()

const slots = defineSlots<BaseSlideGroupItemSlots>()

const slideGroupItem = useGroupItem(props, BaseSlideGroupSymbol)
</script>

<template>
  <slot
    v-bind="{
      isSelected: slideGroupItem.isSelected,
      select: slideGroupItem.select,
      toggle: slideGroupItem.toggle,
      selectedClass: slideGroupItem.selectedClass,
    }"
  />
</template>
