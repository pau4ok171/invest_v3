<script lang="ts">
  import {defineComponent} from 'vue'
  import CheckIcon from "@/components/icons/CheckIcon.vue";
  import CrossIcon from "@/components/icons/CrossIcon.vue";

  export default defineComponent({
    name: "CompanyDetailCheck",
    components: {CrossIcon, CheckIcon},
    props: {
      check: {
        type: Object,
        required: true,
      }
    }
  })
</script>

<template>
  <blockquote class="analysis-section__point">
    <CheckIcon v-if="check.status === 'passed'" class="icon--success"/>
    <CrossIcon v-else class="icon--error"/>

    <p class="analysis-section__point-text">
      <span class="analysis-section__point-title">{{ this.check.title }}: </span>
      <span>{{ this.check.description }}</span>
    </p>
  </blockquote>
</template>

<style scoped>
  .analysis-section__point {
    position: relative;
    display: flex;
    gap: 4px;
    margin-top: 8px;
  }
  .analysis-section__point-text {
    font-size: 1.6rem;
    line-height: 1.5;
    margin-bottom: 8px;
  }
  .icon--success {
    fill: #2dc97e;
  }
  .icon--error {
    fill: #e64141;
  }
</style>