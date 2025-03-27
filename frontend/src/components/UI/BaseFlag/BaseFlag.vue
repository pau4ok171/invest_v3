<script lang="ts">
// Style
import 'flag-icons/css/flag-icons.min.css'

// Utilities
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'BaseFlag',
  props: {
    code: String,
    square: Boolean,
  },
})
</script>

<template>
  <i
    :class="[
      'base-flag',
      'fi',
      [`fi-${code}`],
      {
        fis: square,
      },
    ]"
  />
</template>
