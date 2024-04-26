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

     const company_slug = this.$route.params.company_slug

     axios
       .get(`invest/api/v1/company/${company_slug}`)
       .then(response => {
         this.setCompany(response.data.company)
         this.setPortfolios(response.data.portfolios)
         this.setNotes(response.data.notes)
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