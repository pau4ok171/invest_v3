<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "QuestionText"
})
</script>

<template>
<p class="detail-question__text"><slot/></p>
</template>

<style scoped>
.detail-question__text {
  font-size: 1.6rem;
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, .5);
  margin-top: 35px;
}
</style>