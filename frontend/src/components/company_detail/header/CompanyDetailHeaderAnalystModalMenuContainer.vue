<script lang="ts">
import {defineComponent} from 'vue'
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import CompanyDetailAnalystsModalMenu
  from "@/components/company_detail/content_list/summary/analysts/CompanyDetailAnalystsModalMenu.vue";
import {mapGetters} from "vuex";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailHeaderAnalystsButtonModalMenuContainer",
  components: {
    BaseButton,
    CompanyDetailAnalystsModalMenu,
    BaseModalMenuContainer
  },
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
<div class="detail-analyst__modal-menu-container">

 <BaseModalMenuContainer>
  <template #button>
    <base-button
      variant="text"
      :text="`${totalIdeas} Analysts`"
      density="comfortable"
      size="small"
      lower
    />
  </template>
  <template #menu="menuProps">
    <CompanyDetailAnalystsModalMenu @closeMenu="menuProps.close()"/>
  </template>
</BaseModalMenuContainer>
</div>
</template>

<style scoped>
.detail-analyst__modal-menu-container {
  margin-bottom: -1px;
  margin-left: -4px;
}
</style>