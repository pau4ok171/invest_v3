<script lang="ts">
import {defineComponent} from 'vue'
import CheckmarkCircleIcon from "@/components/icons/CheckmarkCircleIcon.vue";
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import CheckIcon from "@/components/icons/CheckIcon.vue";
import CrossIcon from "@/components/icons/CrossIcon.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";

export default defineComponent({
  name: "CompanyDetailSectionIntroScore",
  components: {ArrowDownIcon, CrossIcon, CheckIcon, CheckedIcon, CheckmarkCircleIcon},
  props: {
    statements: {
      type: Array,
      required: true,
    }
  },
  computed: {
    statementPassCount() {
      return this.statements.reduce((acc, s) => {
        if (s.status === 'PASS') {
          acc += 1
        }
        return acc
      }, 0)
    }
  }
})
</script>

<template>
  <div class="detail-section-intro-score__wrapper">
    <div class="detail-section-intro-score">
      <div class="detail-section-intro-score__inner">
        <p class="detail-section-intro-score__title">
          Valuation Score
          <span class="detail-section-intro-score__num">{{ statementPassCount }}/6</span>
        </p>
        <ul class="detail-section-intro-score__point-list">

          <li
              class="detail-section-intro-score__point"
              v-for="statement in statements"
              :key="statement.id"
          >
            <CheckIcon
                v-if="statement.status === 'PASS'"
                class="detail-section-intro-score__statement-icon-success"
            />
            <CrossIcon
                v-else
                class="detail-section-intro-score__statement-icon-error"
            />
            <p>{{ statement.title }}</p>
            <ArrowDownIcon class="detail-section-intro-score__arrow-icon"/>
          </li>

        </ul>
      </div>
    </div>
  </div>
</template>

<style>
  .detail-section-intro-score__wrapper {
    display: grid;
    grid-template: 1fr / repeat(2, 1fr);
  }
  .detail-section-intro-score {
    background-color: #262e3a;
    border-radius: 8px;
    padding: 12px 12px 16px;
    height: min-content;
  }
  .detail-section-intro-score__inner {
    display: flex;
    flex-flow: wrap;
    justify-content: left;
    align-items: flex-end;
  }
  .detail-section-intro-score__title {
    font-size: 1.4rem;
    line-height: 1.5;
    color: rgba(255, 255, 255, .7);
    margin-bottom: 8px;
  }
  .detail-section-intro-score__num {
    color: #fff;
    font-size: 1.4rem;
  }
  .detail-section-intro-score__point-list {
    list-style-type: none;
    font-size: 1.6rem;
    position: relative;
    width: 100%;
    min-height: 0;
    max-width: 100%;
    flex: 0 0 100%;
  }
  .detail-section-intro-score__point {
    margin-bottom: 8px;
    display: flex;
    flex-flow: wrap;
    justify-content: left;
    align-items: center;
    border-radius: 8px;
    cursor: pointer;
    margin-left: -8px;
    padding-left: 8px;
  }
  .detail-section-intro-score__point:hover {
    background-color: rgba(196, 196, 196, .063)
  }
  .detail-section-intro-score__point:hover .detail-section-intro-score__arrow-icon {
    transform: none;
  }
  .detail-section-intro-score__point p {
    font-size: 1.4rem;
    margin-left: 8px;
  }
  .detail-section-intro-score__statement-icon-success {
    width: 16px;
    height: 24px;
    fill: #2dc97e;
  }
  .detail-section-intro-score__statement-icon-error {
    width: 16px;
    height: 24px;
    fill: #e64141;
  }
  .detail-section-intro-score__arrow-icon {
    width: 1.5em;
    height: 1.5em;
    margin-left: auto;
    transition: transform .2s ease 0s;
    transform: rotate(-90deg);
    fill: #ffffff80;
  }
</style>