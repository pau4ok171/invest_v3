<script lang="ts">
import {mapState} from "vuex";
import {defineComponent} from "vue";

export default defineComponent({
  name: 'TheMain',
  computed: {
    ...mapState({
      lateralMenuIsOpen: "lateralMenuIsOpen",
    }),
  },
})
</script>

<template>
<div class="main">
  <div class="main__inner" :class="{'main__inner--moved': lateralMenuIsOpen}">
    <slot/>
  </div>
</div>
</template>

<style lang="scss">
.main {
  padding: 64px 24px 24px;
  display: flex;
  position: relative;
  flex-wrap: wrap;
  max-width: 100%;
  flex: 1 0 auto;
  justify-content: center;
  transition: .2s cubic-bezier(.4, 0, .2, 1);
}
.main__inner {
  position: relative;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  width: 100%;
}
.main__inner--moved {
  max-width: 1582px;
}
</style>