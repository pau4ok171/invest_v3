<script setup lang="ts">
// Gradients
import ChartPosGradient02 from '@/components/lineair_gradient/ChartPosGradient02.vue'
import ChartNegGradient02 from '@/components/lineair_gradient/ChartNegGradient02.vue'
import Chart05Gradient01 from '@/components/lineair_gradient/Chart05Gradient01.vue'
import Chart05Gradient02 from '@/components/lineair_gradient/Chart05Gradient02.vue'
import ActualBackgroundGradient from "@/components/lineair_gradient/ActualBackgroundGradient.vue";
import YearMarkerGradient from "@/components/lineair_gradient/YearMarkerGradient.vue";
</script>

<template>
  <svg style="display: block; width: 0; height: 0">
    <chart05-gradient01 />
    <chart05-gradient02 />
    <chart-pos-gradient02 />
    <chart-neg-gradient02 />
    <actual-background-gradient />
    <year-marker-gradient />
  </svg>
</template>
