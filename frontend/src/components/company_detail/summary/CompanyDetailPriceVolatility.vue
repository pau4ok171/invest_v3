<script lang="ts">
import {defineComponent} from 'vue'
import PriceVolatilityChart from "@/components/charts/PriceVolatilityChart.vue";
import CompanyDetailStatement from "@/components/company_detail/CompanyDetailStatement.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";

export default defineComponent({
  name: "CompanyDetailPriceVolatility",
  components: {DetailSectionTitle, CompanyDetailStatement, PriceVolatilityChart},
  props: {
    company: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      statement_list : [
        {id: 3, title: 'Stable Share Price', description: 'Insufficient data to determine SBER\'s volatility over the past 3 months', status: 'failed'},
        {id: 4, title: 'Volatility Over Time', description: 'Insufficient data to determine SBER\'s volatility change over the past year', status: 'failed'},
      ]
    }
  }
})
</script>

<template>
  <div>
    <DetailSectionTitle>Price Volatility</DetailSectionTitle>

    <PriceVolatilityChart :company/>

    <CompanyDetailStatement :statement_list/>

  </div>
</template>

<style scoped>

</style>