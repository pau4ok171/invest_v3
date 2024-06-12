<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailSidebarHeader",
    computed: {
      ...mapGetters({
        company: 'companyDetail/getCompany',
      })
  },
})
</script>

<template>
<header class="detail-sidebar__header">
<div class="detail-sidebar__snowflake">
<div class="detail-sidebar__logo">
  <img :src="company.logo_url" :alt="company.slug">
</div>
</div>
</header>
</template>

<style scoped>
.detail-sidebar__header {
  padding-bottom: 8px;
  visibility: hidden;
  opacity: 0;
}
.detail-sidebar__snowflake {
  margin: -18px -8px;
  max-width: 160px;
  padding-bottom: 16px;
}
.detail-sidebar__logo {
  margin: 4px 12px 0 8px;
  float: left;
  background-color: #fff;
  border-radius: 8px;
}
.detail-sidebar__logo img {
  width: 160px;
  height: 160px;
  padding: 11%;
}
</style>