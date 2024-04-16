<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/multiplierVsPeersChart";

export default defineComponent({
  name: "MultiplierVsPeersChart",
  data() {
    return {
      chartOpts: chartOpts
    }
  },
})
</script>

<template>
  <div class="detail-multiplier-vs-peers-chart">
    <charts
      :options="chartOpts"
      :constructorType="'chart'"
    />
  </div>
</template>

<style>
  .detail-multiplier-vs-peers-chart svg {
    height: auto;
    width: auto;
  }
  .multiple-vs-peers-chart__v-axis-name {
    fill: rgb(255, 255, 255);
    border-bottom: 1px dotted rgb(35, 148, 223);
    width: fit-content;
    line-height: 16px;
    opacity: 0.7;
    font-size: 1.2rem;
}
.multiple-vs-peers-chart__middle-label-name {
  fill: #1b222d;
  font-size: 1.3rem;
}
.multiple-vs-peers-chart__data-label-value {
  line-height: 1.5;
  font-weight: 500;
  color: #fff;
  font-size: 1.4rem;
}
.multiple-vs-peers-chart__data-label-name {
  line-height: 1.5;
  color: rgba(255, 255, 255, .8);
  padding-right: 10px;
  font-weight: normal;
  font-size: 1.4rem;
}
.multiple-vs-peers-chart__data-label-name--selected {
  background: linear-gradient(270deg, rgb(35, 148, 223) 0%, rgb(35, 148, 223) 100%);
  padding: 0 6px;
  border-radius: 4px;
  margin-top: 2px;
  color: rgb(255, 255, 255);
}
</style>