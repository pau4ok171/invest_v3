<script lang="ts">
import {defineComponent} from 'vue'
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import CompanyDetailShareholderReturnsTable
  from "@/components/company_detail/summary/shareholder_returns/CompanyDetailShareholderReturnsTable.vue";
import CompanyDetailStatement from "@/components/company_detail/CompanyDetailStatement.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import CompanyDetailShareholderReturnsModalMenu
  from "@/components/company_detail/summary/shareholder_returns/CompanyDetailShareholderReturnsModalMenu.vue";

export default defineComponent({
  name: "CompanyDetailShareholderReturns",
  components: {
    CompanyDetailShareholderReturnsModalMenu,
    BaseModalMenuContainer,
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

  <BaseModalMenuContainer>
    <template #button>
      <RoundedDarkBlueButton :isFullWidth="true">
        <span>See full shareholders returns</span>
      </RoundedDarkBlueButton>
    </template>
    <template #menu="menuProps">
      <CompanyDetailShareholderReturnsModalMenu @closeMenu="menuProps.close()"/>
    </template>
  </BaseModalMenuContainer>

  <CompanyDetailStatement :statement_list/>

</div>
</template>
