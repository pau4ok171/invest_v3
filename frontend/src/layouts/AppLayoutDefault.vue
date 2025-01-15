<script lang="ts">
import TheHeader from '@/components/base/header/TheHeader.vue'
import {defineComponent} from "vue";
import {mapState} from "vuex";

export default defineComponent({
  name: 'AppLayoutDefault',
  components: {
    TheHeader,
  },
  computed: {
    ...mapState({
      lateralMenuIsOpen: "lateralMenuIsOpen",
    }),
  },
})
</script>

<template>
<TheHeader/>

<div class="content">
  <div class="content__inner" :class="{'content__inner--moved': lateralMenuIsOpen}">
      <slot/>
  </div>
</div>
</template>

<style scoped>
.content {
  padding-top: 64px;
  display: flex;
  position: relative;
  flex-wrap: wrap;
  justify-content: center;
}
.content__inner {
  position: relative;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  width: 100%;
  color: #fff;
  padding: 0 24px 24px;
  transition: all .6s cubic-bezier(.83, 0, .17, 1) 0s;
}
.content__inner--moved {
  max-width: 1582px;
}
</style>