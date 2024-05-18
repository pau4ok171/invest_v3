<script lang="ts">
import {defineComponent} from 'vue'
import PriceChart from "@/components/charts/PriceChart.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";

export default defineComponent({
  name: "CompanyDetailPriceHistory",
  components: {DetailSectionTitle, PriceChart}
})
</script>

<template>
<DetailSectionTitle>Price History & Performance</DetailSectionTitle>

<PriceChart/>
</template>
