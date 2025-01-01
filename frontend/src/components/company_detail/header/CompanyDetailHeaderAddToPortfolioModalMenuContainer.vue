<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailPortfolioModalMenu
  from "@/components/company_detail/content_list/summary/portfolio/CompanyDetailPortfolioModalMenu.vue";
import {mapGetters} from "vuex";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import BaseDialog from "@/components/UI/base/components/BaseDialog/BaseDialog.vue";

export default defineComponent({
  name: "CompanyDetailHeaderAddToPortfolioModalMenuContainer",
  components: {BaseDialog, BaseButton, CompanyDetailPortfolioModalMenu},
  computed: {
    ...mapGetters({
      isAuthenticated: 'authModule/getIsAuthenticated',
    }),
  },
})
</script>

<template>
<base-dialog
  title="Add SBER to Portfolio"
  max-width="700"
  footer-type="withoutFooter"
>
  <template #activator>
    <base-button
      text="Add to portfolio"
      color="#000"
      rounded="large"
      size="small"
      lower
      :disabled="!isAuthenticated"
    />
  </template>
  <template #dialog>
    <CompanyDetailPortfolioModalMenu/>
  </template>
</base-dialog>
</template>
