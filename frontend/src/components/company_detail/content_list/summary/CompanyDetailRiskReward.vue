<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailRiskRewardItem from "@/components/company_detail/content_list/summary/CompanyDetailRiskRewardItem.vue";
import TheCompanyDetailRisksModalMenu
  from "@/components/company_detail/content_list/summary/risks/TheCompanyDetailRisksModalMenu.vue";
import {mapGetters} from "vuex";
import type {Statement} from "@/types/statements";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";
import BaseDialog from "@/components/UI/base/components/BaseDialog/BaseDialog.vue";

export default defineComponent({
  name: "CompanyDetailRiskReward",
  components: {
    BaseDialog,
    BaseButton,
    TheCompanyDetailRisksModalMenu,
    CompanyDetailRiskRewardItem
  },
  computed: {
    ...mapGetters({
      statements: 'companyDetail/getStatements',
    }),
    get_rewards() {
      return Object.fromEntries(Object.entries((this.statements as {[name: string]: Statement}))
          .filter(([, s]) => s.type === 'REWARDS' && s.status === 'PASS' && s.outcome > 1000))
    },
    get_risks() {
      const filtered = Object.fromEntries(Object.entries(this.statements as {[name: string]: Statement})
          .filter(([, s]) => s.type === 'RISKS' && s.status === 'FAIL' && s.outcome > 1000))
      return Object.fromEntries(Object.entries(filtered).sort(([, s1], [, s2]) => s1.severity === 'MAJOR' ? -1: 1))
    },
  },
})
</script>

<template>
<div class="risk-reward__container">

  <h3 class="risk-reward__title">Rewards</h3>

  <CompanyDetailRiskRewardItem v-for="statement in get_rewards" :statement :key="statement.id"/>

  <h3 class="risk-reward__title">Risk Analysis</h3>

  <CompanyDetailRiskRewardItem v-for="statement in get_risks" :statement :key="statement.id"/>

  <br>

  <base-dialog
    title="Risk Checks"
    max-width="700"
  >
    <template #activator>
      <base-button
        text="See All Risk Checks"
        theme="dark-blue"
        lower
        rounded="large"
        size="small"
      />
    </template>
    <template #dialog>
      <TheCompanyDetailRisksModalMenu/>
    </template>
  </base-dialog>

</div>
</template>

<style scoped>
.risk-reward__container {
  min-height: 240px;
  margin-top: 24px;
}
.risk-reward__title {
  width: 100%;
  font-size: 1.4rem;
  line-height: 1.5;
  font-weight: normal;
  text-transform: uppercase;
  overflow: hidden;
  text-overflow: ellipsis;
  color: rgba(255, 255, 255, .7);
  margin-top: 8px;
  margin-bottom: 8px;
}
</style>