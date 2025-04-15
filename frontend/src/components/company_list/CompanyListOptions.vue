<script setup lang="ts">
// Composables
import { useCompanyListStore } from '@/store/companyList/companyList'

const store = useCompanyListStore()
</script>

<template>
  <section class="company-list__options">
    <div></div>
    <div class="company-list__company-count">
      <v-skeleton-loader
        v-if="store.fetching"
        loading
        type="text"
        width="150"
      />
      <p v-else>{{ store.totalCompanyLength }} companies</p>
    </div>
    <div class="company-list__view-modes">
      <v-btn-toggle v-model="store.contentMode" mandatory>
        <v-btn icon="$iTableMode" variant="text" value="table" />
        <v-btn icon="$iTileMode" variant="text" value="tile" />
      </v-btn-toggle>
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
  color: rgb(var(--v-theme-on-surface-variant));
}
.company-list__view-modes {
  display: grid;
  grid-template-columns: auto auto;
  justify-content: end;
}
</style>
