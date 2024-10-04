<script lang="ts">
import {defineComponent} from 'vue'
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import CompanyDetailPortfolioModalMenu
  from "@/components/company_detail/content_list/summary/portfolio/CompanyDetailPortfolioModalMenu.vue";
import {mapGetters} from "vuex";
import BaseButton from "@/components/UI/base/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailHeaderAddToPortfolioModalMenuContainer",
  components: {BaseButton, CompanyDetailPortfolioModalMenu, BaseModalMenuContainer},
  computed: {
    ...mapGetters({
      isAuthenticated: 'authModule/getIsAuthenticated',
    }),
  },
})
</script>

<template>
<BaseModalMenuContainer>
  <template #button>
    <base-button
      text="Add to portfolio"
      color="#000"
      rounded="large"
      size="small"
      lower
      :disabled="!isAuthenticated"
    />
  </template>

  <template #menu="menuProps">
    <CompanyDetailPortfolioModalMenu @closeMenu="menuProps.close()" v-if="isAuthenticated"/>
  </template>
</BaseModalMenuContainer>
</template>
