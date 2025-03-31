<script setup lang="ts">
import { defChartOpts } from '@/components/charts/smallPriceChartOpts'
import { computed, ref, watch } from 'vue'
import { useCompanyDetailStore } from '@/store/companyDetail'

const companyDetailStore = useCompanyDetailStore()
const priceData = computed(() => companyDetailStore.chartPriceData)

const chartOpts = ref(defChartOpts)

watch(
  () => priceData.value,
  () => {
    chartOpts.value.series[0].data = priceData.value as []
  }
)
</script>

<template>
  <charts
    class="small-price-history-chart"
    constructorType="stockChart"
    :options="chartOpts"
  />
</template>

<style scoped>
.small-price-history-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 300px;
  max-width: 100%;
  height: 40px;
  line-height: 1.5;
  pointer-events: none;
}
</style>
