<template>
<!--  {% block scripts %}-->
<!--      <script src="https://cdn.jsdelivr.net/npm/luxon@3.4.4/build/global/luxon.min.js" defer></script>-->
<!--      <script src="{% static 'invest/js/company/detail/sidebar/sidebar.js' %}" defer></script>-->
<!--      <script type="module" src="{% static 'invest/js/company/detail/sidebar/copy.js' %}" defer></script>-->
<!--      <script type="module" src="{% static 'invest/js/company/detail/portfolio.js' %}" defer></script>-->
<!--      <script src="{% static 'invest/js/company/detail/detail.js' %}" defer></script>-->
<!--  {% endblock %}-->
  <CompanyDetailHeader v-if="isFetched"/>

  <CompanyDetailContent v-if="isFetched"/>

<!--  {% include 'invest/company/detail/modal_menu/analyst_sources_modal_menu.html' with company_info=company_detail_header_info %}-->
<!--  {% include 'invest/company/detail/modal_menu/add_to_portfolio_modal_menu.html' with company_info=company_detail_header_info %}-->
</template>

<script lang="ts">
import CompanyDetailHeader from "@/components/company_detail/CompanyDetailHeader.vue";
import CompanyDetailContent from "@/components/company_detail/CompanyDetailContent.vue";


import store from "@/store";
import axios from "axios";
import {mapMutations, mapState} from "vuex";

export default {
  name: 'CompanyDetail',
  components: {CompanyDetailContent, CompanyDetailHeader},
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
         document.title = `${this.company.title} (${this.company.market.title}:${this.company.ticker}) - Обзор компании, Новости, Аналитика - Finargo`
         this.isFetched = true
       })

     this.setIsLoading(false)
    },
    ...mapMutations({
      setIsLoading: 'setIsLoading',
      setCompany: 'companyDetail/setCompany',
      setPortfolios: 'companyDetail/setPortfolios',
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