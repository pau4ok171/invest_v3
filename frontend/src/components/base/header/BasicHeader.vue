<template>
  <div class="header">
    <div class="header__inner">
      <Navigation/>
    </div>
  </div>
</template>

<script lang="ts">
  import {defineComponent} from "vue";
  import Navigation from "@/components/base/header/navigation/Navigation.vue";

  export default defineComponent({
    components: {Navigation}
  })
</script>

<style scoped>
  .header {
    background-color: var(--bg-color);
    width: 100%;
    position: fixed;
    z-index: 1000;
    display: flex;
    justify-content: center;
  }
  .header__inner {
    width: 1200px;
    font-size: 1.6rem;
    font-weight: normal;
    line-height: 1.5;
    color: #fff;
    height: 64px;
    padding: 0 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

</style>