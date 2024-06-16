<script lang="ts">
import {defineComponent} from 'vue';
import {AtomSpinner} from "epic-spinners";

export default defineComponent({
  name: "FetchingData",
  components: {AtomSpinner}
})
</script>

<template>
<div class="chart-data-not-available">
  <atom-spinner
    :animation-duration="1250"
    :size="30"
    color="#ff1d5e"
  />
  <p>Fetching data from server...</p>
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
  font-size: 1.2rem;
}
</style>