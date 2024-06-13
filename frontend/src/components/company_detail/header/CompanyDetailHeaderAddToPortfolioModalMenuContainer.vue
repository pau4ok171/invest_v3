<script lang="ts">
import {defineComponent} from 'vue'
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import RoundedWhiteButton from "@/components/UI/buttons/RoundedWhiteButton.vue";
import CompanyDetailPortfolioModalMenu
  from "@/components/company_detail/content_list/summary/portfolio/CompanyDetailPortfolioModalMenu.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailHeaderAddToPortfolioModalMenuContainer",
  components: {CompanyDetailPortfolioModalMenu, RoundedWhiteButton, BaseModalMenuContainer},
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
    <RoundedWhiteButton :disabled="!isAuthenticated">
      <span>Add to portfolio</span>
    </RoundedWhiteButton>
  </template>

  <template #menu="menuProps">
    <CompanyDetailPortfolioModalMenu @closeMenu="menuProps.close()" v-if="isAuthenticated"/>
  </template>
</BaseModalMenuContainer>
</template>
