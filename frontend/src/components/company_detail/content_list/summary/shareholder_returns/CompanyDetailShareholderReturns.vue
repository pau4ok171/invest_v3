<script lang="ts">
import {defineComponent} from 'vue'
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import CompanyDetailShareholderReturnsTable
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsTable.vue";
import CompanyDetailStatement from "@/components/company_detail/content_list/CompanyDetailStatement.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import CompanyDetailShareholderReturnsModalMenu
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsModalMenu.vue";

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

  <CompanyDetailStatement name="Is1YearReturnInLineOrAboveIndustry"/>
  <CompanyDetailStatement name="Is1YearReturnInLineOrAboveMarket"/>

</div>
</template>
