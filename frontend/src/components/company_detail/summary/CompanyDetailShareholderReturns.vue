<script lang="ts">
import {defineComponent} from 'vue'
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import CompanyDetailShareholderReturnsTable
  from "@/components/company_detail/summary/CompanyDetailShareholderReturnsTable.vue";
import CompanyDetailStatement from "@/components/company_detail/CompanyDetailStatement.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";

export default defineComponent({
  name: "CompanyDetailShareholderReturns",
  components: {
    DetailSectionTitle,
    CompanyDetailStatement,
    CompanyDetailShareholderReturnsTable,
    RoundedDarkBlueButton
  },
  data() {
    return {
      statement_list : [
        {id: 1, title: 'Return vs Industry', description: 'SBER underperformed the Russian Banks industry which returned -60.5% over the past year', status: 'failed'},
        {id: 2, title: 'Return vs Market', description: 'SBER underperformed the Russian Market which returned -38.2% over the past year', status: 'failed'},
      ]
    }
  }
})
</script>

<template>
  <div>

    <DetailSectionTitle>Shareholder Returns</DetailSectionTitle>

    <CompanyDetailShareholderReturnsTable/>

    <RoundedDarkBlueButton :isFullWidth="true">See full shareholders returns</RoundedDarkBlueButton>

    <CompanyDetailStatement :statement_list/>

  </div>
</template>

<style scoped>

</style>