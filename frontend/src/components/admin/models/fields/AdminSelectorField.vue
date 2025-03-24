<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'
import type { IFormattedSector, IFormattedSelector } from '@/types/admin.types'
import BaseSelect from '@/apps/visagiste/components/BaseSelect/BaseSelect.vue'

export default defineComponent({
  name: 'AdminSelectorField',
  components: {
    BaseSelect,
  },
  props: {
    hasSearch: {
      type: Boolean,
      default: false,
    },
    options: {
      type: Array<IFormattedSector>,
      required: true,
    },
    label: {
      type: String,
      default: 'Label',
    },
    isRequired: {
      type: Boolean,
      default: false,
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
    modelValue: {
      type: Object as PropType<IFormattedSelector>,
      default: { name: '', slug: '', key: '' },
      required: true,
    },
    fieldStatus: {
      type: String,
      required: true,
    },
  },
  methods: {
    updateSelectorOption(option: IFormattedSelector) {
      this.$emit('update:modelValue', option)
      this.$emit('touch')
      this.$emit('commitValidator')
    },
  },
})
</script>

<template>
  <base-select
    baseColor="#ee4297"
    variant="outlined"
    density="compact"
    :label="`${label}${isRequired ? '*' : ''}`"
    rounded
    :modelValue="modelValue"
    :error="fieldStatus === 'invalid'"
    @update:modelValue="updateSelectorOption"
    :items="options"
    item-value="slug"
    item-title="name"
    :disabled="isDisabled"
    return-object
    min-width="280"
    hide-details
  />
</template>