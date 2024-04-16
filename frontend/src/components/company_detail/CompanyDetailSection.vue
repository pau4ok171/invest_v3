<template>
  <section :class="['detail-section', {'detail-section--min-h': useMinH}]">
    <div :class="{'detail-section__grid': useGrid}">
      <slot/>
    </div>
  </section>
</template>

<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CompanyDetailSection",
  props: {
    useGrid: {
      type: Boolean,
      default: false
    },
    useMinH: {
      type: Boolean,
      default: false
    },
  }
})
</script>

<style>
  .detail-section {
    position: relative;
    padding: 2.4rem 3.2rem;
    margin-bottom: 1.6rem;
    border-radius: 8px;
    background-color: #1b222d;
  }
  .detail-section--min-h {
    min-height: 360px;
  }
  .detail-section hr {
    height: 1px;
    border: transparent;
    border-top: 1px solid #fff;
    opacity: .2;
    margin-top: 32px;
    margin-bottom: 16px;
  }
  .detail-section__grid {
    display: grid;
    grid-template-columns: 1fr 280px;
    grid-template-rows: auto 1fr;
    column-gap: 8px;
  }
</style>