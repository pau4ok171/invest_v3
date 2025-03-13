<script setup lang="ts">
// Components
import { BaseButton } from '@/apps/visagiste/components/BaseButton'

// Composables
import { useCompanyListStore } from '@/store/companyList'

const companyListStore = useCompanyListStore()
</script>

<template>
  <section class="company-list__options">
    <div></div>
    <div class="company-list__company-count">
      <p>{{ companyListStore.totalCompanyLength }} companies</p>
    </div>
    <div class="company-list__view-modes">
      <base-button icon="$iTableMode" variant="text" disabled />

      <base-button icon="$iTileMode" variant="text" />
    </div>
  </section>
</template>

<style lang="scss">
.company-list__options {
  display: grid;
  grid-template-columns: 250px auto 250px;
}
.company-list__company-count {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: normal;
  line-height: 1.5;
  color: rgb(var(--base-theme-on-surface-variant));
}
.company-list__view-modes {
  display: grid;
  grid-template-columns: auto auto;
  justify-content: end;
}
</style>
