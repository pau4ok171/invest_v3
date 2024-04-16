<script lang="ts">
import {defineComponent} from 'vue'
import { chartOpts } from "@/components/charts/multiplierVsFairChart";

export default defineComponent({
  name: "MultiplierVsFairChart",
  data() {
    return {
      chartOpts: chartOpts
    }
  },
})
</script>

<template>
  <div class="detail-fair-ratio-chart">
    <charts
      :options="chartOpts"
      :constructorType="'chart'"
    />
  </div>
</template>

<style>
  .detail-fair-ratio-chart svg {
    width: auto;
    height: auto;
  }
</style>