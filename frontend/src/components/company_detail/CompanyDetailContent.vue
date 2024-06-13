<script lang="ts">
import CompanyDetailSidebar from "@/components/company_detail/sidebar/CompanyDetailSidebar.vue";
import CompanyDetailContentList from "@/components/company_detail/content_list/CompanyDetailContentList.vue";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'CompanyDetailContent',
  components: {
    CompanyDetailContentList,
    CompanyDetailSidebar
  },
})
</script>

<template>
<div class="detail__content">

  <CompanyDetailSidebar/>

  <CompanyDetailContentList/>

</div>
</template>

<style>
.detail__content {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
.detail__content-item {
  position: relative;
  flex: 0 0 100%;
  max-width: 100%;
  width: 100%;
  min-height: 0;
}
.detail__point-list {
  margin-top: 3.2rem;
}
</style>