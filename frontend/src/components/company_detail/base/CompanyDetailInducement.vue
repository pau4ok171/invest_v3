<script setup lang="ts">
const props = defineProps({
  question: String,
  response: String,
})
</script>

<template>
  <div class="company-detail-inducement">
    <p class="company-detail-inducement__question">{{ props.question }}</p>
    <a href="#" class="company-detail-inducement__answer">
      {{ props.response }}
      <v-icon icon="$iArrowDown" color="info" />
    </a>
  </div>
</template>

<style lang="scss" scoped>
.company-detail-inducement__question {
  line-height: 1.5;
  font-weight: 500;
  color: rgba(var(--v-theme-on-surface-light), 0.5);
  margin-top: 35px;
}
.company-detail-inducement__answer {
  display: flex;
  line-height: 1.5;
  font-weight: 500;
  color: rgb(var(--base-theme-info));
  text-decoration: underline;
}
.company-detail-inducement__answer i {
  transform: rotate(-90deg);
  margin-left: -6px;
}
</style>
