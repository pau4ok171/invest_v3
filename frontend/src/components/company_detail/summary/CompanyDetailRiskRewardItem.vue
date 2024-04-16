<script lang="ts">
import {defineComponent} from 'vue'
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";

export default defineComponent({
  name: "CompanyDetailRiskRewardItem",
  components: {ArrowDownIcon, SolidStarIcon},
  props: {
    status: {
     type: String,
     required: true,
    }
  },
  methods: {
    getStatusClass() {
      const status_list = {
        reward: 'risk-reward-item__status-icon--reward',
        risk: 'risk-reward-item__status-icon--minor-risk',
        high_risk: 'risk-reward-item__status-icon--major-risk',
      }
      return status_list[this.status]
    }
  }
})
</script>

<template>
  <blockquote class="risk-reward-item">
    <div class="risk-reward-item__status-icon">
      <SolidStarIcon :class="getStatusClass()"/>
    </div>
    <div class="risk-reward-item__desc">
        <a href="#" class="risk-reward-item__link">
          <span><slot/></span>
          <ArrowDownIcon class="risk-reward-item__arrow-icon"/>
        </a>
    </div>
  </blockquote>
</template>

<style scoped>
  .risk-reward-item {
    position: relative;
    display: flex;
    margin-bottom: 8px;
    padding-left: 32px;
  }
  .risk-reward-item__status-icon {
    position: absolute;
    left: 0;
    padding: 4px;
  }
  .risk-reward-item__status-icon svg {
    transform: none;
    position: absolute;
    width: 24px;
    height: 24px;
    margin: 0;
    top: 0;
    left: 0;
    cursor: auto;
  }
  .risk-reward-item__status-icon--major-risk {
    fill: #e64141;
  }
  .risk-reward-item__status-icon--minor-risk {
    fill: #ff9212;
  }
  .risk-reward-item__status-icon--reward {
    fill: #2dc97e;
  }
  .risk-reward-item__desc {
    margin-top: -2px;
    font-size: 1.6rem;
    line-height: 1.5;
  }
  .risk-reward-item__link {
    position: relative;
    vertical-align: top;
    text-align: left;
    display: inline;
    padding: 4px 0;
  }
  .risk-reward-item__link:hover > span {
    box-shadow: #fff 0 -1px 0 0 inset;
    transition: box-shadow .2s ease;
  }
  .risk-reward-item__link:hover > .risk-reward-item__arrow-icon {
    transform: none;
  }
  .risk-reward-item__arrow-icon {
    display: inline;
    vertical-align: middle;
    margin: 0 -8px 0 -4px;
    transform: rotate(-90deg);
    transition: transform .2s ease-out;
    fill: #fff;
    opacity: .5;
  }
</style>