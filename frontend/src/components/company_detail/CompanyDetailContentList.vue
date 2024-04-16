<template>
  <div class="detail__content-list">
    <article>

      <CompanyDetailSummary
        :company
      />

      <CompanyDetailValuation
        :company
      />

      <div class="detail__future"></div> <!-- /detail__future -->

      <div class="detail__past"></div> <!-- /detail__past -->

      <div class="detail__health"></div> <!-- /detail__health -->

      <div class="detail__dividend"></div> <!-- /detail__dividend -->

      <div class="detail__management"></div> <!-- /detail__management -->

      <div class="detail__ownership"></div> <!-- /detail__ownership -->

      <div class="detail__other"></div> <!-- /detail__other -->

    </article>
  </div>
</template>

<script lang="ts">
  import CompanyDetailSummary from "@/components/company_detail/CompanyDetailSummary.vue";
  import CompanyDetailValuation from "@/components/company_detail/CompanyDetailValuation.vue";

  export default {
    name: 'CompanyDetailContentList',
    components: {CompanyDetailValuation, CompanyDetailSummary},
    props: {
      company: {
        type: Object,
        required: true,
      }
    }
  }
</script>

<style scoped>
  .detail__content-list {
    position: relative;
    width: 100%;
    min-height: 0;
    flex: 0 0 75%;
    max-width: 75%;
  }
</style>