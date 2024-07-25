<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminTextField",
  props: {
    isRequired: {
      type: Boolean,
      default: false,
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
  },
})
</script>

<template>
<div class="admin-text-field">
  <textarea
      :required="isRequired"
      :disabled="isDisabled"
      @input="(event: Event) => $emit('update:modelValue', (event.target as HTMLInputElement).value)"
      :value="($attrs.modelValue as any)"
      placeholder="Введите несколько строчек"
  />
</div>
</template>

<style scoped>

</style>