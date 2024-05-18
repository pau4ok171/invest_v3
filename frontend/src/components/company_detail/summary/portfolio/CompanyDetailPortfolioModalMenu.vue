<script lang="ts">
import {defineComponent} from 'vue'
import BaseModalMenu from "@/components/UI/base/BaseModalMenu.vue";
import {mapActions, mapGetters, mapMutations} from "vuex";
import CompanyDetailPortfolioModalMenuPortfolioItem
  from "@/components/company_detail/summary/portfolio/CompanyDetailPortfolioModalMenuPortfolioItem.vue";
import RoundedHighGreyButton from "@/components/UI/buttons/RoundedHighGreyButton.vue";
import NewPortfolioInput from "@/components/UI/inputs/NewPortfolioInput.vue";
import axios from "axios";
import {toast} from "vue3-toastify";
import type {Portfolio} from "@/types/portfolios";

export default defineComponent({
  name: "CompanyDetailPortfolioModalMenu",
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
  components: {
    NewPortfolioInput,
    RoundedHighGreyButton,
    CompanyDetailPortfolioModalMenuPortfolioItem,
    BaseModalMenu,
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
<BaseModalMenu>

  <template #title>Add SBER to Portfolio</template>

  <template #content>
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
      <RoundedHighGreyButton @click.stop="changeMode" v-else>
        <span>New Portfolio</span>
      </RoundedHighGreyButton>
    </div>
  </template>

</BaseModalMenu>
</template>

<style scoped>
.detail-portfolio-modal-menu__new {
  display: flex;
  justify-content: flex-start;
  padding: 16px 16px 16px 24px;
}
</style>