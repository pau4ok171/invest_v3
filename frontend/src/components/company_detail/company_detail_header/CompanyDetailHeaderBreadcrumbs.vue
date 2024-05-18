<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyDetailBreadcrumbs",
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
  },
})
</script>

<template>
<div class="detail-header__breadcrumbs">
  <ul>
    <li>
      <RouterLink to="/">Stocks</RouterLink>
    </li>
    <li>
      <RouterLink to="/">{{ company.sector.title }}</RouterLink>
    </li>
  </ul>
</div>
</template>

<style scoped>
.detail-header__breadcrumbs {
  margin-bottom: 2.4rem;
}
.detail-header__breadcrumbs ul {
  font-size: 1.6rem;
}
.detail-header__breadcrumbs li {
  position: relative;
  display: inline-block;
  padding-right: .8rem;
}
.detail-header__breadcrumbs li:nth-child(2n)::before {
  content: '/';
  padding-right: .8rem;
}
.detail-header__breadcrumbs a {
  font-size: 1.4rem;
  text-decoration: underline;
  line-height: 1.5;
}
</style>