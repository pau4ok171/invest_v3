<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AdminModelIndicator',
  props: {
    isActive: {
      type: Boolean,
      default: false,
    },
  },
})
</script>

<template>
  <div class="d-flex justify-center align-center">
    <div
      class="admin-model-indicator"
      :class="{ 'admin-model-indicator--is-active': isActive }"
    >
      <div
        class="admin-model-indicator__bounce admin-model-indicator__bounce1"
      ></div>
      <div
        class="admin-model-indicator__bounce admin-model-indicator__bounce2"
      ></div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.admin-model-indicator {
  position: relative;
  width: 8px;
  height: 8px;

  .admin-model-indicator__bounce {
    border-radius: 50%;
    position: absolute;
    background-color: #b01111;
    width: 8px;
    height: 8px;
  }
  .admin-model-indicator__bounce1 {
    opacity: 0.5;
    animation: bounce 2s infinite ease-in-out;
  }
  @keyframes bounce {
    0%,
    100% {
      transform: scale(1);
    }
    50% {
      transform: scale(2);
    }
  }
}
.admin-model-indicator--is-active {
  .admin-model-indicator__bounce {
    background-color: #4b8232;
  }
}
</style>
