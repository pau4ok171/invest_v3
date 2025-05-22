<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'

const props = defineProps({
  chartName: {
    type: String,
    required: true,
  },
})

const { t } = useI18n()
</script>

<template>
  <div class="chart-data-not-available">
    <p>{{ t('highcharts.dataNotAvailable') }} {{ props.chartName }}</p>
  </div>
</template>

<style lang="scss" scoped>
.chart-data-not-available {
  display: flex;
  justify-content: center;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  text-align: center;
  padding: 16px;
  height: 100%;
  background-color: rgb(var(--base-theme-surface-bright));
  border-radius: 4px;
}
.chart-data-not-available p {
  font-size: 0.875rem;
}
</style>
