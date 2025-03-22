<script setup lang="ts">
const props = defineProps({
  chartName: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="chart-data-not-available">
    <p>Insufficient data to display {{ props.chartName }}</p>
  </div>
</template>

<style scoped>
.chart-data-not-available {
  display: flex;
  justify-content: center;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  height: 100%;
  background-color: var(--bg-color);
  border-radius: 8px;
}
.chart-data-not-available p {
  font-size: 0.875rem;
}
</style>
