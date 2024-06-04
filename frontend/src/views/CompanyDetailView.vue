<script lang="ts">
import CompanyDetailHeader from "@/components/company_detail/CompanyDetailHeader.vue";
import CompanyDetailContent from "@/components/company_detail/CompanyDetailContent.vue";
import {mapActions, mapGetters, mapMutations} from "vuex";
import {defineComponent} from "vue";
import {RouteNamesEnum} from "@/router/routes.types";

export default defineComponent({
  name: 'CompanyDetail',
  components: {
    CompanyDetailContent,
    CompanyDetailHeader
  },
  mounted() {
    this.initializeView()
    },
  methods: {
    async initializeView() {
      const company_slug = this.$route.params.company_slug as String
      await this.fetchCompany(company_slug)
      await this.fetchPriceData(company_slug)
      document.title = `${this.company.title} (${this.company.market.title}:${this.company.ticker}) - Обзор компании, Новости, Аналитика - Finargo`
      this.setPageIsReady(true)
    },
    ...mapMutations({
      setPageIsReady: 'companyDetail/setPageIsReady'
    }),
    ...mapActions({
      fetchCompany: 'companyDetail/fetchCompany',
      fetchPriceData: 'companyDetail/fetchPriceData',
    }),
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      pageIsReady: 'companyDetail/getPageIsReady',
    })
  },
  watch: {
    $route(to, from) {
      if (to.name === RouteNamesEnum.company_detail) {
        this.initializeView()
      }
    }
  },
})
</script>

<template>
<CompanyDetailHeader v-if="pageIsReady"/>

<CompanyDetailContent v-if="pageIsReady"/>
</template>
