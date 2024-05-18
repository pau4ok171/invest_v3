<script lang="ts">
import BasicHeader from '@/components/base/header/BasicHeader.vue'
import Loader from "@/components/UI/Loader.vue";
import {defineComponent} from "vue";
import {mapState} from "vuex";

export default defineComponent({
  name: 'AppLayoutDefault',
  components: {
    Loader,
    BasicHeader,
  },
  computed: {
    ...mapState({
      isLoading: 'isLoading',
    }),
  },
})
</script>

<template>
<BasicHeader :class="{'screen__blured':false}"/>

<div class="content">
  <div class="content__inner">
      <slot/>
  </div>
</div>

<Loader v-if="isLoading"/>
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
.screen__blured {
	filter: blur(6px);
}
</style>