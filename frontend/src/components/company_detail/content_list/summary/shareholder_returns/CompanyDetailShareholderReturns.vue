<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailShareholderReturnsTable
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsTable.vue";
import CompanyDetailStatement from "@/components/company_detail/content_list/CompanyDetailStatement.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import CompanyDetailShareholderReturnsModalMenu
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsModalMenu.vue";
import BaseButton from "@/components/UI/base/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailShareholderReturns",
  components: {
    BaseButton,
    CompanyDetailShareholderReturnsModalMenu,
    BaseModalMenuContainer,
    DetailSectionTitle,
    CompanyDetailStatement,
    CompanyDetailShareholderReturnsTable,
  },
})
</script>

<template>
<div>

  <DetailSectionTitle>Shareholder Returns</DetailSectionTitle>

  <CompanyDetailShareholderReturnsTable/>

  <BaseModalMenuContainer>
    <template #button>
      <base-button
        text="See full shareholders returns"
        theme="dark-blue"
        rounded="large"
        block
      />
    </template>
    <template #menu="menuProps">
      <CompanyDetailShareholderReturnsModalMenu @closeMenu="menuProps.close()"/>
    </template>
  </BaseModalMenuContainer>

  <CompanyDetailStatement name="Is1YearReturnInLineOrAboveIndustry"/>
  <CompanyDetailStatement name="Is1YearReturnInLineOrAboveMarket"/>

</div>
</template>
