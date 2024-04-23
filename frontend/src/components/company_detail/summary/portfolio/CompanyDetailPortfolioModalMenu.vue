<script lang="ts">
import {defineComponent} from 'vue'
import BaseModalMenu from "@/components/UI/base/BaseModalMenu.vue";
import ModalMenuCloseIcon from "@/components/icons/ModalMenuCloseIcon.vue";
import {mapActions, mapGetters, mapMutations} from "vuex";
import CompanyDetailPortfolioModalMenuPortfolioItem
  from "@/components/company_detail/summary/portfolio/CompanyDetailPortfolioModalMenuPortfolioItem.vue";
import RoundedHighGreyButton from "@/components/UI/buttons/RoundedHighGreyButton.vue";
import RoundedGreyButton from "@/components/UI/buttons/RoundedGreyButton.vue";
import NewPortfolioInput from "@/components/UI/inputs/NewPortfolioInput.vue";
import axios from "axios";
import {toast} from "vue3-toastify";

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
      setPortfolioModalMenuIsOpen: "companyDetail/setPortfolioModalMenuIsOpen",
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
      const formData = {
        portfolio_name: this.portfolioInputValue
      }
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
    async updatePortfolio(action, portfolio, company) {
      this.setPortfolioIsLoading(true)
      await axios
        .put(`portfolio/api/v1/portfolios/portfolios/${portfolio.id}/`, {'action': action, 'company_id': company.id})
        .then(response => {
          this.updatePortfoliosWithNewPortfolio(response.data)
          toast.success(`${company.slug.toUpperCase()} was added to ${portfolio.name}`)
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
    RoundedGreyButton,
    RoundedHighGreyButton,
    CompanyDetailPortfolioModalMenuPortfolioItem,
    ModalMenuCloseIcon,
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

  <header class="detail-portfolio-modal-menu__header">
    <h1 class="detail-portfolio-modal-menu__title">Add SBER to Portfolio</h1>
    <RoundedGreyButton @click="setPortfolioModalMenuIsOpen(false)"><ModalMenuCloseIcon/></RoundedGreyButton>
  </header>

  <main class="detail-portfolio-modal-menu__main">
    <CompanyDetailPortfolioModalMenuPortfolioItem
        v-for="portfolio in this.portfolios"
        :portfolio
        :key="portfolio.id"
        @updatePortfolio="updatePortfolio"
    />
  </main>

  <footer class="detail-portfolio-modal-menu__footer">
    <NewPortfolioInput
        v-if="inputMode"
        v-model="portfolioInputValue"
        v-model:inputMode="inputMode"
        @createNewPortfolio="createNewPortfolio"
    />
    <RoundedHighGreyButton @click.stop="changeMode" v-else><span>New Portfolio</span></RoundedHighGreyButton>
  </footer>

</BaseModalMenu>
</template>

<style scoped>
.detail-portfolio-modal-menu__header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #e8e8e8;
}
.detail-portfolio-modal-menu__title {
  font-size: 2rem;
  line-height: 1.5;
  font-weight: 500;
  color: #262e3a;
}
.detail-portfolio-modal-menu__main {
  max-height: 392px;
  overflow-y: auto;
  padding: 0;
  border-bottom: none;
}
.detail-portfolio-modal-menu__main::-webkit-scrollbar {
  width: 10px;
}
.detail-portfolio-modal-menu__main::-webkit-scrollbar-track {
	-webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
	background-color: #f9f9fd;
	border-radius: 10px;
}
.detail-portfolio-modal-menu__main::-webkit-scrollbar-thumb {
	border-radius: 10px;
	background: linear-gradient(180deg, #00c6fb, #005bea);
}
.detail-portfolio-modal-menu__footer {
  display: flex;
  justify-content: flex-start;
  padding: 16px 16px 16px 24px;
}
</style>