<script lang="ts">
import {defineComponent} from 'vue'
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";

export default defineComponent({
  name: "QuestionLink",
  components: {ArrowDownIcon}
})
</script>

<template>
  <a href="#" class="detail-question__link">
    <slot/>
    <ArrowDownIcon class="detail-question__icon"/>
  </a>
</template>

<style scoped>
  .detail-question__link {
    display: flex;
    font-size: 1.6rem;
    line-height: 1.5;
    font-weight: 500;
    color: var(--blue);
    text-decoration: underline;
  }
  .detail-question__icon {
    transform: rotate(-90deg);
    margin-left: -6px;
    fill: var(--blue);
  }
</style>