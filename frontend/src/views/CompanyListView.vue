<script lang="ts">
import CompanyListHeader from "@/components/company_list/CompanyListHeader.vue";
import CompanyListContent from "@/components/company_list/CompanyListContent.vue";
import {mapActions, mapGetters, mapMutations} from "vuex";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'CompanyList',
  components: {
    CompanyListHeader,
    CompanyListContent,
  },
  async mounted() {
    document.title = 'Stocks'
    await this.fetchFilters()
    await this.fetchCompanies()
    this.setPageIsReady(true)
  },
  methods: {
    ...mapActions({
      fetchCompanies: "companyList/fetchCompanies",
      fetchFilters: "companyList/fetchFilters",
    }),
    ...mapMutations({
      setPageIsReady: "companyList/setPageIsReady",
    })
  },
  computed: {
    ...mapGetters({
      pageIsReady: "companyList/getPageIsReady",
    }),
  },
})
</script>

<template>
<section>
  <CompanyListHeader v-if="pageIsReady"/>

  <CompanyListContent v-if="pageIsReady"/>
</section>
</template>
