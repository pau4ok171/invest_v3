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
  display: grid;
  height: 100%;
  place-items: center;
}
.chart-data-not-available p {
  font-size: 1.4rem;
}
</style>