<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "BaseToolbarItems"
})
</script>

<template>
<div class="base-toolbar-items">
  <slot/>
</div>
</template>
