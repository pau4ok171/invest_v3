<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailShareholderReturnsTable
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsTable.vue";
import CompanyDetailStatement from "@/components/company_detail/content_list/CompanyDetailStatement.vue";
import DetailSectionTitle from "@/components/UI/text/DetailSectionTitle.vue";
import CompanyDetailShareholderReturnsDialogContent
  from "@/components/company_detail/content_list/summary/shareholder_returns/CompanyDetailShareholderReturnsDialogContent.vue";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import BaseDialog from "@/components/UI/base/components/BaseDialog/BaseDialog.vue";

export default defineComponent({
  name: "CompanyDetailShareholderReturns",
  components: {
    BaseDialog,
    BaseButton,
    CompanyDetailShareholderReturnsDialogContent,
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

  <base-dialog
    title="Shareholder Returns"
    max-width="750"
  >
    <template #activator>
      <base-button
        text="See full shareholders returns"
        theme="dark-blue"
        rounded="large"
        block
      />
    </template>
    <template #dialog>
      <CompanyDetailShareholderReturnsDialogContent/>
    </template>
  </base-dialog>

  <CompanyDetailStatement name="Is1YearReturnInLineOrAboveIndustry"/>
  <CompanyDetailStatement name="Is1YearReturnInLineOrAboveMarket"/>

</div>
</template>
