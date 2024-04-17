<template>
  <header class="detail-header">

    <CompanyDetailHeaderPicture/>

    <div class="detail-header__element">

      <CompanyDetailBreadcrumbs/>

      <CompanyDetailHeaderLogo/>

      <CompanyDetailHeaderTitle/>

    </div>

    <CompanyDetailHeaderButtonList class="detail-header__element"/>

    <CompanyDetailHeaderInfoPanel class="detail-header__element"/>

  </header>
</template>

<script lang="ts">
  import CompanyDetailHeaderPicture
    from "@/components/company_detail/company_detail_header/CompanyDetailHeaderPicture.vue";
  import CompanyDetailBreadcrumbs
    from "@/components/company_detail/company_detail_header/CompanyDetailHeaderBreadcrumbs.vue";
  import CompanyDetailHeaderLogo from "@/components/company_detail/company_detail_header/CompanyDetailHeaderLogo.vue";
  import CompanyDetailHeaderTitle from "@/components/company_detail/company_detail_header/CompanyDetailHeaderTitle.vue";
  import CompanyDetailHeaderButtonList
    from "@/components/company_detail/company_detail_header/CompanyDetailHeaderButtonList.vue";
  import CompanyDetailHeaderInfoPanel
    from "@/components/company_detail/company_detail_header/CompanyDetailHeaderInfoPanel.vue";

  export default {
    name: 'CompanyDetailHeader',
    components: {
      CompanyDetailHeaderInfoPanel,
      CompanyDetailHeaderButtonList,
      CompanyDetailHeaderTitle,
      CompanyDetailHeaderLogo,
      CompanyDetailBreadcrumbs,
      CompanyDetailHeaderPicture,
    },
  }
</script>

<style scoped>
  .detail-header {
    border-radius: 0 0 8px 8px;
    margin-bottom: 16px;
    padding: 16px 32px;
    background-color: #1b222d;
    background-position: center;
    background-size: cover;
    position: relative;
    z-index: 1;
    min-height: 166px;
    display: flex;
    flex-flow: wrap;
    justify-content: left;
  }
  .detail-header__element {
    position: relative;
    width: 100%;
    max-width: 100%;
    flex: 0 0 100%;
  }
</style>
