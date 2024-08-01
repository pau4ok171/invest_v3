<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminModelIndicator",
  props: {
    isActive: {
      type: Boolean,
      default: false,
    },
  },
})
</script>

<template>
<div>
  <div class="admin-model-indicator" :class="{'admin-model-indicator--is-active': isActive}">
    <div class="admin-model-indicator__bounce1"></div>
    <div class="admin-model-indicator__bounce2"></div>
  </div>
</div>
</template>

<style scoped lang="scss">
.admin-model-indicator {
  position: absolute;

  .admin-model-indicator__bounce1,
  .admin-model-indicator__bounce2 {
    border-radius: 50%;
    position: absolute;
    background-color: #b01111;
    top: 0;
    left: 0;
    width: 8px;
    height: 8px;
  }

  .admin-model-indicator__bounce1 {
    opacity: 0.5;
    -webkit-animation: in-bounce 2s infinite ease-in-out;
    animation: in-bounce 2s infinite ease-in-out;
  }

  @keyframes in-bounce {
    0%,
    100% {
      transform: scale(1.0);
    }
    50% {
      transform: scale(2);
    }
  }
}
.admin-model-indicator--is-active {

  .admin-model-indicator__bounce1,
  .admin-model-indicator__bounce2 {
      background-color:  #4B8232;
    }
  }
</style>