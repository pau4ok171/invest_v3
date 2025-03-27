<script setup lang="ts">
// Components
import NewPortfolioInput from '@/components/UI/inputs/NewPortfolioInput.vue'
import CompanyDetailPortfolioModalMenuPortfolioItem from '@/components/company_detail/content_list/summary/portfolio/CompanyDetailPortfolioModalMenuPortfolioItem.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { ref, shallowRef } from 'vue'
import axios from 'axios'
import { toast } from 'vue3-toastify'

// Types
import type { Portfolio } from '@/types/portfolios'

const companyDetailStore = useCompanyDetailStore()

const inputMode = shallowRef(false)
const inputValue = ref(null)

async function createNewPortfolio() {
  const formData = new FormData()
  const formDataFields: Object = {
    portfolio_name: inputValue.value,
  }
  Object.entries(formDataFields).forEach(([key, val]) =>
    formData.append(key, val)
  )

  await axios
    .post('portfolio/api/v1/portfolios/portfolios/', formData)
    .then((response) => {
      companyDetailStore.portfolios.push(response.data)
      inputValue.value = null
      inputMode.value = false
      toast.success(`Portfolio ${response.data.name} was created`)
    })
    .catch((error) => {
      console.log(error)
      toast.error('Something was wrong...')
    })
}

async function updatePortfolio(action: string, portfolio: Portfolio) {
  const formData = new FormData()
  Object.entries({
    action: action,
    company_id: companyDetailStore.company.id,
  }).forEach(([key, val]: [string, any]) => formData.append(key, val))

  await axios
    .put(`portfolio/api/v1/portfolios/portfolios/${portfolio.id}/`, formData)
    .then((response) => {
      companyDetailStore.updatePortfolios(response.data)
      if (action === 'include') {
        toast.success(
          `${companyDetailStore.company.slug?.toUpperCase()} was added to ${portfolio.name}`
        )
      } else {
        toast.success(
          `${companyDetailStore.company.slug?.toUpperCase()} was remove from ${portfolio.name}`
        )
      }
    })
    .catch((error) => {
      console.log(error)
      toast.error('Something was wrong...')
    })
}
</script>

<template>
  <CompanyDetailPortfolioModalMenuPortfolioItem
    v-for="portfolio in companyDetailStore.portfolios"
    :portfolio
    :key="portfolio.id as number"
    @updatePortfolio="updatePortfolio"
  />

  <div class="detail-portfolio-modal-menu__new">
    <NewPortfolioInput
      v-if="inputMode"
      v-model="inputValue"
      v-model:inputMode="inputMode"
      @createNewPortfolio="createNewPortfolio"
    />

    <v-btn
      v-else
      text="new portfolio"
      color="#000"
      rounded="large"
      @click.stop="inputMode = true"
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
