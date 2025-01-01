<script lang="ts">
import {defineComponent} from 'vue'
import TheCompanyDetailRisksTable from "@/components/company_detail/content_list/summary/risks/TheCompanyDetailRisksTable.vue";

export default defineComponent({
  name: "TheCompanyDetailRisksModalMenu",
  components: {
    TheCompanyDetailRisksTable
  },
})
</script>

<template>
<section class="detail-risks-modal-menu__content">
  <div class="detail-risks-modal-menu__desc">
    <span>
      We perform automated risk checks on every company. We flag any failed checks as potential investment risks. A company which passes all our checks, however, is not 'risk free'.
    </span>
  </div>
  <TheCompanyDetailRisksTable/>
</section>
</template>

<style scoped>
.detail-risks-modal-menu__desc {
  margin-bottom: 16px;
  line-height: 1.5;
  font-size: 1.4rem;
}
</style>