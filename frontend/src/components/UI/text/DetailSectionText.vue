<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "DetailSectionText"
})
</script>

<template>
<p class="detail-section__text"><slot/></p>
</template>

<style scoped>
.detail-section__text {
  font-size: 1.6rem;
  line-height: 1.5;
  margin-bottom: 8px;
}
</style>