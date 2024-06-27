<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters} from "vuex";

export default defineComponent({
  name: "KeyValuationMetricTable",
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_caption_desc() {
      if (!this.company.slug) return ''
      return `${this.company.slug.toUpperCase()} key valuation metrics and ratios. From Price to Earnings, Price to Sales and Price to Book to Price to Earnings Growth Ratio, Enterprise Value and EBITDA.`
    }
  },
})
</script>

<template>
<div class="key-valuation-metrics__table-wrapper">
  <table class="key-valuation-metrics__table">
    <caption>{{ get_caption_desc }}</caption>
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
.key-valuation-metrics__table-wrapper {
  min-height: 280px;
}
.key-valuation-metrics__table {
  line-height: 1.5;
  font-weight: 500;
  width: 100%;
  border-spacing: 0;
  font-size: 1.6rem;
  margin-top: 0;
}
.key-valuation-metrics__table caption {
  line-height: 1.5;
  opacity: 0.5;
  padding-top: 8px;
  caption-side: bottom;
  text-align: left;
  font-size: 1.2rem;
}
.key-valuation-metrics__table th {
  text-align: left;
  line-height: 1.5;
  font-weight: 500;
  font-size: 1.2rem;
}
.key-valuation-metrics__table td {
  font-size: 1.6rem;
  box-sizing: border-box;
  height: 38px;
  padding-bottom: 8px;
  vertical-align: bottom;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.key-valuation-metrics__table-text {
  line-height: 1.5;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  border-bottom: 1px dotted rgb(35, 148, 223);
  cursor: help;
  width: fit-content;
  font-size: 1.6rem;
}
</style>
