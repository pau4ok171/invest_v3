<script lang="ts">
import CompanyDetailHeader from "@/components/company_detail/header/CompanyDetailHeader.vue";
import CompanyDetailContent from "@/components/company_detail/CompanyDetailContent.vue";
import {mapActions, mapGetters, mapMutations} from "vuex";
import {defineComponent} from "vue";
import {RouteNamesEnum} from "@/router/routes.types";
import PageNotFound from "@/components/base/page_not_found/PageNotFound.vue";

export default defineComponent({
  name: 'CompanyDetail',
  components: {
    PageNotFound,
    CompanyDetailContent,
    CompanyDetailHeader
  },
  mounted() {
    this.initializeView()
    },
  unmounted() {
    this.setPageNotFound(false)
  },
  methods: {
    async initializeView() {
      this.setPageIsReady(false)
      const company_slug = this.$route.params.company_slug as String
      await this.fetchCompany(company_slug)
      if (!this.pageNotFound) {
        await this.fetchPriceData(company_slug)
        document.title = `${this.company.title} (${this.company.market.title}:${this.company.ticker}) - Обзор компании, Новости, Аналитика - Finargo`
      }
      this.setPageIsReady(true)
    },
    ...mapMutations({
      setPageIsReady: 'companyDetail/setPageIsReady',
      setPageNotFound: 'companyDetail/setPageNotFound',
    }),
    ...mapActions({
      fetchCompany: 'companyDetail/fetchCompany',
      fetchPriceData: 'companyDetail/fetchPriceData',
    }),
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      pageNotFound: 'companyDetail/getPageNotFound',
    })
  },
  watch: {
    $route(to) {
      if (to.name === RouteNamesEnum.company_detail) {
        this.initializeView()
      }
    }
  },
})
</script>

<template>
<PageNotFound v-if="pageNotFound"/>
<div v-else>
  <CompanyDetailHeader/>
  <CompanyDetailContent/>
</div>

</template>
