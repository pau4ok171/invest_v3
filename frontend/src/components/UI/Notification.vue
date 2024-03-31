<template>
  <div class="notification" v-if="isActive">
    <div class="notification__inner">
      <div class="notification__icon">
        <slot name="icon"/>
      </div>
      <div class="notification__text">
        <slot name="message"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
 export default {
   name: 'Notification',
   data() {
     return {
       isActive: false,
     }
   },
 }
</script>

<style>
  .notification {
    position: fixed;
    display: flex;
    vertical-align: middle;
    background-color: #202833;
    width: 448px;
    height: 53px;
    border: 1px solid #2b333d;
    border-radius: 5px;
    right: 30px;
    bottom: 50px;
  }
  .notification__inner {
    display: flex;
    align-items: center;
    gap: 17px;
  }
  .notification__icon {
    margin-left: 16px;
  }
  .notification__icon svg {
    height: 24px;
    width: 24px;
  }
  .notification__text {
    font-size: 16px;
    font-weight: 500;
  }
</style>