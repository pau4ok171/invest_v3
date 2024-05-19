<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: 'BaseInput',
  props: {
    inputValue: [Number, String],
  },
  methods: {
    updateInput(event: Event) {
      const target = event.target as HTMLInputElement
      this.$emit('updateInput', target.value)
    }
  },
})
</script>

<template>
<input
    type="text"
    class="input"
    :value="inputValue"
    @input="updateInput"
    placeholder="Type to input..."
>
</template>