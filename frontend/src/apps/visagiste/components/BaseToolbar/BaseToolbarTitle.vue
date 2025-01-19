<script setup lang="ts">
// Types
export type BaseToolbarTitleSlots = {
  default(name: {}): any,
  text(name: {}): any,
}

const props = defineProps({
  text: String,
})
const slots = defineSlots<BaseToolbarTitleSlots>()
const hasText = !!(slots.default || slots.text || props.text)
</script>

<template>
<div class="base-toolbar-title">
  <template v-if="hasText">
    <div class="base-toolbar-title__placeholder">
      <slot name="text">{{ props.text }}</slot>

      <slot name="default"/>
    </div>
  </template>
</div>
</template>