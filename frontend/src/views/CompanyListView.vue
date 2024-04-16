<template>
  <section>

    <CompanyListHeader
      :companies="sortedCompanies"
      :totalCompaniesLength="totalCompaniesLength"
      :filters="filteredFilters"
      :active_filters
      :list_updated
      :country_search_query="country_search_query"
      :sector_search_query="sector_search_query"
      @updateCountrySearchQuery="updateCountrySearchQuery"
      @updateSectorSearchQuery="updateSectorSearchQuery"
      @fetchNewCompanies="fetchNewCompanies"
    />
    <CompanyListContent
      :companies="sortedCompanies"
      :next_url
      @fetchMoreCompanies="fetchCompanies"
      @toggleToWatchlist="toggleToWatchlist"
    />

    <Notification>
      <template v-slot:icon>
        <CheckmarkCircleIcon fill="#2dc97e"/>
      </template>
      <template v-slot:message>
        Success
      </template>

    </Notification>

  </section>
</template>

<script lang="ts">
import CompanyListHeader from "@/components/company_list/CompanyListHeader.vue";
import CompanyListContent from "@/components/company_list/CompanyListContent.vue";
import axios from "axios";
import store from "@/store";
import Notification from "@/components/UI/Notification.vue";
import CheckmarkCircleIcon from "@/components/icons/CheckmarkCircleIcon.vue";

export default {
  name: 'CompanyList',
  components: {
    CheckmarkCircleIcon,
    Notification,
    CompanyListHeader,
    CompanyListContent,
  },
  data() {
    return {
      companies: [],
      filters: {
        country: [],
        sector: [],
        sorter: [],
      },
      active_filters: {
        country: {},
        sector: {},
        sorter: {},
      },
      list_updated: '',
      country_search_query: '',
      sector_search_query: '',
      totalCompaniesLength: 0,
      next_url: '/invest/api/v1/companies',
    }
  },
  methods: {
    updateCountrySearchQuery(value) {
      this.country_search_query = value
    },
    updateSectorSearchQuery(value) {
      this.sector_search_query = value
    },
    fetchNewCompanies() {
      this.next_url = `/invest/api/v1/companies/${this.active_filters.country.slug}/${this.active_filters.sector.slug}`
      this.companies = []
      this.fetchCompanies()
      this.fetchFiltersByCountry()
    },
    async fetchCompanies() {
      store.commit('setIsLoading', true)

      await axios
        .get(this.next_url)
        .then(response => {
          this.companies = [...this.companies, ...response.data.results]
          this.next_url = response.data.next
          this.totalCompaniesLength = response.data.count
        })
        .catch(error => console.log(error))

      store.commit('setIsLoading', false)
    },
    async fetchFilters() {
      await axios
        .get('/invest/api/v1/filters')
        .then(response => {
          const data = response.data
          this.filters.country = [{title: 'Global', slug: 'global', required: true}, ...data.filters.country]
          this.filters.sector = [{title: 'Any', slug: 'any', required: true}, ...data.filters.sector]
          this.filters.sorter = data.filters.sorter
          this.active_filters.country = this.filters.country[0]
          this.active_filters.sector = this.filters.sector[0]
          this.active_filters.sorter = this.filters.sorter[0]
          this.list_updated = data.list_updated
        })
        .catch(error => console.log(error))
    },
    async fetchFiltersByCountry() {
      await axios
        .get(`invest/api/v1/filters/sector/${this.active_filters.country.slug}`)
        .then(response => {
          this.filters.sector = [{title: 'Any', slug: 'any', required: true}, ...response.data.filters.sector]
        })
        .catch(error => console.log(error))
    },
    toggleToWatchlist(object) {
      this.companies.forEach(company => {
        if (company.uid === object.uid) {
          company.is_watchlisted = object.is_watchlisted
        }
      })
    },
  },
  async mounted() {
    document.title = 'Stocks'
    await this.fetchFilters()
    await this.fetchCompanies()
  },
  computed: {
    sortedCompanies() {
      return [...this.companies]
        .sort((a, b) => (a.price_data[this.active_filters.sorter.order_type] - b.price_data[this.active_filters.sorter.order_type]) * (this.active_filters.sorter.reverse ? -1 : 1))
    },
    filteredAndSortedSectorFilters() {
      if (this.sector_search_query.length) {
        return [...this.filters.sector].filter(s => s.title.toLowerCase().includes(this.sector_search_query.toLowerCase()) || s.required)
      }
      return [...this.filters.sector]
    },
    filteredAndSortedCountryFilters() {
      let filters = {...this.filters}
      let countries = filters.country
      if (this.country_search_query.length) {
        return countries.filter(c => c.title.toLowerCase().includes(this.country_search_query.toLowerCase()) || c.required)
      }
      return countries
    },
    filteredFilters() {
      let filters = {...this.filters}
      filters.country = this.filteredAndSortedCountryFilters
      filters.sector = this.filteredAndSortedSectorFilters
      return filters
    },
  },
}
</script>
