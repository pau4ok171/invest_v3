<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import RoundedSuccessButton from "@/components/UI/buttons/RoundedSuccessButton.vue";
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import RoundedErrorButton from "@/components/UI/buttons/RoundedErrorButton.vue";
import TrashIcon from "@/components/icons/TrashIcon.vue";
import RoundedBlueButton from "@/components/UI/buttons/RoundedBlueButton.vue";
import PlusIcon from "@/components/icons/PlusIcon.vue";
import {mapGetters} from "vuex";
import MiniLoader from "@/components/UI/MiniLoader.vue";
import type {Portfolio} from "@/types/portfolios";

export default defineComponent({
  name: "CompanyDetailPortfolioModalMenuPortfolioItem",
  components: {MiniLoader, PlusIcon, RoundedBlueButton, TrashIcon, RoundedErrorButton, CheckedIcon, RoundedSuccessButton},
  props: {
    portfolio: {
      type: Object as PropType<Portfolio>,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
      portfolioIsLoading: "companyDetail/getPortfolioIsLoading",
    }),
    isCompanyInPortfolio() {
      return this.portfolio.positions.includes(this.company.id)
    }
  },
})
</script>

<template>
<div class="detail-portfolio-modal-menu-item">
  <div class="detail-portfolio-modal-menu-item__info-block">
    <div class="detail-portfolio-modal-menu-item__title">{{ portfolio.name }}</div>
    <div class="detail-portfolio-modal-menu-item__total-shares">
      {{ portfolio.positions.length }} Holdings
    </div>
  </div>

  <div class="detail-portfolio-modal-menu-item__actions">
    <template v-if="isCompanyInPortfolio">
      <RoundedSuccessButton disabled>
        <CheckedIcon/>
        <span>Added</span>
      </RoundedSuccessButton>

      <RoundedErrorButton @click="$emit('updatePortfolio', 'exclude', portfolio)">
        <MiniLoader v-if="portfolioIsLoading"/>
        <TrashIcon v-else style="width: 20px; height: 20px;"/>
      </RoundedErrorButton>
    </template>

    <template v-else>
      <RoundedBlueButton @click="$emit('updatePortfolio', 'include', portfolio)">
        <MiniLoader v-if="portfolioIsLoading"/>
        <PlusIcon v-else style="width: 20px; height: 20px;"/>
        <span>Add</span>
      </RoundedBlueButton>
    </template>
  </div>
</div>
</template>

<style scoped>
.detail-portfolio-modal-menu-item {
  display: flex;
  justify-content: space-between;
  padding: 7px 24px;
  border-bottom: 1px solid #e8e8e8;
}
.detail-portfolio-modal-menu-item__info-block {
  color: #262e3a;
  line-height: 1.5;
  text-align: left;
}
.detail-portfolio-modal-menu-item__title {
  font-size: 1.8rem;
  font-weight: 500;
}
.detail-portfolio-modal-menu-item__total-shares {
  font-size: 1.4rem;
  opacity: .5;
}
.detail-portfolio-modal-menu-item__actions {
  display: flex;
  gap: 5px;
  align-items: center;
}
</style>