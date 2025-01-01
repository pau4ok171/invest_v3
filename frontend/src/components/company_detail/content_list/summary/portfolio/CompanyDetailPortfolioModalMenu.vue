<script lang="ts">
import {defineComponent} from 'vue'
import {mapActions, mapGetters, mapMutations} from "vuex";
import CompanyDetailPortfolioModalMenuPortfolioItem
  from "@/components/company_detail/content_list/summary/portfolio/CompanyDetailPortfolioModalMenuPortfolioItem.vue";
import NewPortfolioInput from "@/components/UI/inputs/NewPortfolioInput.vue";
import axios from "axios";
import {toast} from "vue3-toastify";
import type {Portfolio} from "@/types/portfolios";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailPortfolioModalMenu",
  components: {
    BaseButton,
    NewPortfolioInput,
    CompanyDetailPortfolioModalMenuPortfolioItem,
  },
  data() {
    return {
      inputMode: false,
      portfolioInputValue: null,
    }
  },
  methods: {
    ...mapMutations({
      addNewPortfolio: "companyDetail/addNewPortfolio",
      setPortfolioIsLoading: "companyDetail/setPortfolioIsLoading",
    }),
    ...mapActions({
      updatePortfoliosWithNewPortfolio: "companyDetail/updatePortfoliosWithNewPortfolio",
    }),
    changeMode() {
      this.inputMode = true
    },
    async createNewPortfolio() {
      const formData = new FormData()
      const formDataFields: Object = {
        portfolio_name: this.portfolioInputValue,
      }
      Object.entries(formDataFields).forEach(([key, val]) => formData.append(key, val))

      await axios
        .post('portfolio/api/v1/portfolios/portfolios/', formData)
        .then(response => {
          this.addNewPortfolio(response.data)
          this.portfolioInputValue = null
          this.inputMode = false
          toast.success(`Portfolio ${response.data.name} was created`)
        })
        .catch(error => {
          console.log(error)
          toast.error('Something was wrong...')
        })
    },
    async updatePortfolio(action: string, portfolio: Portfolio) {
      const formData = new FormData()
      Object.entries({
          action: action,
          company_id: this.company.id,
      }).forEach(([key, val]) => formData.append(key, val))

      this.setPortfolioIsLoading(true)
      await axios
        .put(`portfolio/api/v1/portfolios/portfolios/${portfolio.id}/`, formData)
        .then(response => {
          this.updatePortfoliosWithNewPortfolio(response.data)
          if (action === 'include') {
            toast.success(`${this.company.slug.toUpperCase()} was added to ${portfolio.name}`)
          } else {
            toast.success(`${this.company.slug.toUpperCase()} was remove from ${portfolio.name}`)
          }
        })
        .catch(error => {
          console.log(error)
          toast.error('Something was wrong...')
        })
      this.setPortfolioIsLoading(false)
    },
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      portfolios: 'companyDetail/getPortfolios',
    })
  },
})
</script>

<template>
<CompanyDetailPortfolioModalMenuPortfolioItem
  v-for="portfolio in portfolios"
  :portfolio
  :key="portfolio.id"
  @updatePortfolio="updatePortfolio"
/>

<div class="detail-portfolio-modal-menu__new">
  <NewPortfolioInput
    v-if="inputMode"
    v-model="portfolioInputValue"
    v-model:inputMode="inputMode"
    @createNewPortfolio="createNewPortfolio"
  />

  <base-button
    v-else
    text="new portfolio"
    theme="grey"
    color="#000"
    rounded="large"
    @click.stop="changeMode"
  />
</div>
</template>

<style scoped>
.detail-portfolio-modal-menu__new {
  display: flex;
  justify-content: flex-start;
  padding: 16px 16px 16px 24px;
  width: 600px;
}
</style>