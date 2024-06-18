<script lang="ts">
import {defineComponent} from 'vue'
import {mapMutations} from "vuex";

export default defineComponent({
  name: "BaseLateralMenuContainer",
  data() {
    return {
      isOpen: false,
      teleportTo: document.querySelector('.content__inner')
    }
  },
  methods: {
    close() {
      this.isOpen=false
      this.setLateralMenuIsOpen(false)
    },
    open() {
      this.isOpen=true
      this.setLateralMenuIsOpen(true)
    },
    ...mapMutations({
      setLateralMenuIsOpen: "setLateralMenuIsOpen",
    }),
  },
})
</script>

<template>
<div>
  <div @click="open">
    <slot name="button"/>
  </div>

  <Transition name="appear">
  <teleport :to="teleportTo">
    <div v-if="isOpen" class="teleported">
      <slot :close="close" name="menu"/>
    </div>
  </teleport>
  </Transition>
</div>
</template>

<style>
.appear-entry-active {
  animation: 600ms cubic-bezier(0.83, 0, 0.17, 1) 0s 1 normal none running lateral_mouvement;
}
.appear-leave-active {
  animation: 600ms cubic-bezier(0.83, 0, 0.17, 1) 0s 1 normal none running lateral_mouvement;
}
@keyframes lateral_mouvement {
  0% {
    transform: translateX(100%);
    opacity: 0;
  }
  100% {
    transform: translateX(0%);
    opacity: 1;
  }
}
</style>
