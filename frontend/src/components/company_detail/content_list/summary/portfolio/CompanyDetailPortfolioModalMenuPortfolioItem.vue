<script setup lang="ts">
// Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Types
import type { PropType } from 'vue'
import type { Portfolio } from '@/types/portfolios'

const companyDetailStore = useCompanyDetailStore()

const props = defineProps({
  portfolio: {
    type: Object as PropType<Portfolio>,
    required: true,
  },
})
</script>

<template>
  <div class="detail-portfolio-modal-menu-item">
    <div class="detail-portfolio-modal-menu-item__info-block">
      <div class="detail-portfolio-modal-menu-item__title">
        {{ portfolio.name }}
      </div>
      <div class="detail-portfolio-modal-menu-item__total-shares">
        {{ portfolio.positions.length }} Holdings
      </div>
    </div>

    <div class="detail-portfolio-modal-menu-item__actions">
      <template
        v-if="
          props.portfolio.positions.includes(
            companyDetailStore.company.id as number
          )
        "
      >
        <base-button
          prepend-icon="$iChecked"
          text="added"
          color="success"
          rounded="large"
          readonly
        />

        <base-button
          icon="$iDelete"
          color="error"
          rounded="lg"
          density="comfortable"
          @click="$emit('updatePortfolio', 'exclude', portfolio)"
        />
      </template>

      <template v-else>
        <base-button
          prepend-icon="$plus"
          text="add"
          color="info"
          rounded="large"
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
  font-size: 1.125rem;
  font-weight: 500;
}
.detail-portfolio-modal-menu-item__total-shares {
  font-size: 0.875rem;
  opacity: 0.5;
}
.detail-portfolio-modal-menu-item__actions {
  display: flex;
  gap: 5px;
  align-items: center;
}
</style>
