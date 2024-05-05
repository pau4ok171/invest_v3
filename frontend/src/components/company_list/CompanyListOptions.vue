<script lang="ts">
import {defineComponent} from 'vue'
import TileModeIcon from "@/components/icons/TileModeIcon.vue";
import CircledButton from "@/components/UI/buttons/CircledButton.vue";
import TableModeIcon from "@/components/icons/TableModeIcon.vue";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "CompanyListOptions",
  components: {
    TableModeIcon,
    CircledButton,
    TileModeIcon,
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
    <p>{{ this.totalCompaniesLength }} companies</p>
  </div>
  <div class="company-list__view-modes">

    <CircledButton disabled>
      <TableModeIcon/>
    </CircledButton>

    <CircledButton>
      <TileModeIcon/>
    </CircledButton>

  </div>
</section>
</template>

<style scoped>
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
  color: rgba(255, 255, 255, .3);
}
.company-list__view-modes {
  display: grid;
  grid-template-columns: auto auto;
  justify-content: end;
}
</style>