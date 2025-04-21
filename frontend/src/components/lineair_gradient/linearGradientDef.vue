<script setup lang="ts">
// Gradients
import ChartPosGradient02 from '@/components/lineair_gradient/ChartPosGradient02.vue'
import ChartNegGradient02 from '@/components/lineair_gradient/ChartNegGradient02.vue'
import Chart05Gradient01 from '@/components/lineair_gradient/Chart05Gradient01.vue'
import Chart05Gradient02 from '@/components/lineair_gradient/Chart05Gradient02.vue'
import ActualBackgroundGradient from "@/components/lineair_gradient/ActualBackgroundGradient.vue";
import YearMarkerGradient from "@/components/lineair_gradient/YearMarkerGradient.vue";
import Chart01Gradient01 from "@/components/lineair_gradient/Chart01Gradient01.vue";
import Chart01Gradient02 from "@/components/lineair_gradient/Chart01Gradient02.vue";
import Chart02Gradient01 from "@/components/lineair_gradient/Chart02Gradient01.vue";
import Chart02Gradient02 from "@/components/lineair_gradient/Chart02Gradient02.vue";
import Chart03Gradient01 from "@/components/lineair_gradient/Chart03Gradient01.vue";
import Chart03Gradient02 from "@/components/lineair_gradient/Chart03Gradient02.vue";
import Chart04Gradient01 from "@/components/lineair_gradient/Chart04Gradient01.vue";
import Chart04Gradient02 from "@/components/lineair_gradient/Chart04Gradient02.vue";
</script>

<template>
  <svg style="display: block; width: 0; height: 0">
    <chart01-gradient01 />
    <chart01-gradient02 />
    <chart02-gradient01 />
    <chart02-gradient02 />
    <chart03-gradient01 />
    <chart03-gradient02 />
    <chart04-gradient01 />
    <chart04-gradient02 />
    <chart05-gradient01 />
    <chart05-gradient02 />
    <chart-pos-gradient02 />
    <chart-neg-gradient02 />
    <actual-background-gradient />
    <year-marker-gradient />
  </svg>
</template>
