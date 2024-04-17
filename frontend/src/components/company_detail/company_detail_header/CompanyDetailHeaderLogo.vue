<script lang="ts">
import {defineComponent} from 'vue'
import {mapState} from "vuex";

export default defineComponent({
  name: "CompanyDetailHeaderLogo",
  computed: {
    ...mapState({
      company: state => state.companyDetail.company,
    }),
  },
})
</script>

<template>
  <div class="detail-header__logo">
    <img :src="this.company.logo_url" alt="{{ this.company.slug }}">
  </div>
</template>

<style scoped>
  .detail-header__logo {
    margin: 4px 12px 0 8px;
    float: left;
    background-color: #fff;
    border-radius: 8px;
  }
  .detail-header__logo img {
    width: 56px;
    height: 56px;
    min-width: 56px;
    min-height: 56px;
    border: 1px solid #fff;
    border-radius: 8px;
    object-fit: scale-down;
    vertical-align: text-bottom;
  }
</style>