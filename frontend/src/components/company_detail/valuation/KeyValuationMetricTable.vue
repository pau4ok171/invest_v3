<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "KeyValuationMetricTable"
})
</script>

<template>
  <div class="key-valuation-metrics__table-wrapper" hidden>
    <table class="key-valuation-metrics__table">
      <caption>
        SBER key valuation metrics and ratios. From Price to Earnings, Price to Sales and Price to Book to Price to Earnings Growth Ratio, Enterprise Value and EBITDA.
      </caption>
      <thead>
        <tr>
          <th colspan="2">Key Statistics</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <span tabindex="0" class="key-valuation-metrics__table-text">Enterprise Value/Revenue</span>
          </td>
          <td>n/a</td>
        </tr>
        <tr>
          <td>
            <span tabindex="0" class="key-valuation-metrics__table-text">Enterprise Value/EBITDA</span>
          </td>
          <td>n/a</td>
        </tr>
        <tr>
          <td>
            <span tabindex="0" class="key-valuation-metrics__table-text">PEG Ratio</span>
          </td>
          <td>0.3x</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>

</style>