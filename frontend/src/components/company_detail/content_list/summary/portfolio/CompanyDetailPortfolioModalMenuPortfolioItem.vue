<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import {mapGetters} from "vuex";
import type {Portfolio} from "@/types/portfolios";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyDetailPortfolioModalMenuPortfolioItem",
  components: {
    BaseButton,
  },
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
      <base-button
        prepend-icon="CheckedIcon"
        text="added"
        theme="success"
        rounded="large"
        disabled
      />

      <base-button
        icon="TrashIcon"
        theme="error"
        rounded="x-small"
        density="comfortable"
        :loading="portfolioIsLoading"
        @click="$emit('updatePortfolio', 'exclude', portfolio)"
      />
    </template>

    <template v-else>
      <base-button
        prepend-icon="PlusIcon"
        text="add"
        theme="blue"
        rounded="large"
        :loading="portfolioIsLoading"
        @click="$emit('updatePortfolio', 'include', portfolio)"
      />
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