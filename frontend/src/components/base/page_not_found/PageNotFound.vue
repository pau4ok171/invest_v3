<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "PageNotFound",
  mounted() {
    document.title = 'Page Not Found - Finargo'
  },
})
</script>

<template>
<div class="page-not-found">
  PAGE NOT FOUND
</div>
</template>

<style scoped>
.page-not-found {
  display: flex;
  font-size: 5rem;
  align-items: center;
  justify-content: center;
  margin: 100px 0;
}
</style>