<template>

  <CompanyDetailHeader v-if="isFetched"/>

  <CompanyDetailContent v-if="isFetched"/>

</template>

<script lang="ts">
import CompanyDetailHeader from "@/components/company_detail/CompanyDetailHeader.vue";
import CompanyDetailContent from "@/components/company_detail/CompanyDetailContent.vue";


import store from "@/store";
import axios from "axios";
import {mapGetters, mapMutations} from "vuex";
import type {Competitor, DetailCompany} from "@/types/invest";
import type {Portfolio} from "@/types/portfolios";
import type {Note} from "@/types/notes";
import type {Statement} from "@/types/statements";

export default {
  name: 'CompanyDetail',
  components: {
    CompanyDetailContent,
    CompanyDetailHeader
  },
  data() {
    return {
      isFetched: false
    }
  },
  methods: {
   async  fetchCompany() {
     this.setIsLoading(true)

     const company_slug = this.$route.params.company_slug as String

     axios
       .get(`api/v1/invest/companies/${company_slug}`)
       .then(response => {
         this.setCompany(response.data.company as DetailCompany)
         this.setPortfolios(response.data.portfolios as Array<Portfolio>)
         this.setNotes(response.data.notes as Array<Note>)
         this.setStatements(response.data.statements as Array<Statement>)
         const snowflake: Array<Number> = Object.values(response.data.snowflake as Array<Number>)
         this.setSnowflake(snowflake)
         this.setCompetitors(response.data.peers as Array<Competitor>)
         document.title = `${this.company.title} (${this.company.market.title}:${this.company.ticker}) - Обзор компании, Новости, Аналитика - Finargo`
         this.isFetched = true
       })

     this.setIsLoading(false)
    },
    ...mapMutations({
      setIsLoading: 'setIsLoading',
      setCompany: 'companyDetail/setCompany',
      setPortfolios: 'companyDetail/setPortfolios',
      setNotes: "companyDetail/setNotes",
      setStatements: "companyDetail/setStatements",
      setSnowflake: "companyDetail/setSnowflake",
      setCompetitors: "companyDetail/setCompetitors",
    })
  },
  async mounted() {
    await this.fetchCompany()
    await store.dispatch("companyDetail/fetchPriceData", this.$route.params.company_slug)
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    })
  },
}
</script>