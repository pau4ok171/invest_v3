<script setup lang="ts">
// Utilities
import { ref } from 'vue'
import { chartOpts as _chartOpts } from '@/components/charts/multiplierVsFairChart'

const chartOpts = ref(_chartOpts)
</script>

<template>
  <div>
    <charts :options="chartOpts" constructorType="chart" />
  </div>
</template>
