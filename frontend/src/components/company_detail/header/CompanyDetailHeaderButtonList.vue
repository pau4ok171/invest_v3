<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailHeaderAdditionalActionsDropDownMenuBox
  from "@/components/company_detail/header/CompanyDetailHeaderAdditionalActionsDropDownMenuBox.vue";
import CompanyDetailHeaderAddToPortfolioModalMenuContainer
  from "@/components/company_detail/header/CompanyDetailHeaderAddToPortfolioModalMenuContainer.vue";
import CompanyDetailHeaderToggleToWatchlist
  from "@/components/company_detail/header/CompanyDetailHeaderToggleToWatchlist.vue";

export default defineComponent({
  name: "CompanyDetailHeaderButtonList",
  components: {
    CompanyDetailHeaderToggleToWatchlist,
    CompanyDetailHeaderAddToPortfolioModalMenuContainer,
    CompanyDetailHeaderAdditionalActionsDropDownMenuBox,
  },
})
</script>

<template>
<div class="detail-header__button-list">

  <CompanyDetailHeaderToggleToWatchlist/>

  <CompanyDetailHeaderAddToPortfolioModalMenuContainer/>

  <CompanyDetailHeaderAdditionalActionsDropDownMenuBox/>

</div>
</template>

<style scoped>
.detail-header__button-list {
  width: 100%;
  display: flex;
  gap: 4px;
  justify-content: flex-end;
  text-align: right;
  margin-top: -30px;
  height: 32px;
}
</style>