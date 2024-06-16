<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "DataNotAvailable",
  props: {
    chartName: {
      type: String,
      required: true,
    }
  },
})
</script>

<template>
<div class="chart-data-not-available">
  <p>Insufficient data to display {{ chartName }}</p>
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
  font-size: 1.4rem;
}
</style>