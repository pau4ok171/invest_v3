<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailAnalystsModalMenu
  from "@/components/company_detail/content_list/summary/analysts/CompanyDetailAnalystsModalMenu.vue";
import {mapGetters} from "vuex";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import BaseDialog from "@/components/UI/base/components/BaseDialog/BaseDialog.vue";

export default defineComponent({
  name: "CompanyDetailHeaderAnalystsButtonModalMenuContainer",
  components: {
    BaseDialog,
    BaseButton,
    CompanyDetailAnalystsModalMenu,
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

  <base-dialog
    title="Analyst Sources"
    max-width="700"
  >
    <template #activator>
      <base-button
        variant="text"
        :text="`${totalIdeas} Analysts`"
        density="comfortable"
        size="small"
        lower
      />
    </template>
    <template #dialog>
       <CompanyDetailAnalystsModalMenu/>
    </template>
  </base-dialog>

</div>
</template>

<style scoped>
.detail-analyst__modal-menu-container {
  margin-bottom: -1px;
  margin-left: -4px;
}
</style>