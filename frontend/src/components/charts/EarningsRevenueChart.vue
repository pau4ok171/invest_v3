<script setup lang="ts">
// Components
import DataNotAvailable from '@/components/charts/DataNotAvailable.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, onMounted, ref, shallowRef } from 'vue'
import { chartOpts } from '@/components/charts/earningsRevenueChart'

// Types
import type { Report } from '@/types/invest'

const store = useCompanyDetailStore()
const company = computed(() => store.company)

const chartOptions = ref(chartOpts)
const available = shallowRef(true)

onMounted(() => {
  if (!company.value.reports) {
    available.value = false
    return
  }

  const report: Report = company.value.reports[0]
  if (!report) {
    available.value = false
    return null
  }
  const others_expenses = Number(
    (report.gross_margin - report.income_net).toFixed(1)
  )
  const series: any = chartOptions.value.series[0]
  series.data = [
    {
      name: 'Revenue',
      color: '#2394DF',
      y: report.sales,
    },
    {
      name: 'Cost of Revenue',
      color: 'rgba(230,65,65,.5)',
      y: -report.cost_of_sales,
    },
    {
      name: 'Gross Profit',
      color: '#2DC97E',
      isIntermediateSum: true,
    },
    {
      name: 'Other Expenses',
      color: 'rgba(230,65,65,.5)',
      y: -others_expenses,
    },
    {
      name: 'Earnings',
      color: '#71E7D6',
      isSum: true,
    },
  ] as Array<Object>
  chartOptions.value.series[0].dataLabels.format = `{(abs y):,.f}${report.scale}`
})
</script>

<template>
  <div class="earnings-revenue-chart">
    <DataNotAvailable v-if="!available" chart-name="Earnings Revenue Chart" />
    <charts v-else constructorType="chart" :options="chartOptions" />
  </div>
</template>

<style>
.earnings-revenue-chart {
  height: 248px;
}
.earnings-revenue-chart svg {
  height: auto;
  width: auto;
}
</style>
