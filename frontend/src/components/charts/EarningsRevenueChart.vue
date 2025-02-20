<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/earningsRevenueChart";
import {mapGetters} from "vuex";
import type {Report} from "@/types/invest";
import DataNotAvailable from "@/components/charts/DataNotAvailable.vue";

export default defineComponent({
  name: "EarningsRevenueChart",
  components: {DataNotAvailable},
  data() {
    return {
      chartOpts: chartOpts,
      dataIsAvailable: true,
    }
  },
  mounted() {
    if (!this.company.reports) {
      this.dataIsAvailable = false
      return null
    }
    const report: Report = this.company.reports[0]
    if (!report) {
      this.dataIsAvailable = false
      return null
    }
    const others_expenses = Number((report.gross_margin-report.income_net).toFixed(1))
    const series: any = this.chartOpts.series[0]
    series.data = [{
      name: 'Revenue',
      color: "#2394DF",
      y: report.sales
    }, {
      name: 'Cost of Revenue',
      color: "rgba(230,65,65,.5)",
      y: -report.cost_of_sales
    }, {
      name: 'Gross Profit',
      color: "#2DC97E",
      isIntermediateSum: true,
    }, {
      name: 'Other Expenses',
      color: "rgba(230,65,65,.5)",
      y: -others_expenses
    }, {
      name: 'Earnings',
      color: "#71E7D6",
      isSum: true,
    }] as Array<Object>
    this.chartOpts.series[0].dataLabels.format = `{(abs y):,.f}${report.scale}`
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    })
  },
})
</script>

<template>
<div class="earnings-revenue-chart">
  <DataNotAvailable v-if="!dataIsAvailable" chart-name="Earnings Revenue Chart"/>
  <charts
    v-else
    :constructorType="'chart'"
    :options="chartOpts"
  />
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