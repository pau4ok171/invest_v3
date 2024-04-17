<script lang="ts">
import {defineComponent} from 'vue'
import {mapState} from "vuex";

export default defineComponent({
  name: "CompanyDetailHeaderTitle",
  computed: {
    ...mapState({
      company: state => state.companyDetail.company,
    }),
  },
})
</script>

<template>
  <div>
    <h1 class="detail-header__company-title">
      {{ this.company.title }}
      <span class="detail-header__company-desc">{{ this.company.market.title }}:{{ this.company.slug.toUpperCase() }} Stock Report</span>
    </h1>
  </div>
</template>

<style scoped>
  .detail-header__company-title {
    font-size: 3.6rem;
    line-height: 1.25;
    font-weight: 500;
    margin: 0 0 14px;
    overflow: hidden;
  }
  .detail-header__company-desc {
    display: block;
    font-size: 1.6rem;
    line-height: 1.5;
    color: rgba(255, 255, 255, .7);
  }
</style>