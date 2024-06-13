<script lang="ts">
import {defineComponent} from 'vue'
import BaseModalMenu from "@/components/UI/base/BaseModalMenu.vue";
import TheCompanyDetailRisksTable from "@/components/company_detail/content_list/summary/risks/TheCompanyDetailRisksTable.vue";

export default defineComponent({
  name: "TheCompanyDetailRisksModalMenu",
  components: {TheCompanyDetailRisksTable, BaseModalMenu}
})
</script>

<template>
<BaseModalMenu>
  <template #title>Risk Checks</template>

  <template #content>
    <section class="detail-risks-modal-menu__content">
      <div class="detail-risks-modal-menu__desc">
        <span>
          We perform automated risk checks on every company. We flag any failed checks as potential investment risks. A company which passes all our checks, however, is not 'risk free'.
        </span>
      </div>
      <TheCompanyDetailRisksTable/>
    </section>

  </template>
</BaseModalMenu>
</template>

<style scoped>
.detail-risks-modal-menu__content {
  padding: 12px 24px 32px;
}
.detail-risks-modal-menu__desc {
    margin-bottom: 16px;
    line-height: 1.5;
    font-size: 1.4rem;
}
</style>