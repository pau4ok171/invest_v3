<script lang="ts">
import {defineComponent} from 'vue'
import {mapGetters} from "vuex";
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";

export default defineComponent({
  name: "CompanyListOptions",
  components: {
    BaseButton,
  },
  computed: {
    ...mapGetters({
      totalCompaniesLength: "companyList/getTotalCompaniesLength",
    })
  },
})
</script>

<template>
<section class="company-list__options">
  <div></div>
  <div class="company-list__company-count">
    <p>{{ totalCompaniesLength }} companies</p>
  </div>
  <div class="company-list__view-modes">

    <base-button
      :icon="{value: 'TableModeIcon', size: 'large'}"
      variant="text"
      disabled
    />

    <base-button
      :icon="{value: 'TileModeIcon', size: 'large'}"
      variant="text"
    />

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
  font-size: 1.2rem;
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