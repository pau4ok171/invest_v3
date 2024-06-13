<script lang="ts">
import {defineComponent} from 'vue'
import TextButton from "@/components/UI/buttons/TextButton.vue";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import CompanyDetailAnalystsModalMenu
  from "@/components/company_detail/content_list/summary/analysts/CompanyDetailAnalystsModalMenu.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailHeaderAnalystsButtonModalMenuContainer",
  components: {CompanyDetailAnalystsModalMenu, BaseModalMenuContainer, TextButton},
  computed: {
    totalIdeas() {
      return this.company.analyst_ideas.length
    },
    ...mapGetters({
      company: "companyDetail/getCompany",
    }),
  },
})
</script>

<template>
 <BaseModalMenuContainer>
  <template #button>
    <TextButton>{{ totalIdeas }} Analysts</TextButton>
  </template>
  <template #menu="menuProps">
    <CompanyDetailAnalystsModalMenu @closeMenu="menuProps.close()"/>
  </template>
</BaseModalMenuContainer>
</template>

<style scoped>

</style>