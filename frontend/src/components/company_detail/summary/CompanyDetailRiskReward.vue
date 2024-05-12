<script lang="ts">
import {defineComponent} from 'vue'
import CompanyDetailRiskRewardItem from "@/components/company_detail/summary/CompanyDetailRiskRewardItem.vue";
import RoundedDarkBlueButton from "@/components/UI/buttons/RoundedDarkBlueButton.vue";
import BaseModalMenuContainer from "@/components/UI/modal_menu/BaseModalMenuContainer.vue";
import TheCompanyDetailRisksModalMenu
  from "@/components/company_detail/summary/risks/TheCompanyDetailRisksModalMenu.vue";

export default defineComponent({
  name: "CompanyDetailRiskReward",
  components: {
    TheCompanyDetailRisksModalMenu,
    BaseModalMenuContainer, RoundedDarkBlueButton, CompanyDetailRiskRewardItem}
})
</script>

<template>
  <div class="risk-reward__container">

    <h3 class="risk-reward__title">Rewards</h3>

    <CompanyDetailRiskRewardItem status="reward">
      Trading at 59.5% below our estimate of its fair value
    </CompanyDetailRiskRewardItem>
    <CompanyDetailRiskRewardItem status="reward">
      Earnings are forecast to grow 8.24% per year
    </CompanyDetailRiskRewardItem>
    <CompanyDetailRiskRewardItem status="reward">
      Earnings grew by 52.4% over the past year
    </CompanyDetailRiskRewardItem>
    <CompanyDetailRiskRewardItem status="reward">
      Trading at good value compared to peers and industry
    </CompanyDetailRiskRewardItem>

    <h3 class="risk-reward__title">Risk Analysis</h3>

    <CompanyDetailRiskRewardItem status="high_risk">
      Shares are highly illiquid
    </CompanyDetailRiskRewardItem>
    <CompanyDetailRiskRewardItem status="risk">
      Unstable dividend track record
    </CompanyDetailRiskRewardItem>
    <CompanyDetailRiskRewardItem status="risk">
      Latest financial reports are more than 6 months old
    </CompanyDetailRiskRewardItem>

    <br>

    <BaseModalMenuContainer>
      <template #button>
        <RoundedDarkBlueButton>
          <span>See All Risk Checks</span>
        </RoundedDarkBlueButton>
      </template>
      <template #menu="menuProps">
        <TheCompanyDetailRisksModalMenu @closeMenu="menuProps.close()"/>
      </template>
    </BaseModalMenuContainer>

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