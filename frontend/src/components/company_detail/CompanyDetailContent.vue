<template>
  <div class="detail__content">

    <CompanyDetailSidebar
      :company
    />

    <CompanyDetailContentList
      :company
    />

  </div>
</template>

<script lang="ts">
import CompanyDetailSidebar from "@/components/company_detail/CompanyDetailSidebar.vue";
import CompanyDetailContentList from "@/components/company_detail/CompanyDetailContentList.vue";

export default {
  name: 'CompanyDetailContent',
  components: {CompanyDetailContentList, CompanyDetailSidebar},
  props: {
    company: {
      type: Object,
      required: true,
    }
  }
}
</script>

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