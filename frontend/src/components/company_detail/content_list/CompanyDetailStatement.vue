<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from 'vue';
import type {Statement} from "@/types/statements";

export default defineComponent({
  name: "CompanyDetailStatement",
  props: {
    statement: {
      type: Object as PropType<Statement>,
      required: true,
    }
  }
})
</script>

<template>
<section class="detail-statement">

  <blockquote class="detail-statement-item">
    <p class="detail-statement-item__text">
      <span class="text--error">{{  statement.title }}: </span>
      <span>{{ statement.description }}</span>
    </p>
  </blockquote>

</section>
</template>

<style scoped>
.detail-statement {
  margin-top: 24px;
}
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