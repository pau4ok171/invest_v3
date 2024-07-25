<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminCharField",
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
<div class="admin-char-field">
  <input
      :required="isRequired"
      :disabled="isDisabled"
      :value="$attrs.modelValue"
      @input="(event: Event) => $emit('update:modelValue', (event.target as HTMLInputElement).value)"
      placeholder="Введите несколько строчек"
  />
</div>
</template>

<style scoped>

</style>