<script setup lang="ts">
// Components
import { AtomSpinner } from 'epic-spinners'
</script>

<template>
  <div class="chart-data-not-available">
    <atom-spinner :animation-duration="1250" :size="30" color="#ff1d5e" />
    <p>Fetching data from server...</p>
  </div>
</template>

<style lang="scss" scoped>
.chart-data-not-available {
  display: flex;
  justify-content: center;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  height: 100%;
  background-color: rgb(var(--base-theme-surface-bright));
  border-radius: 8px;
}
.chart-data-not-available p {
  font-size: 0.75rem;
}
</style>
