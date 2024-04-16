<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CompanyDetailStatementItem",
  props: {
    statement: {
      type: Object,
      required: true,
    }
  }
})
</script>

<template>
  <blockquote class="detail-statement-item">
    <p class="detail-statement-item__text">
      <span class="text--error">{{  statement.title }}:</span>
      <span> {{ statement.description }}</span>
    </p>
  </blockquote>
</template>

<style scoped>
  .detail-statement-item {
    position: relative;
    margin-top: 8px;
    text-align: left;
  }
  .detail-statement-item__text {
    font-size: 1.6rem;
    line-height: 1.5;
  }
</style>